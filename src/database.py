
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from fastapi import Depends
from src.user_management.api.v1.dependencies import UserManagementDependency
from src.config import settings
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

class CustomSession(Session):
    tenant_name = None
       
    def set_connection(self):
        self.connection(execution_options={
            "schema_translate_map": {settings.DEFAULT_SCHEMA:self.tenant_name }},
        ) # reconnecting to same session after commit flushes all sessions

    def commit(self):
        super().commit()
        self.set_connection()

    @classmethod
    def get_db(cls,schema_name=Depends(UserManagementDependency.get_tenant_name)):
    # expire_on_commit = False because when commit action is performed all session are killed
        db = sessionLocal(expire_on_commit=False) 
        try:
            cls.tenant_name = schema_name
            db.connection(execution_options={
                "schema_translate_map": {settings.DEFAULT_SCHEMA: schema_name}},
            )    
            yield db
        finally:
            db.close()

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,class_=CustomSession)
Base = declarative_base()




