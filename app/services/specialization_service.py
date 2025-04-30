from utils.db import db
from utils.exceptions import ModelNotFoundException, ModelAlreadyExistsException
from models.specialization import Specialization
from datetime import datetime

def get_all_specializations() -> list:
    return Specialization.query.all()

def get_specialization_by_id(specialization_id: int) -> Specialization:
    specialization = Specialization.query.get(specialization_id)
    if not specialization:
        raise ModelNotFoundException("Specialization", specialization_id)
    return specialization

def search_specialization_by_name(name: str) -> list:
    specialization = Specialization.query.filter(Specialization.name.like(f"%{name}%")).all()
    if not specialization:
        raise ModelNotFoundException("Specialization", name)
    return specialization

def delete_specialization(specialization_id: int) -> None:
    specialization = get_specialization_by_id(specialization_id)
    db.session.delete(specialization)
    db.session.commit()
    
def add_specialization(specialization: Specialization) -> Specialization:
    db.session.add(specialization)
    db.session.commit()
    return specialization

def update_specialization(specialization: Specialization) -> Specialization:
    db.session.commit()
    return specialization