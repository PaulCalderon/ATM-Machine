import os
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
from datetime import datetime

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
        amount_in_transaction: Mapped[Optional[str]]
        account_id = mapped_column(ForeignKey("Accounts.account_id"))
        date: Mapped[str]
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
    def login(account_id: str, input_pin:str) -> None:

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
    def create_account(name: str, lastname: str , pin: str)  -> None:  #can be modified to accept ORM object instead of individual fields

        engine, Base, Accounts, Transactions = table_init()
        create_user = Accounts(name=name, lastname=lastname, pin=pin)
        with Session(engine) as session:
            session.add(create_user)
            session.flush()
            session.commit()

        
    @staticmethod
    def withdraw(withdraw_amount: str) -> str:
        account_id = InternalMethods.get_active_session_id()
        withdraw_amount = int(withdraw_amount)

        engine, Base, Accounts, Transactions = table_init()
        with Session(engine) as session:
            current_balance = session.get(Accounts, account_id) 
            if int(current_balance.balance) >= withdraw_amount:
                old_balance = current_balance.balance
                current_balance.balance = int(current_balance.balance) - withdraw_amount
                session.commit()
            else:
                raise ValueError("Insufficient Balance")
            #ask to print recipt
            return account_id, old_balance, current_balance.balance
        

    @staticmethod
    def deposit(deposit_amount: str) -> None:
        account_id = InternalMethods.get_active_session_id()
        engine, Base, Accounts, Transactions = table_init()
        with Session(engine) as session:
            deposit_balance = session.get(Accounts, account_id)
            deposit_balance.balance = deposit_amount
            session.flush()
            session.commit()
        

    @staticmethod
    def check_balance() -> str:
        account_id = InternalMethods.get_active_session_id()
        engine, Base, Accounts, Transactions = table_init()
        with Session(engine) as session:
            current_balance = session.get(Accounts, account_id)
        return current_balance.balance
    
    @staticmethod
    def change_pin(new_pin: str) -> None:
        account_id = InternalMethods.get_active_session_id()
        engine, Base, Accounts, Transactions = table_init()
        with Session(engine) as session:
            account_data = session.get(Accounts, account_id)
            account_data.pin = new_pin
            session.flush()
            session.commit()

    @staticmethod
    def pay_bills(pay_amount: str) -> str: #TODO diffentiate from withdraw
        account_id = InternalMethods.get_active_session_id()
        pay_amount = int(pay_amount)

        engine, Base, Accounts, Transactions = table_init()
        with Session(engine) as session:
            current_balance = session.get(Accounts, account_id) 
            if int(current_balance.balance) >= pay_amount:
                old_balance = current_balance.balance
                current_balance.balance = int(current_balance.balance) - pay_amount
                session.commit()
                    #call receipt function
            else:
                raise ValueError("Insufficient Balance")
        return account_id, old_balance, current_balance.balance
    
    @staticmethod
    def logout()  -> None:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)


class TransactionsDatabase:
    @staticmethod
    def record_transaction(transaction_type, account_id, *amount): #should probably private and expose some other method

        today = datetime.today()
        date_and_time = today.strftime("%b-%d-%Y %H:%M:%S") #gets date 
        if len(amount) == 1:
            amount = amount[0]
        else:
            amount = None
        engine, Base, Accounts, Transactions = table_init()
        data_to_insert = Transactions(type_of_transaction= transaction_type, account_id= account_id, amount_in_transaction= amount, date= date_and_time)
        with Session(engine) as session:
            session.add(data_to_insert)
            session.flush()
            session.commit()


        
class InternalMethods:

    @staticmethod
    def get_active_session_id() -> str:
        config_data.read(SESSION_FILE)
        option = config_data["account"]
        for data in option:
            if data == 'id':
                return option.get(data)

    @staticmethod
    def receipt_output(id: str, old_balance: str, new_balance: str):
        return id, old_balance, new_balance
    
        # receipt_answer = input("Do you want a receipt? (y/n) ")
        # if receipt_answer in ['y',  'Y']:
        #     print("Receipt Printed")
        # elif receipt_answer in ['n' or 'N']:
        #     print("Account ID =", id)
        #     print("Old Balance =", old_balance)
        #     print("Current Balance =", new_balance)
        #     print("Data =") #TODO implement date and time


# if __name__ == "__main__":
#     InternalMethods.receipt_output("1", "2000", "1000")
    # print(ATM_DB)
    # name = "erjw"
    # lastname = "aso"
    # pin = "123543"
    # AtmCommands.create_account(name, lastname, pin)    
#     pass
    # pass
# if __name__ == "__main__":
#     TransactionsDatabase.record_transaction("deposit")