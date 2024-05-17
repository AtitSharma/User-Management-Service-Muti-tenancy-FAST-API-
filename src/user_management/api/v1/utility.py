import requests
import json
from src.user_management.api.schema import AuthUserRegisterSchema
from src.config import settings

class RegisterUser:
    def __init__(self,user_id,email
            ,password,confirm_password,tenant_name):
        self.user_id = user_id
        self.email = email
        self.password = password
        self.confirm_password = confirm_password
        self.tenant_name = tenant_name

    def register_user_in_auth(self):
        AUTH_SERVER_REGISTER_URL=settings.AUTH_SERVER_REGISTER_URL

        new_data = json.dumps(AuthUserRegisterSchema(user_id=str(self.user_id),email=self.email,password=self.password,confirm_password=self.confirm_password).__dict__)
        request= requests.post(url=AUTH_SERVER_REGISTER_URL,data=new_data,headers={
            "tenant_name":self.tenant_name
        }
        )
        return request.json()


