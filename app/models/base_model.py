from utils.db import db

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    
    def serialize(self) -> dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    
    def __str__(self):
        return f"<{self.__class__.__name__} {self.id}>"
    
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"