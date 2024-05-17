from sqlalchemy import  MetaData, Table, inspect,text
from sqlalchemy.orm import sessionmaker
from src.config import settings
from src.database import engine,sessionLocal
from alembic import command
from alembic.config import Config
import sys


DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
alembic_ini_path = "alembic.ini"


def get_global_db():
    ''' THIS function is get the database instance '''
    db = sessionLocal() 
    try:  
        yield db
    finally:
        db.close()

db = next(get_global_db()) 



def migrate_all_tables_in_all_schema(session, source_schema, target_schemas):

    ''' This method copies all tables from default schema to target schemas '''
    inspector = inspect(engine)
    tables = inspector.get_table_names(schema=source_schema)
    for table_name in tables:
        for target_schema in target_schemas:
            table = Table(table_name, metadata, schema=source_schema, autoload_with=engine)
            session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {target_schema}"))
            session.commit()
            table.schema = target_schema
            table.create(bind=engine, checkfirst=True)
            session.execute(text(f"INSERT INTO {target_schema}.{table_name} SELECT * FROM {source_schema}.{table_name}"))
            session.commit()


def main(new_schema):
    migrate_all_tables_in_all_schema(db,settings.DEFAULT_SCHEMA,[new_schema])


def upgrade_initial_migration():
    config=Config(alembic_ini_path)
    try:
        command.upgrade(config,"head") #upgrade the recent changes to avoid conflicts
    except Exception :
        print("Cannot apply initial migrations ")
        sys.exit()
        


if __name__ == "__main__":
    try :
        new_schema = sys.argv[1]
    except IndexError:
        print("Provide a schema name you want to add !!!!!")
        sys.exit()
    upgrade_initial_migration()
    main(new_schema)

    
    



    





