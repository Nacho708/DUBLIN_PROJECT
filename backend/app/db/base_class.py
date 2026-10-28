# backend/app/db/base_class.py
from typing import Any
from sqlalchemy.orm import as_declarative, declared_attr

@as_declarative()
class Base:
    id: Any
    __name__: str

    # Genera el nombre de la tabla automáticamente a partir del nombre de clase si no se define __tablename__
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()