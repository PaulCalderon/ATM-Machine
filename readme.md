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


```
pip install SQLAlchemy
pip install pytest
```


## Usage

**Call from CMD/Shell**
```
ATM_API.py <command> <flags>
```
*Commands are case-insensitve**

Only Login, Create Account, Help and Logout are available if no session file is found

Main handles all the logic for verifying valid inputs and interacting with user
ATM_Repository handles all database transactions and return data to Main
ATM_repository assumes that all received values are valid for querying

### **Available commands**
> **Login**
Input: ID and 6 Digit Pin
Creates a session file upon sucessful login



> **Create** Account
Input: Name, Last Name, 6 Digit PIN
Accounts to be recorded under Accounts Table
Record account creation in Transactions table 

> **Withdraw**
There should be an active session
Input: Amount to be withdrawn
Amount should be less than or equal to current and divisible by 100
Ask if receipt should be printed or to display current remaining balance 
Call withdraw_receipt() if ask to be printed

> **Deposit** #implemented for the sake of being a test project #should be handled by different system
There should be an active session
Input Amount to be deposited
Amount should be integer and divisible by 100
Ask if receipt should be printed or to display current remaining balance 
Call withdraw_receipt() if ask to be printed

> **Check** Balance
There should be an active session
To display current balance 

> **Change** Pin
There should be an active session
Input: New PIN
Updates PIN in database

> **Pay** Bills (Simplified)
There should be an active session
Input: Amount to be paid 
Amount should be less than or equal to current 
Ask if receipt should be printed or to display current remaining balance 
Call withdraw_receipt() if ask to be printed

> Check **History**
There should be an active session
Retrieves and displays past transactions of active session

> **Help**
Displays help prompt
Help prompt is the available commands.
Displayed commands will changed based on the presence of session file

> **Logout**
If existing, session file will be deleted



##### Config File
The config file (config.ini) contains configurable options for the program
- User_Table = *name of table here* | defaults to *User*
- Transaction_Table = *name of table here* | defaults to *Transaction*
- Session_file = *name of text file containing info about session* (should be encrypted in production I think) | defaults to *session.txt*


##### **def receipt_output()** - could be receipt only to accommodate withdraw and paybills
Output is 
>ID
Old Balance
New Balance
Date 


### Table Schema 
[![](https://mermaid.ink/img/pako:eNptUcFqwzAM_RWjY2h_IOzSEgahWym0R4PRbLUzi-1iO4WQ5d_nNClOR-WDLOn5PcnqQTpFUIJsMIRK48Wj4ZYl20jpWhsDe_tdr9nJow0oo3aWp3OHL5P99Gi0uhLuLGKuseLgtUHfsR11RQaeuiuN0AUNy9WNGeWFtk_14ua0wq-GFjxzp6KuWPHuPOmL_adUYaSZepjcNMBjxv412eu292goRx8YonhOHep9DrbYoJULdViBIW9Qq_Ttd2EO8ZsSAZTpqtD_cOB2SDhsozt2VkIZfUsraK8qDTJvCcozNiFlSeno_Oe8x9ENf_-6lAw?type=png)](https://mermaid.live/edit#pako:eNptUcFqwzAM_RWjY2h_IOzSEgahWym0R4PRbLUzi-1iO4WQ5d_nNClOR-WDLOn5PcnqQTpFUIJsMIRK48Wj4ZYl20jpWhsDe_tdr9nJow0oo3aWp3OHL5P99Gi0uhLuLGKuseLgtUHfsR11RQaeuiuN0AUNy9WNGeWFtk_14ua0wq-GFjxzp6KuWPHuPOmL_adUYaSZepjcNMBjxv412eu292goRx8YonhOHep9DrbYoJULdViBIW9Qq_Ttd2EO8ZsSAZTpqtD_cOB2SDhsozt2VkIZfUsraK8qDTJvCcozNiFlSeno_Oe8x9ENf_-6lAw)
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

## Testing
The tests were developed using pytest and included in the program files. 
The package **pytest** should be installed in the environment
The tests can be run by entering in the console:
```
pytest
```
while in the root directory of the program
Running the tests will close active sessions, if any
The following files contain the testing codes
> test_repository.py
> test_main.py
