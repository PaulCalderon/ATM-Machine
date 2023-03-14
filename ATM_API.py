import sys
import os
import getopt
import configparser
from ATM_Repository import AtmCommands

CONFIG = "config.ini"

config_data = configparser.ConfigParser()
config_data.read(CONFIG)
config_option = config_data["options"]
for data in config_option: # gets config option for session_file
    if data == 'session_file':
        SESSION_FILE = config_option.get(data)


def check_input(command: list) -> str | None:  # should raise exception if error
    """parses and checks CLI input"""

    if os.path.exists(SESSION_FILE): #checks if session file exists
        command_list = ["login", "create", "help", "withdraw", "deposit", "check", "change", "pay", "logout"]
    else:
        command_list = ["login", "create", "help"]

    if command.lower() in command_list:
        return command.lower()
    else:
        error_string = f"{command} command is invalid"
        raise ValueError(error_string)

def command_parser(command: str, *flags: list | None) -> None:
    """has logic for selecting correct action based on parsed command"""
    if len(flags) > 0:
        flags = list(flags[0])
            #converts tuple to list. this is because of *flags to facilitate variable arguemnts
    match command:
        case 'login':
            try:
                if len(flags) != 4:
                    raise ValueError
                flag, args = getopt.getopt(flags, "u:p:")

            except:
                print("Syntax should be login -u <ID> -p <PIN> ")
                raise ValueError("Incorrect Flags")

            for option, argument in flag:
                if option == '-u':
                    account_id = argument
                elif option == '-p':
                    pin = argument
            AtmCommands.login(account_id, pin)
            print("Login Complete")

        case 'create': #need some workaround to create transaction entry for this
            try:
                if len(flags) != 6:
                    raise ValueError

                flag, args = getopt.getopt(flags, "n:l:p:")
            except:
                print("Syntax should be create -n <name> -l <last name> -p <PIN> ")
                raise ValueError("Incorrect Flags")

            for option, argument in flag:  #checks if PIN is 6 digits long and numeric
                if option == '-p':
                    if len(argument) != 6 or not argument.isnumeric():
                        raise ValueError("PIN should be 6 digits long")

            for option, argument in flag:
                if option == '-n':
                    name = argument
                elif option == '-l':
                    lastname = argument
                elif option == '-p':
                    pin = argument
            AtmCommands.create_account(name, lastname, pin)
            print("Account Created")

        case 'help':
            if os.path.exists(SESSION_FILE):

                print("Available Commands:")
                print("Create - Creates a new account - ATM_API.py create -n <FIRST NAME> -l <LAST NAME> -p <PIN>")
                print("Login - Login to your account and start a session - ATM_API.py login -u <ID> -p <PIN> ")
                print("Withdraw - Withdraw from available balance - ATM_API.py withdraw -a <AMOUNT>")
                print("Deposit - Deposits amount to balance - ATM_API.py deposit -a <AMOUNT>")
                print("Check - Checks available balance - ATM_API.py check")
                print("Change - Changes PIN - ATM_API.py change -p <NEW PIN>")
                print("Pay - Pay bills - ATM_API.py -a <AMOUNT>")
                print("History - Displays past transaction - ATM_API.py history")
                print("Logout - End current session - ATM_API.py logout")
                print("Help - Displays this help prompt  - ATM_API.py help")

            else:
                print("Available Commands:")
                print("Create - Creates a new account - ATM_API.py create -n <FIRST NAME> -l <LAST NAME> -p <PIN>")
                print("Login - Login to your account and start a session - ATM_API.py login -u <ID> -p <PIN> ")
                print("Help - Displays this help prompt  - ATM_API.py help")
                print("Login to display more commands")

        case 'withdraw': #need to be divisible by 100
            try:
                if len(flags) != 2:
                    raise ValueError
                flag, args = getopt.getopt(flags, "a:")
            except:
                raise ValueError("Incorrect Flags")

            for option, argument in flag:  
                #checks if withdrawl amount is divisible by 100 #Zero is a valid withdrawl amount

                if option == '-a':
                    if not argument.isnumeric():
                        raise ValueError("Withdraw amount should divisible by 100")

                    if int(argument) % 100 != 0:
                        raise ValueError("Withdraw amount should divisible by 100")
            
            for option, argument in flag:
                if option == '-a':
                    amount = argument
            account_id, old_balance, new_balance = AtmCommands.withdraw(amount)
            print("Would you like to print a receipt? (y/n)") 
            print("Not printing a receipt would display the previous transaction results on your screen")
            answer = input()
            if answer == ('y' or 'Y'):
                print("Receipt Printed")
            elif answer == ('n' or "N"):
                print("Account ID: ", account_id)
                print("Old Balance: ", old_balance)
                print("New Balance: ", new_balance)
            else:
                print("Invalid Input")
            
            
            
            
        case 'deposit':
            try:
                if len(flags) != 2:
                    raise ValueError
                flag, args = getopt.getopt(flags, "a:")
            except:
                raise ValueError("Incorrect Flags")
            
            for option, argument in flag:  
                #raise exception if amount is non numberic
                if option == '-a':
                    if not argument.isnumeric():
                        raise ValueError("Deposit amount is invalid")
                    amount = argument
            
            AtmCommands.deposit(amount)
            print("Successfully deposited: ",amount)

        case 'check':
            amount = AtmCommands.check_balance()
            #TODO complete display here 
            print("Current Balance: ", amount)

        case 'change':
            try:
                if len(flags) != 2:
                    raise ValueError
                flag, args = getopt.getopt(flags, "p:")
            except:
                raise ValueError("Incorrect Flags")
            
            for option, argument in flag:  #checks if PIN is 6 digits long and numeric
                if option == '-p':
                    if len(argument) != 6 or not argument.isnumeric():
                        raise ValueError("PIN should be 6 digits long")
            
            for option, argument in flag:
                if option == '-p':
                    pin = argument
            AtmCommands.change_pin(pin)
            print("Pin Changed")

        case 'pay':
            if len(flags) != 2:
                raise ValueError("Incorrect Flags")
            try:
                flag, args = getopt.getopt(flags, "a:")
            except:
                raise ValueError("Incorrect Flags")
            
            for option, argument in flag:  
                #raise exception if amount is non numberic
                if option == '-a':
                    if not argument.isnumeric():
                        raise ValueError("Amount is invalid")
                    amount = argument

            account_id, old_balance, new_balance = AtmCommands.pay_bills(amount)
            print("Would you like to print a receipt? (y/n)") 
            print("Not printing a receipt would display the previous transaction results on your screen")
            answer = input()
            if answer == ('y' or 'Y'):
                print("Receipt Printed")
            elif answer == ('n' or "N"):
                print("Account ID: ", account_id)
                print("Old Balance: ", old_balance)
                print("New Balance: ", new_balance)
            else:
                print("Invalid Input")

        case 'history':
            raise NotImplementedError
        
        case 'logout':
            AtmCommands.logout()
            print("Session Ended")

if __name__ == "__main__":
    parsed_command = check_input(sys.argv[1])
    command_parser(parsed_command, sys.argv[2:])
