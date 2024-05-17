from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.exceptions import HTTPException

pwd_content = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    ''' Hashes the normal string '''
    return pwd_content.hash(password)


def verify(plain_password, hashed_password):
    ''' Verify the plain string with the hashed string '''
    return pwd_content.verify(plain_password, hashed_password)




def get_or_not_found(db:Session,model,search_field,value):

    ''' Custom get or not found method that raises 404 if the instance is not found else return object 
        db : Session 
        model : Database model
        search_field : model.id or model.search_field (requires sql_alchemy object)
        value : Search value 
    '''
    
    query = db.query(model).filter(search_field==value).first()
    if not query:
        raise HTTPException(status_code=404,detail="Cannot find instance")
    return query


