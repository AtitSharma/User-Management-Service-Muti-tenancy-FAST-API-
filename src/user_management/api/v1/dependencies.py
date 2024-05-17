from fastapi import Request,Depends,HTTPException,status
import redis
from jose import JWTError,jwt
from src.config import settings
from fastapi.security import OAuth2PasswordBearer
import json

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")

r = redis.Redis(
host=settings.AUTH_REDIS_HOST,
port=settings.AUTH_REDIS_PORT,
decode_responses=True,
password=settings.AUTH_DB_PASSWORD,
)

class UserManagementDependency:

    @staticmethod
    def get_tenant_name(request : Request):
        """ returns tenant name from the request headers 
        other wise gives value error """

        tenant_name = request.headers.get("tenant_name")
        if not tenant_name :
            raise ValueError({"tenant_name":"Tenant name is required "})
        return tenant_name


    @classmethod
    def get_current_user(cls,token = Depends(oauth2_scheme)):
        ''' returns user_id from the redis cache of auth server 
        if exits else returns HTTP_401_UNAUTHORIZED '''

        jti = cls.get_jti_from_token(token)
        keys = r.keys(f"*:{jti}")
        if len(keys)<1:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        user_redis_jti_key= r.get(keys[0])
        user_all_data_in_redis = json.loads(user_redis_jti_key).get(jti)
        return user_all_data_in_redis.get("user_id")

        
        
    @classmethod
    def get_jti_from_token(cls,token):
        """ Returns jti from token payload  
        Ignores the expiry of token because expiry
        is checked in Redis Cache """

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, 
                       algorithms=[settings.ALGORITHM],options={"verify_exp": False}) 
            return payload.get("jti")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)



        

        


    



