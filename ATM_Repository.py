from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy import String, ForeignKey
from typing import List, Optional
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.pool import NullPool
import configparser

#TODO HELP() will check if session file is present before choosing appropriate help prompt
#TODO use config parser to create the session file with details


CONFIG = "config.ini"
config_data = configparser.ConfigParser()
config_data.read(CONFIG)
option = config_data["options"]
for data in option: # gets config option for session_file
    if data == 'session_file':
        SESSION_FILE = option.get(data)
    if data =='atm_table':
        ATM_DB = option.get(data)

def table_init():
    engine = create_engine("sqlite+pysqlite:///" + ATM_DB, echo=False, poolclass=NullPool)
    class Base(DeclarativeBase):
        pass

    class Accounts(Base):  # This might be better off in a table schema file
        __tablename__ = "Accounts"
        account_id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(30))
        lastname: Mapped[str] = mapped_column(String(30))
        pin : Mapped[str]
        balance: Mapped[Optional[str]]
        transaction: Mapped[List["Transactions"]] = relationship(back_populates="accounts")

    class Transactions(Base):
        __tablename__ = "Transactions"
        id: Mapped[int] = mapped_column(primary_key=True)  #transaction ID
        type_of_transaction: Mapped[str]
        amount_in_trasaction: Mapped[str]
        account_id = mapped_column(ForeignKey("Accounts.account_id"))
        data: Mapped[str]
        accounts: Mapped[Accounts] = relationship(back_populates="transaction")
    with Session(engine) as session:
        Base.metadata.create_all(engine)
    #     session.flush()
    #     session.commit()
    # with Session(engine) as session:
    #     Base.metadata.create_all(engine)
    return engine, Base, Accounts, Transactions

class AtmCommands:
    """Methods for ATM Command"""
    @staticmethod
    def login(account_id, input_pin):
        engine, Base, Accounts, Transactions = table_init()
        with Session(engine) as session:
            retrieved_data = session.get(Accounts, account_id)

        if retrieved_data.pin == input_pin:
            config = configparser.ConfigParser()
            config.add_section("account")
            config.set("account", "id", account_id)
            with open(SESSION_FILE, 'w') as example:
                config.write(example)

        else:

            raise ValueError("PIN is incorrect")
        
    @staticmethod
    def create_account(name, lastname, pin):  #can be modified to accept ORM object instead of individual fields

        engine, Base, Accounts, Transactions = table_init()
        create_user = Accounts(name=name, lastname=lastname, pin=pin)
        with Session(engine) as session:
            session.add(create_user)
            session.flush()
            session.commit()

        
    @staticmethod
    def withdraw():
        pass

    @staticmethod
    def deposit(deposit_amount):
        engine, Base, Accounts, Transactions = table_init()
        with Session(engine) as session:
            deposit_balance = session.get(Accounts, 1)
            deposit_balance.balance = deposit_amount
            session.flush()
            session.commit()
        


    def check_balance(self):
        pass

    def change_pin(self):
        pass

    def pay_bills(self):
        pass

    def logout(self):
        pass
class InternalMethods:
    @staticmethod
    def get_one():
        pass

if __name__ == "__main__":
    # print(ATM_DB)
    name = "erjw"
    lastname = "aso"
    pin = "123543"
    AtmCommands.create_account(name, lastname, pin)    
#     pass
    # pass
