from utils.db import db
from utils.exceptions import ModelNotFoundException, ModelAlreadyExistsException
from models.company import Company
from datetime import datetime

def get_all_companies() -> list:
    return Company.query.all()

def get_company_by_id(company_id: int) -> Company:
    company = Company.query.get(company_id)
    if not company:
        raise ModelNotFoundException("Company", company_id)
    return company

def search_company_by_name(name: str) -> list:
    company = Company.query.filter(Company.name.like(f"%{name}%")).all()
    if not company:
        raise ModelNotFoundException("Company", name)
    return company

def delete_company(company_id: int) -> None:
    company = get_company_by_id(company_id)
    db.session.delete(company)
    db.session.commit()
    
def add_company(company: Company) -> Company:
    db.session.add(company)
    db.session.commit()
    return company

def update_company(company: Company) -> Company:
    db.session.commit()
    return company