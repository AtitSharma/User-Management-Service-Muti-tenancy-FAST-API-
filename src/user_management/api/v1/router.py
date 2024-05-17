from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.user_management.api.v1.dependencies import UserManagementDependency
from src.database import CustomSession
from src.schemas import ValidationResponseSchema,ResponseSchema
from src.user_management.api.schema import (UserRegisterSchema,
        UserTokenDetails)
from src.user_management.api.v1.service import UserManagement


router = APIRouter(prefix="/ums/api/v1/ums", tags=["User"])
user_management = UserManagement()


@router.post(
    "/register/",
    response_model=UserTokenDetails,
    responses={422: {"model": ValidationResponseSchema}},
    description="Registers user in User management Service as well as in auth service "
)
def register(user_data: UserRegisterSchema,
            db: Session = Depends(CustomSession.get_db),
            tenant_name=Depends(UserManagementDependency.get_tenant_name)):
    return user_management.register(user_data, db,tenant_name)

@router.get("/register-new-tenant/{tenant_name}/",
            response_model=ResponseSchema,
            responses={422: {"model": ValidationResponseSchema}},
            description="Adds new tenant in the UMS service.\
            This api will ignore adding tenant if the tenant is already \
            available in the UMS service .")
def register_new_tenant(tenant_name,
                        user=Depends(UserManagementDependency.get_current_user)):
    return user_management.register_new_tenant(tenant_name)



# @router.post("/register-new-office/",
#              description="This Api will register new office \
#             in UMS service . This api is for OMS(Office Management System) \
#             Requires tenant name in the headers")
# def register_new_office(office_detail:RegisterOffice,
#         db = Depends(CustomSession.get_db),
#         user=Depends(UserManagementDependency.get_current_user)):
#     return user_management.register_new_office(office_detail,db)


# @router.delete("/delete-office/{office_id}/",
#     description="This Api is to delete the office from UMS service .\
#     This api is for OMS(Office Management System).\
#     Requires office_id from the url parameter")
# def delete_office(office_id,db=Depends(CustomSession.get_db),
#     user=Depends(UserManagementDependency.get_current_user)):
#     return user_management.delete_office(db,office_id)

# @router.patch("/update-office/{office_id}/",
#         description="This api id for OMS. This api will update office details in the system.")
# def update_office(office_id,update_schema:UpdateOfficeSchema,db=Depends(CustomSession.get_db),
#     user=Depends(UserManagementDependency.get_current_user)):
#     return user_management.update_office(db,office_id,update_schema)


