

from pydantic import BaseModel, EmailStr, model_validator

class UserDetailSchema(BaseModel):
    username : str     
    email: EmailStr
    contact_number: str

class UserRegisterSchema(UserDetailSchema):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def validate_password(cls, v):
        if v.password != v.confirm_password:
            raise ValueError({"password": "Both Password doesn't match"})
        if len(v.password) < 5:
            raise ValueError({"password": "Password is less than 5 characters"})
        v.__dict__.pop("confirm_password")
        return v


    






class AuthUserRegisterSchema(BaseModel):
    user_id : str
    email : EmailStr
    password : str    
    confirm_password : str  

class UserTokenDetails(BaseModel):
    access_token: str
    refresh_token: str

class RegisterOffice(BaseModel):
    office_id : int   
    name : str     

class UpdateOfficeSchema(BaseModel):
    name : str   