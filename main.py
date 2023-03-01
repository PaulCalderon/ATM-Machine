import sys
import os
import getopt
import configparser

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
        command_list = ["login", "create", "help", "logout", "withdraw", "deposit", "check", "change", "pay"]
    else:
        command_list = ["login", "create", "help", "logout"]

    if command.lower() in command_list:
        return command.lower()
    else:
        raise ValueError("Command is invalid")

def command_parser(command: str, flags: list) -> None:
    """has logic for selecting correct action based on parsed command"""
    match command:

        case 'login':
            try:
                if len(flags) != 4:
                    raise ValueError
                flag, args = getopt.getopt(flags, "u:p:")
            except:
                print("Syntax should be login -u <ID> -p <PIN> ")
                raise ValueError("Incorrect Flags")

        case 'create':
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

        case 'help':
            pass

        case 'logout':
            pass

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

        case 'deposit':
            try:
                if len(flags) != 2:
                    raise ValueError
                flag, args = getopt.getopt(flags, "a:")
            except:
                raise ValueError("Incorrect Flags")
        case 'check':
            pass

        case 'change':
            try:
                if len(flags) != 2:
                    raise ValueError
                flag, args = getopt.getopt(flags, "p:")
            except:
                raise ValueError("Incorrect Flags")

        case 'pay':
            if len(flags) != 2:
                raise ValueError("Incorrect Flags")
            try:
                flag, args = getopt.getopt(flags, "a:")
            except:
                raise ValueError("Incorrect Flags")



if __name__ == "__main__":
    parsed_command = check_input(sys.argv[1])
    command_parser(parsed_command, sys.argv[2:])
