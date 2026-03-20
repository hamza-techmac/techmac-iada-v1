import os
import re
from string import Template

entities = [
    ("Role", "role", "roles"),
    ("User", "user", "users"),
    ("PaymentMethod", "payment_method", "payment_methods"),
    ("Provider", "provider", "providers"),
    ("FranchiseActiveChannel", "franchise_active_channel", "franchise_active_channels"),
]

SERVICE_TEMPLATE = Template("""from sqlalchemy.orm import Session
from sqlalchemy import text
from schemas import ${Entity}Create, ${Entity}Update
from queries import ${Entity}Queries

class ${Entity}Service:
    @staticmethod
    def get_all(db: Session):
        return db.execute(text(${Entity}Queries.GET_ALL)).mappings().all()

    @staticmethod
    def get_by_id(db: Session, entity_id: int):
        return db.execute(text(${Entity}Queries.GET_BY_ID), {"id": entity_id}).mappings().first()

    @staticmethod
    def create(db: Session, entity: ${Entity}Create):
        query = text(${Entity}Queries.INSERT)
        result = db.execute(query, entity.model_dump())
        db.commit()
        return result.lastrowid

    @staticmethod
    def update(db: Session, entity_id: int, entity: ${Entity}Update):
        update_data = entity.model_dump(exclude_unset=True)
        if not update_data:
            return False

        set_clause = ", ".join([f"{key} = :{key}" for key in update_data.keys()])
        query = text(${Entity}Queries.update_query(set_clause))
        
        update_data["id"] = entity_id
        result = db.execute(query, update_data)
        db.commit()
        
        return result.rowcount > 0
""")

ROUTER_TEMPLATE = Template("""from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import ${Entity}Create, ${Entity}Update
from services.${module}_service import ${Entity}Service

router = APIRouter(prefix="/${path}", tags=["${Entity}s"])

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    try:
        data = ${Entity}Service.get_all(db)
        return {"status": "success", "data": [dict(row) for row in data]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.get("/{id}")
def get_by_id(id: int, db: Session = Depends(get_db)):
    try:
        data = ${Entity}Service.get_by_id(db, id)
        if not data:
            raise HTTPException(status_code=404, detail="Not found")
        return {"status": "success", "data": dict(data)}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.post("/")
def create(entity: ${Entity}Create, db: Session = Depends(get_db)):
    try:
        new_id = ${Entity}Service.create(db, entity)
        return {"status": "success", "message": "Created successfully", "id": new_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@router.put("/{id}")
@router.patch("/{id}")
def update(id: int, entity: ${Entity}Update, db: Session = Depends(get_db)):
    try:
        updated = ${Entity}Service.update(db, id, entity)
        if not updated:
            raise HTTPException(status_code=404, detail="Not found or no fields to update")
        return {"status": "success", "message": "Updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        return {"status": "error", "message": str(e)}
""")

# 1. Generate new services and routers
for entity, module, path in entities:
    with open(f"services/{module}_service.py", "w") as f:
        f.write(SERVICE_TEMPLATE.substitute(Entity=entity, module=module, path=path))
    
    with open(f"routers/{path}.py", "w") as f:
        f.write(ROUTER_TEMPLATE.substitute(Entity=entity, module=module, path=path))

# 2. Add @router.patch to existing routers
for filename in os.listdir("routers"):  # type: ignore
    if filename.endswith(".py") and filename != "__init__.py":
        filepath = os.path.join("routers", filename)  # type: ignore
        with open(filepath, "r") as f:
            content = f.read()
        
        # Simple regex to find @router.put("/{param}") and add patch immediately after if it doesn't exist
        if "@router.patch" not in content and "@router.put" in content:
            # find all put mappings
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.strip().startswith('@router.put("'):
                    # insert patch right after
                    put_path = line.split('"')[1]
                    patch_line = f'@router.patch("{put_path}")'
                    lines.insert(i+1, patch_line)
                    break
            
            with open(filepath, "w") as f:
                f.write('\n'.join(lines))
