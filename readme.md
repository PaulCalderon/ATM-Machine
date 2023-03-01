# ATM API 

Developed in Python. This ATM API project works by accepting command line arguments and processing them to implement the commands as is provided by ATM machines. Two database tables are maintained by the API. The first one is a table of account holders with the PIN for the account. The second is a table of transactions performed on the local machine. A TDD approach was taken in developing this program.

The backend database is sqlite3 and interfaced via ORM using SQLalchemy.

## Installation
It is recommented to install the packages in a virtual environment
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the below packages.
The program was developed under the following versions:
>Python3 3.11.0
>SQLalchemy 2.04
>Pytest 7.2.1


```bash
pip install SQLAlchemy
pip install pytest
```

## Usage

**Call from CMD/Shell**
```
ATM_API.py <command>
```

### **Available commands**

>> **Create Account**
Name, Last Name, 6 Digit PIN
Accounts to be recorded under Accounts Table
Record account creation in Transactions table 

>> **Withdraw**
Input: ID and PIN then ask for amount to be withdrawn
Amount should be less than or equal to current and divisible by 100
Ask if receipt should be printed or to display current remaining balance 
Call withdraw_receipt() if ask to be printed

>> **Deposit** #implemented for the sake of being a test project #should be handled by different system
Input: ID and PIN then ask for amount to be deposited
Amount should be integer and divisible by 100
Ask if receipt should be printed or to display current remaining balance 
Call withdraw_receipt() if ask to be printed

>> **Check Balance**
To display current balance 
Change Pin 
Input: ID and PIN 
Ask for new PIN

>> **Pay Bills (Simplified)**
Ask for amount to be paid 
Amount should be less than or equal to current 
Ask if receipt should be printed or to display current remaining balance 
Call withdraw_receipt() if ask to be printed

>> **Help**
Displays help prompt
Help prompt is the available commands



##### Config File
The config file (config.ini) contains configurable options for the program
- User_Table = *name of table here*
- Transaction_Table = *name of table here*


##### **def withdraw_receipt()** - could be receipt only to accommodate withdraw and paybills
Output is 
>ID
Old Balance
New Balance
Date 


### Table Schema 
[![](https://mermaid.ink/img/pako:eNptUU1rwzAM_StGx9Bedwi7bIRB2QeF9Wgwmq1mYrFdbGcQsvz3OR8j6ah8kC29Jz1ZPWhvCErQDcZYMdYBrXQi24PWvnUpivuf_V6cArqIOrF3Mp8Jvg32M2m0Q6X8WaU1J4pjYIuhE8_UFStw6aAOlSiefCCu3T_EqbvQWGzTSGz4dqKzu8oX354NfjS0qVNhooU4zG4e4G_G_rao27Lf0NL6esGY1HXoTlVcc1JHdmvwERt0eqMCdmApWGSTv38SICF9Ui4EZb4aDF8SpBsyDtvk3zunoUyhpR20F5MHWrYF5RmbmKNkOPnwuuxzdMMvpPOXMQ?type=png)](https://mermaid.live/edit#pako:eNptUU1rwzAM_StGx9Bedwi7bIRB2QeF9Wgwmq1mYrFdbGcQsvz3OR8j6ah8kC29Jz1ZPWhvCErQDcZYMdYBrXQi24PWvnUpivuf_V6cArqIOrF3Mp8Jvg32M2m0Q6X8WaU1J4pjYIuhE8_UFStw6aAOlSiefCCu3T_EqbvQWGzTSGz4dqKzu8oX354NfjS0qVNhooU4zG4e4G_G_rao27Lf0NL6esGY1HXoTlVcc1JHdmvwERt0eqMCdmApWGSTv38SICF9Ui4EZb4aDF8SpBsyDtvk3zunoUyhpR20F5MHWrYF5RmbmKNkOPnwuuxzdMMvpPOXMQ)
##### Accounts
1. Account ID (Primary ID) #should actually be the account number but for the purposes of being a test project this is just the auto generated primary key of the database.
2. Name
3. Last Name
4. 6 Digit Pin
5. Balance

##### Transaction 
1. ID of transaction (Primary Key)
2. ID of User (Foreign Key)
3. Type of Transaction 
4. Amount in Transaction (If Applicable) (voidable)
5. Date 



