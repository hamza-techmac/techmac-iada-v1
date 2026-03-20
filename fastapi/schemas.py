from pydantic import BaseModel  # type: ignore
from typing import Optional  # type: ignore
from datetime import date  # type: ignore

class SaleCreate(BaseModel):
    sales_date: date
    branch_id: int
    channel_id: int
    amount: float

class FranchiseCreate(BaseModel):
    franchise_name: str
    owner_name: str
    contact_email: str

class FranchiseUpdate(BaseModel):
    franchise_name: Optional[str] = None
    owner_name: Optional[str] = None
    contact_email: Optional[str] = None

class FranchiseResponse(BaseModel):
    id: int
    franchise_name: str
    owner_name: str
    contact_email: str

class BranchCreate(BaseModel):
    franchise_id: int
    branch_name: str
    area_name: Optional[str] = None
    postcode: Optional[str] = None
    is_active: Optional[int] = 1
    city_id: int

class BranchUpdate(BaseModel):
    franchise_id: Optional[int] = None
    branch_name: Optional[str] = None
    area_name: Optional[str] = None
    postcode: Optional[str] = None
    is_active: Optional[int] = None
    city_id: Optional[int] = None

class BranchResponse(BaseModel):
    id: int
    franchise_id: int
    branch_name: str
    area_name: Optional[str] = None
    postcode: Optional[str] = None
    is_active: Optional[int] = None
    city_id: int

class ChannelCreate(BaseModel):
    id: int
    display_name: str
    payment_method_id: int
    provider_id: int

class ChannelUpdate(BaseModel):
    display_name: Optional[str] = None
    payment_method_id: Optional[int] = None
    provider_id: Optional[int] = None

class ChannelResponse(BaseModel):
    id: int
    display_name: str
    payment_method_id: int
    provider_id: int

class CityCreate(BaseModel):
    city_name: str
    region: Optional[str] = None

class CityUpdate(BaseModel):
    city_name: Optional[str] = None
    region: Optional[str] = None

class CityResponse(BaseModel):
    id: int
    city_name: str
    region: Optional[str] = None

# New Models
class RoleCreate(BaseModel):
    name: str

class RoleUpdate(BaseModel):
    name: Optional[str] = None

class RoleResponse(BaseModel):
    id: int
    name: str

class UserCreate(BaseModel):
    username: str
    password: str
    auth_key: Optional[str] = None
    old_password: Optional[str] = None
    role_id: int

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    auth_key: Optional[str] = None
    old_password: Optional[str] = None
    role_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role_id: int

class UserLogin(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    id: int
    username: str
    role_id: int
    auth_key: str

class PaymentMethodCreate(BaseModel):
    name: str

class PaymentMethodUpdate(BaseModel):
    name: Optional[str] = None

class PaymentMethodResponse(BaseModel):
    id: int
    name: str

class ProviderCreate(BaseModel):
    name: str

class ProviderUpdate(BaseModel):
    name: Optional[str] = None

class ProviderResponse(BaseModel):
    id: int
    name: str

class FranchiseActiveChannelCreate(BaseModel):
    branch_id: int
    channel_id: int
    is_active: Optional[bool] = True

class FranchiseActiveChannelUpdate(BaseModel):
    branch_id: Optional[int] = None
    channel_id: Optional[int] = None
    is_active: Optional[bool] = None

class FranchiseActiveChannelResponse(BaseModel):
    id: int
    branch_id: int
    channel_id: int
    is_active: bool
