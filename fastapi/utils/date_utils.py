from datetime import date  # type: ignore

def generate_date_key(d: date) -> int:
    return int(d.strftime("%Y%m%d"))

def get_year(d: date) -> int:
    return d.year

def get_week_number(d: date) -> int:
    return d.isocalendar()[1]

def get_day_name(d: date) -> str:
    return d.strftime("%A")

def is_weekend(d: date) -> int:
    return 1 if d.weekday() >= 5 else 0

def extract_date_dimensions(d: date) -> dict:
    return {
        "date_key": generate_date_key(d),
        "sales_date": d,
        "year": get_year(d),
        "week_number": get_week_number(d),
        "day_name": get_day_name(d),
        "is_weekend": is_weekend(d)
    }
