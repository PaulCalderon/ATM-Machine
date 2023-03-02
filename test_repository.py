import pytest
from sqlalchemy.orm import Session, DeclarativeBase
from io import StringIO
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

from ATM_Repository import AtmCommands, TransactionsDatabase, table_init
class TestAtmCommands:

    def test_program_should_create_entry_upon_calling_the_function(self):
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

    def test_program_should_have_details_in_login_in_the_session_file(self):
        account_id = "1"
        pin = "123456"

        AtmCommands.login(account_id, pin)

        config_data.read(SESSION_FILE)
        option = config_data["account"]
        for data in option:
            if data == 'id':
                active_id = option.get(data)
        assert active_id == '1'
            
    def test_program_should_have_raise_error_if_login_fails(self):
        account_id = "1"
        incorrect_pin = "123452"
        with pytest.raises(ValueError, match="PIN is incorrect"):    
            AtmCommands.login(account_id, incorrect_pin)

    def test_program_should_delete_session_upon_new_login_and_create_new_session(self):
            #use create account for new account and login
        account_id = '2'
        name = 'Dannah'
        lastname = 'Hintay'
        pin = "654321"
        AtmCommands.create_account(name, lastname, pin)
        AtmCommands.login(account_id, pin)

        config_data.read(SESSION_FILE)
        option = config_data["account"]
        for data in option:
            if data == 'id':
                active_id = option.get(data)


        assert active_id == '2'

        AtmCommands.login('1', '123456') # returns active session to account_id 1

    def test_program_should_correctly_increment_balance_upon_deposit(self): #active session is account_id 1 from here
        deposit_amount = '10000'
        AtmCommands.deposit(deposit_amount)
        engine, Base, Accounts, Transactions = table_init()
        with Session(engine) as session:
            retrieved_data = session.get(Accounts, 1)
        
        assert deposit_amount == retrieved_data.balance

    def test_program_should_raise_error_if_balance_is_insufficient_upon_withdraw(self):
        withdraw_amount = '100000'
        with pytest.raises(ValueError, match="Insufficient Balance"):    
            AtmCommands.withdraw(withdraw_amount)

    def test_program_should_deduct_balance_after_withdraw(self):
        withdraw_amount = '1000'
        #monkeypatch.setattr('builtins.input', lambda _: "y") #monkeypatch to mock entering input
        AtmCommands.withdraw(withdraw_amount)
        engine, Base, Accounts, Transactions = table_init()
        
        with Session(engine) as session:

            retrieved_data = session.get(Accounts, 1)

        assert retrieved_data.balance == '9000'
    def test_program_should_raise_error_if_balance_is_insufficient_upon_paying_bills(self):
        pay_amount = '10000'
        with pytest.raises(ValueError, match="Insufficient Balance"):
            AtmCommands.pay_bills(pay_amount)

    def test_program_should_deduct_balance_after_pay_bills(self):
        withdraw_amount = '1000'
        #monkeypatch.setattr('builtins.input', lambda _: "y") #monkeypatch to mock entering input
        AtmCommands.withdraw(withdraw_amount)
        engine, Base, Accounts, Transactions = table_init()
        
        with Session(engine) as session:
            retrieved_data = session.get(Accounts, 1)
        assert retrieved_data.balance == '8000'

    def test_program_should_return_transaction_details_during_withdraw_or_pay(self):
        withdraw_amount = 1000
        id, old_balance, new_balance = AtmCommands.withdraw(withdraw_amount)
        assert id == '1'
        assert old_balance == '8000'
        assert new_balance == '7000'

    def test_program_should_correctly_retrieve_balance_from_database(self):
        current_balance = AtmCommands.check_balance()

        assert current_balance == '7000'


    def test_program_should_correctly_store_new_pin_after_changing_pin(self):
        pin = '567890'
        AtmCommands.change_pin(pin)
        engine, Base, Accounts, Transactions = table_init()
        with Session(engine) as session:
            retrieved_data = session.get(Accounts, 1)
            new_pin = retrieved_data.pin

        assert new_pin == '567890'

    def test_logout_should_delete_session_file(self):
        before_delete: bool = os.path.exists(SESSION_FILE)
        AtmCommands.logout()
        after_delete: bool = os.path.exists(SESSION_FILE)
        assert before_delete #session exists before deleting
        assert not after_delete #session is deleted after calling logout

class TestTransactionDatabase:

    def test_check_if_transactions_are_recorded_succesfully(self):
        transaction_type = "deposit"
        account_id = '2'
        amount = '1000'


        TransactionsDatabase.record_transaction(transaction_type, account_id, amount)
    
    def test_check_if_transactions_are_recorded_correctly(self):
        #test past transactions if they were recorded
        engine, Base, Accounts, Transactions = table_init()
        with Session(engine) as session:
            first_transaction = session.get(Transactions, 1 )
        assert first_transaction.account_id == 1
        assert first_transaction.type_of_transaction == 'Create Account'
        
        
    


def test_clean_up():
    """dummy test to clean up created files"""
    try:
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
            
        if os.path.exists("test.db"):
            os.remove("test.db")  #idk how to fix. DBAPI connection is not closed upon closing of session #fixed by changing setting of SQLalchemy to nullpool
            
    finally:
        make_config(ATM_DB, SESSION_FILE) #reverts settings to original
    #assert False

        # assert False
