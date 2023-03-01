import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase
from sqlalchemy import String, ForeignKey
from typing import List, Optional
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
import configparser
import os

from configmaker import make_config


CONFIG = "config.ini"
config_data = configparser.ConfigParser()
config_data.read(CONFIG)
option = config_data["options"]
for data in option: # gets config option for session_file
    if data == 'session_file':
        SESSION_FILE = option.get(data)
    if data =='atm_table':
        ATM_DB = option.get(data)

make_config("test.db", "session.txt") # changes database to test.db

from ATM_Repository import AtmCommands, table_init

def test_program_should_create_session_file_on_sucessful_login():
    raise NotImplementedError

def test_program_should_have_details_in_login_in_the_session_file():
    raise NotImplementedError
        
def test_program_should_create_entry_upon_calling_the_function():
    name = "Paul"
    lastname = "August"
    pin = "123456"
    AtmCommands.create_account(name, lastname, pin)
    engine, Base, Accounts, Transactions = table_init()
    submitted_data = Accounts(name=name, lastname=lastname, pin=pin)

    with Session(engine) as session:
        retrieved_data = session.get(Accounts, 1)

    assert submitted_data.name == retrieved_data.name
    assert submitted_data.lastname == retrieved_data.lastname
    assert submitted_data.pin == retrieved_data.pin

def test_program_should_raise_error_if_balance_is_insufficient_upon_withdraw():
    raise NotImplementedError

def test_program_should_raise_error_if_balance_is_insufficient_upon_paying_bills():
    raise NotImplementedError

def test_program_should_deduct_balance_after_withdraw():
    raise NotImplementedError

def test_program_should_correctly_increment_balance_upon_deposit():
    raise NotImplementedError

def test_program_should_correctly_retrieve_balance_from_database():
    raise NotImplementedError

def test_program_should_correctly_store_new_pin_after_changing_pin():
    raise NotImplementedError

def test_program_should_decuct_amount_after_pay_bills_function():
    raise NotImplementedError

def test_logout_should_delete_session_file():
    raise NotImplementedError

def test_clean_up():
    """dummy test to clean up created files"""
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        if os.path.exists("test.db"):
            os.remove("test.db")  #idk how to fix. DBAPI connection is not closed upon closing of session
    finally:
        make_config(ATM_DB, SESSION_FILE) #reverts settings to original
    #assert False

    # assert False
