import sqlite3
# from flask import current_app, g
# from flask import Flask
import uuid
DATABASE = 'thndr_test.db'



def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn
def create_temp_users():
    db = get_db()
    print("CREATING TEMP USERS........................")
    uuids = ['e60a0530-c910-11ea-86cb-0242ac130002',
             'e615f3e0-c910-11ea-86cb-0242ac130002',
             'e6256e60-c910-11ea-86cb-0242ac130002', 
             'e634ed0e-c910-11ea-86cb-0242ac130002',
             'e642ae1c-c910-11ea-86cb-0242ac130002', 
             'e653a852-c910-11ea-86cb-0242ac130002']
    for uuid in uuids:
        
        # print(str(user_uuid))
        sql = """INSERT INTO dim_user(user_id,balance)VALUES(?,?)"""
        db.execute(sql,(uuid,0))
        db.commit()
class DataBase:
    def drop_table(self,table_name):
        cur = get_db()
        cur.execute( """ drop table IF EXISTS %s """ % table_name)
        cur.commit()
    def create_table(self,schema):
        cur = get_db()
        cur.execute(schema)
        cur.commit()
def Create_DB():
    db_helper = DataBase()
    tables = ['dim_user','fact_transaction','fact_trade']
    for table in tables:
        db_helper.drop_table(table)

    dim_user_schema = """
    
    CREATE TABLE dim_user (
                user_id VARCHAR(40) primary key,
                balance DECIMAL);
                
    """

    fact_transaction_schema = """
    
       CREATE TABLE fact_transaction (
                    transaction_id VARCHAR(40)primary key,
                    user_id VARCHAR(40), 
                    amount DECIMAL,
                    type VARCHAR(22),
                    transaction_timestamp timestamp,
                    Foreign Key(user_id) References dim_user(user_id));
    """
   
    fact_trade_schema = """
    CREATE TABLE fact_trade(
                 trade_id VARCHAR(40) primary key,
                 stock_id VARCHAR(40),
                 user_id VARCHAR(40),
                 total_stocks INTEGER,
                 stock_price Decimal,
                 trade_type VARCHAR(10),
                 trade_timestamp timestamp,
                 status VARCHAR(10),
                 note VARCHAR(100),
                 Foreign Key (user_id) References dim_user(user_id)
    );

    """
    schemas = [dim_user_schema,fact_transaction_schema,fact_trade_schema]
    for schema,table_name in zip(schemas,tables):

        db_helper.create_table(schema)
        print(table_name,"IS CREATED................")

# if __name__ =="__main__":

print("CREATING DATABASE............")
Create_DB()
create_temp_users() 
db = get_db()
users = db.execute("SELECT * from dim_user").fetchall()
print("Users................")
print(users)