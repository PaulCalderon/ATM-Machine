import pytest
import os
import configparser
from main import check_input, command_parser

CONFIG = "config.ini"

config_data = configparser.ConfigParser()
config_data.read(CONFIG)
option = config_data["options"]
for data in option: # gets config option for session_file
    if data == 'session_file':
        SESSION_FILE = option.get(data)


class TestCLIHandlingOfMain:
    """Class for grouping tests"""
    def test_program_should_raise_error_if_command_is_invalid(self):
        """ To be implemented by creating a method in main to check if command is valid"""
        with pytest.raises(ValueError, match="Command is invalid") as exc_info:
            check_input("")
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "Command is invalid"

    def test_program_commands_should_be_case_insensitive(self):
        """ Checking method should be case insentive and not raise error"""
        assert check_input("CREATE")
        assert check_input("LOgin")
        assert check_input("HELp")
        assert check_input("logout")

    def test_program_should_accept_all_commands_as_valid_if_session_file_exists(self):
        """All commands should be valid"""
        with open(SESSION_FILE, "w") as file:  #used to create session_file to simulate open session
            pass
        assert check_input("Check")
        assert check_input("Pay")
        assert check_input("deposit")
        assert check_input("withdraw")
        assert check_input("Change")

    def test_program_should_only_accept_login_or_create_account_or_help_or_logout_commands_when_there_is_no_active_session(self):
        """Will check for prescence of session file before accepting any other commands"""
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)

        with pytest.raises(ValueError, match="Command is invalid") as exc_info:
            check_input("Check Balance")
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "Command is invalid"

    def test_program_should_raise_value_error_if_flags_are_invalid_create(self):
        """assumes that check_input is correct"""
        command = check_input("Create")

        with pytest.raises(ValueError, match="Incorrect Flags") as exc_info:
            command_parser(command, [])
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "Incorrect Flags"

        with pytest.raises(ValueError, match="Incorrect Flags") as exc_info:
            command_parser(command, ['-u','any','-l','lastname','-p','123456'])
                #-u is wrong input. main should raise exception
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "Incorrect Flags"

    def test_program_should_raise_value_error_if_flags_are_invalid_login(self):
        """assumes that check_input is correct"""
        command = check_input("login")

        with pytest.raises(ValueError, match="Incorrect Flags") as exc_info:
            command_parser(command, [])
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "Incorrect Flags"

        with pytest.raises(ValueError, match="Incorrect Flags") as exc_info:
            command_parser(command, ['-a','any','-l','lastname'])
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "Incorrect Flags"

    def test_program_should_raise_value_error_if_flags_are_invalid_withdraw(self):
        """assumes that check_input is correct"""

        with open(SESSION_FILE, "w") as file:  #used to create session_file to simulate open session
            pass
        command = check_input("withdraw")

        with pytest.raises(ValueError, match="Incorrect Flags") as exc_info:
            command_parser(command, [])
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "Incorrect Flags"

        with pytest.raises(ValueError, match="Incorrect Flags") as exc_info:
            command_parser(command, ['-x','any'])
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "Incorrect Flags"

    def test_program_should_raise_value_error_if_flags_are_invalid_deposit(self):
        """assumes that check_input is correct"""

        with open(SESSION_FILE, "w") as file:  #used to create session_file to simulate open session
            pass
        command = check_input("deposit")

        with pytest.raises(ValueError, match="Incorrect Flags") as exc_info:
            command_parser(command, [])
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "Incorrect Flags"

        with pytest.raises(ValueError, match="Incorrect Flags") as exc_info:
            command_parser(command, ['-x','any'])
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "Incorrect Flags"

    def test_program_should_raise_value_error_if_flags_are_invalid_change_pin(self):
        """assumes that check_input is correct"""

        with open(SESSION_FILE, "w") as file:  #used to create session_file to simulate open session
            pass
        command = check_input("change")

        with pytest.raises(ValueError, match="Incorrect Flags") as exc_info:
            command_parser(command, [])
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "Incorrect Flags"

        with pytest.raises(ValueError, match="Incorrect Flags") as exc_info:
            command_parser(command, ['-x','any']) 
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "Incorrect Flags"

    def test_program_should_raise_value_error_if_flags_are_invalid_pay_bills(self):
        """assumes that check_input is correct"""
        with open(SESSION_FILE, "w") as file:  #used to create session_file to simulate open session
            pass

        command = check_input("pay")
        with pytest.raises(ValueError, match="Incorrect Flags") as exc_info:
            command_parser(command, [])
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "Incorrect Flags"

        with pytest.raises(ValueError, match="Incorrect Flags") as exc_info:
            command_parser(command, ['-x','any'])
        assert exc_info.type is ValueError
        assert exc_info.value.args[0] == "Incorrect Flags"

    def test_program_should_raise_value_error_if_PIN_in_create_account_is_not_6_and_not_all_numeric(self):
        """Checks if pin is valid"""
        command = check_input("create")
        with pytest.raises(ValueError, match="PIN should be 6 digits long") as exc_info:
            command_parser(command, ['-n', 'first', '-l', 'last', '-p','12345'])
            #PIN is only 5 digits
        with pytest.raises(ValueError, match="PIN should be 6 digits long") as exc_info:
            command_parser(command, ['-n', 'first', '-l', 'last', '-p','asdsad'])
            #PIN isn't only numeric characters

    def test_program_should_raise_value_error_if_withdraw_amount_is_not_divisible_by_100(self):
        """Exception raised when not divisible by 100 or invalid"""
        command = check_input("withdraw")
        with pytest.raises(ValueError, match="Withdraw amount should divisible by 100"):
            command_parser(command, ['-a', '2304']) #amount is not divisible by 100
        with pytest.raises(ValueError, match="Withdraw amount should divisible by 100"):
            command_parser(command, ['-a', 'werwer']) #amount should be numbers only

    def test_clean_up(self):
        """dummy test to clean up created files"""
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
