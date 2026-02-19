from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import Module


class ModuleRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def update_module(self, new_module: Module) -> Module:
        self.db.add(new_module)
        self.db.commit()
        self.db.refresh(new_module)

        return new_module
    
    def create_module(self, module: Module) -> Module:
        self.db.add(module)
        self.db.commit()
        self.db.refresh(module)

        return module
    
    def delete_module(self, module_id: int) -> None:
        module = self.db.get(Module, module_id)

        if module:
            self.db.delete(module)
            self.db.commit()
