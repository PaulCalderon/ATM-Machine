import configparser
import os

CONFIG = "config.ini"

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.add_section("options")
    config.set("options", "User_Table", "User.db")
    config.set("options", "Transaction_Table", "Transaction.db")
    config.set("options", "Session_file", "session.txt")

    if os.path.exists(CONFIG):
        os.remove(CONFIG)

    with open(CONFIG, 'w') as example:
        config.write(example)
