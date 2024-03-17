from pydantic import BaseModel, Field
from sqlalchemy import Column, String
from app.domains.base import Base

########################################################
#                      DB MODEL                        #
########################################################


class Organization(Base):
    __tablename__ = 'organization'
    __table_args__ = {"info": {"db": "org"}}

    id = Column(String, primary_key=True)
    org_name = Column(String)
    created_at = Column(String)
    updated_at = Column(String)
    db_url = Column(String)


########################################################
#                    Pydantic Models                   #
########################################################

class OrganizationCreate(BaseModel):
    org_name: str = Field(...)
    created_at: str = Field(...)
    username: str = Field(...)
    password: str = Field(...)


