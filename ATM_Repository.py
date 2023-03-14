import os
from typing import List, Optional
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.pool import NullPool
import configparser

CONFIG = "config.ini"  #had a problem here. Ano best way to deal with getting settings from config file
config_data = configparser.ConfigParser()
config_data.read(CONFIG)
option = config_data["options"]
for data in option: # gets config option for session_file
    if data == 'session_file':
        SESSION_FILE = option.get(data)
    if data =='atm_table':
        ATM_DB = option.get(data)


def table_init():
    InternalMethods.get_updated_config() #work around for tests #fetches latest config data
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
        transaction_type = "Login"
        TransactionsDatabase.record_transaction(transaction_type, account_id)

    @staticmethod
    def create_account(name: str, lastname: str , pin: str)  -> None:  #can be modified to accept ORM object instead of individual fields
        engine, Base, Accounts, Transactions = table_init()
        create_user = Accounts(name=name, lastname=lastname, pin=pin)
        with Session(engine) as session:
            session.add(create_user)
            session.flush()
            account_id = create_user.account_id
            session.commit()
        transaction_type = "Create Account"
        TransactionsDatabase.record_transaction(transaction_type, account_id)

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
                new_balance = str(current_balance.balance)
                session.commit()
            else:
                raise ValueError("Insufficient Balance")
            #ask to print recipt
        transaction_type = "Withdraw"
        TransactionsDatabase.record_transaction(transaction_type, account_id, withdraw_amount)
        return account_id, old_balance, new_balance

    @staticmethod
    def deposit(deposit_amount: str) -> None:
        account_id = InternalMethods.get_active_session_id()
        deposit_amount = int(deposit_amount)
        engine, Base, Accounts, Transactions = table_init()
        with Session(engine) as session:
            deposit_balance = session.get(Accounts, account_id)
            deposit_balance.balance = deposit_amount + int(deposit_balance.balance or 0)
            session.flush()
            session.commit()
        transaction_type = "Deposit"
        TransactionsDatabase.record_transaction(transaction_type, account_id, deposit_amount)

    @staticmethod
    def check_balance() -> str:
        account_id = InternalMethods.get_active_session_id()
        engine, Base, Accounts, Transactions = table_init()
        with Session(engine) as session:
            current_balance = session.get(Accounts, account_id)
        transaction_type = "Check Balance"

        TransactionsDatabase.record_transaction(transaction_type, account_id)
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

        transaction_type = "Change Pin"
        TransactionsDatabase.record_transaction(transaction_type, account_id)

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
                new_balance = str(current_balance.balance)
                session.commit()
            else:
                raise ValueError("Insufficient Balance")

        transaction_type = "Change Pin"
        TransactionsDatabase.record_transaction(transaction_type, account_id, pay_amount)
        return account_id, old_balance, new_balance

    @staticmethod
    def logout()  -> None:
        if os.path.exists(SESSION_FILE):
            account_id = InternalMethods.get_active_session_id()
            os.remove(SESSION_FILE)
        transaction_type = "Logout"
        TransactionsDatabase.record_transaction(transaction_type, account_id)

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
    def get_updated_config() -> None:  #for testing purposes
        config_data = configparser.ConfigParser()
        config_data.read(CONFIG)
        option = config_data["options"]
        for data in option: # gets config option for session_file
            if data == 'session_file':
                global SESSION_FILE 
                SESSION_FILE = option.get(data)
            if data =='atm_table':
                global ATM_DB
                ATM_DB = option.get(data)
