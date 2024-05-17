from sqlalchemy import Column,ForeignKey, Integer, String, UniqueConstraint, UUID,Boolean
from src.database import Base
from src.models import TimeStampMixin
from src.config import settings

default_schema = settings.DEFAULT_SCHEMA

class User(Base, TimeStampMixin):
    __tablename__ = "users"
    __table_args__ = ({'schema': default_schema})
    id = Column(UUID, primary_key=True, nullable=False)
    username = Column(String, nullable=False,unique=True)
    email = Column(String, nullable=False, unique=True)
    contact_number = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean,default=True)
    is_employee  = Column(Boolean,default=False)

    @property
    def full_name(self):
        if self.middle_name:
            return self.first_name + " " + self.middle_name + " " + self.last_name
        return self.first_name + " " + self.last_name

class Role(Base, TimeStampMixin):
    __tablename__ = "roles"
    __table_args__ = {'schema': default_schema}
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)

class UserRole(Base, TimeStampMixin):
    __tablename__ = "user_role"
    __table_args__ = (UniqueConstraint("user_id", "role_id", name="_user_role_uc"),{'schema': default_schema},)
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(
        UUID, ForeignKey(f"{default_schema}.users.id", ondelete="CASCADE"), nullable=False
    )
    role_id = Column(Integer, ForeignKey(f"{default_schema}.roles.id"), nullable=False)

