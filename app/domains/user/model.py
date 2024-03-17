from pydantic import BaseModel, Field
from sqlalchemy import Column, String
from app.domains.base import Base

########################################################
#                      DB MODEL                        #
########################################################


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {"info": {"db": "tenant"}}

    id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)
    mail = Column(String)
    created_at = Column(String)
    updated_at = Column(String)


########################################################
#                    Pydantic Models                   #
########################################################

class UserCreate(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    mail: str = Field(...)
    password: str = Field(...)


