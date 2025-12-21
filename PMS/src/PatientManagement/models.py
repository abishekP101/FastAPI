from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlmodel import SQLModel , Field,Column
import sqlalchemy.dialects.postgresql as pg


from sqlmodel import SQLModel, Field
import uuid
import sqlalchemy.dialects.postgresql as pg


class Patient(SQLModel, table=True):
    __tablename__ = "patients"

    uid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        sa_column_kwargs={"nullable": False},
        sa_type=pg.UUID(as_uuid=True),
    )

    name: str = Field(nullable=False)
    city: str = Field(nullable=False)
    age: int = Field(nullable=False)
    gender: str = Field(nullable=False)
    height: float = Field(nullable=False)
    weight: float = Field(nullable=False)

    def __repr__(self):
        return f"<Patient {self.name}"

