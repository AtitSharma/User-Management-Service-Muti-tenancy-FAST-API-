
from fastapi.responses import JSONResponse
import uuid
from src.user_management.api.models import User
from src.user_management.api.v1.utility import RegisterUser
from sqlalchemy.orm import Session
from manage import migrate_all_tables_in_all_schema,db,upgrade_initial_migration
from src.schemas import ResponseSchema
from fastapi import status
from src.config import settings



class UserManagement:

    def register(self, user_data, db:Session,tenant_name):
        """ View to register user in the UMS service . 
        This view further register user in AUTH server and gives response of auth server """

        user_id = uuid.uuid4()
        password = user_data.__dict__.pop("password")
        user = User(id=user_id,**user_data.__dict__)
        db.add(user)
        db.commit()
        auth_user = RegisterUser(user_id=user_id,
                    email=user.email,password=password,
                    confirm_password=password,tenant_name=tenant_name)
        response = auth_user.register_user_in_auth()
        return JSONResponse(content=response)



    def register_new_tenant(self,tenant_name):
        '''
        This view will register new tenant in the UMS service 
        by calling the management commands functions.
        tenant_name : name of the schema (str) 
        '''
        
        # migrate all recent changes in all tenants 
        upgrade_initial_migration() 
        # make a photo copy of default schema in new schema
        migrate_all_tables_in_all_schema(db,settings.DEFAULT_SCHEMA,[tenant_name])
        return JSONResponse(ResponseSchema(code=201,
                message="New Tenant added in UMS successfully",
                data=[]).__dict__,status_code=status.HTTP_201_CREATED)
    

    # def register_new_office(self,office_details,db:Session):
    #     ''' 
    #     This view will register new office in the particular tenant.
    #         office_details: Schema containing details of office in order to register office in UMS
    #         db: Session connected with particular schema.  
    #     '''

    #     office = Office(**office_details.__dict__)
    #     db.add(office)
    #     db.commit()
    #     return JSONResponse(ResponseSchema(code=201,
    #             message="New Office Registered in UMS successfully",
    #             data=office_details.__dict__).__dict__,status_code=status.HTTP_201_CREATED)



    # def delete_office(self,db:Session,office_id):
    #     ''' 
    #     This view will delete office from the particular tenant
    #         db: Session connected with particular schema.  
    #         office_id : Integer (office_id) which is primary key of OMS service Office Model
    #     '''

    #     office = db.query(Office).filter(Office.office_id == office_id).first()
    #     if not office :
    #         raise ValueError({"office_id":"No such office with provided office_id"})
    #     db.delete(office)
    #     db.commit()
    #     return JSONResponse(content=ResponseSchema(code=200,
    #             message="Office Deleted Successfully",
    #             data=[]).__dict__,status_code=status.HTTP_200_OK)       
    
    # def update_office(self,db:Session,office_id,update_schema):
    #     '''
    #     This view will update office in the UMS service in particular tenant
    #         office_id : Integer (office_id) which is primary key of OMS service Office Model
    #         db: Session connected with particular schema.  
    #     '''

    #     office = get_or_not_found(db,Office,Office.office_id,office_id)
    #     office.name = update_schema.__dict__.get("name")
    #     db.commit()
    #     db.refresh(office)
    #     return JSONResponse(content=ResponseSchema(code=200,message="Office updated successfully",data=[]).__dict__,status_code=status.HTTP_200_OK)
