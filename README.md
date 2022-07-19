# BankingApp
Banking app was created as a CS50 final project. Users can create, update, and rename different types of accounts. Functionality includes transferring funds, depositing, and withdrawing. 

# Personal Finance App
### Description:
The personal finance app is designed to be a way that users can keep track of income and expenses in an organized manner and see their overall profile. It is designed to operate like a banking app and also a personal finance app. Each user receives a checking and saving account to start their profile, but can add and remove accounts to their liking to plan for specific life events such as a vacation, a home, a vehicle, college, etc.

The finance app came into being from a discussion with my wife regarding finances and tracking finances and trying to decide how to save for different life events. This inspired me to try and create a system that my wife and I could use to manage our own finances and find some financial peace.

The app consists of login and register pages. Once logged in, users have the option to log transactions in their current checking and saving accounts. Users can transfer funds between accounts as well if they have need. If they want to create a page specifically for an event, they can create an account that will be added to the accounts list so they can transfer or transact money to that account and monitor the total amount. If a life event has been achieved, the user can delete the special account. One condition to deletion or transfers, the account balance must be zero in order to delete an account and the transfer cannot deplete another account below zero.

This project uses a similar flask environment from the week 9 finance assignment. The basic CSS design is very similar to that assignment, however, most of the logic and functions are my own. In the finance app I also use python, HTML, Bootstrap CSS, Jinja, and SQL.

#### project.db
I created three tables in the database project.db: users, accounts, account_type. The users table allows for new and old users to store usernames, emails, and passwords that can allow them to login and customize their accounts based on what they'd like to do. This is done in the accounts and account_type tables. The accounts table stores information concerning each account the user possess and also allows for deposits, withdrawals, and transfers to be made at will by the user. The account_type table is a table where each user stores both their standard checking and saving account as well as any customized accounts they have created on their own.

#### templates folder
The templates folder contains 10 different HTML documents for the different pages on the website. From top to bottom:
- delete.html
- error.html
- history.html
- index.html
- layout.html
- login.html
- new_account.html
- register.html
- transfer.html
- update.html

#### delete.html
A very simple HTML document containing Jinja functions to allow a user to select an account and then press a button to delete the said account. This document pairs with the delete() function in app.py which selects all user accounts, verifies they are at zero, then allows the user to select and delete the account.

#### error.html
A simple, short HTML document that uses the error() function from extras.py to pass in a message and error code and return the user to a page that displays the error and message and allows them to return to the index page which displays their accounts.

#### history.html
Uses a table and Jinja loops to loop through a users accounts, match and sum the accounts with their amounts, and display them on the history page in such a way that they are outlined with their timestamp, descriptions, action type, account names, and amounts.

#### index.html
Operates very mucht the same as history.html. Their is an HTML table working with Jinja loops to display the current total balances of all accounts in the user's database.

#### layout.html
The base HTML document into which all the other templates fit. It uses Jinja logic to confirm if a user is logged in or not by checking the session["user"] to determine what information to show. If the user is not logged in, it will display the login.html page, or the register.html page. If the user is logged in, it will allow the user access to the index, transaction, transfer, history, create, and delete pages. It will also give the user the ability to logout.

#### login.html
Determines if a user is in the database and then checks the password hash to determine if the passwords match. If they do not, it returns them an error page which will redirect them to the login page again. On this page, their is the option to register for an account which the user can do.

#### register.html
Allows a user to input a username, email, and password- which is then hashed in the database. The register() funcion in app.py checks to see if the username is already in the database, and if it is not, it redirects user to the login page. If the username is already in the database, it gives the user an error message.

#### new_account.html
Uses a Jinja loop to select one of two account types the user can choose: either checking or saving. It then allows a text input for the user to name their account for easier understanding and readability. Once a user submits the new account, index.html will show the new account with a $0 balance. But the user will have the ability to transact or transfer funds into the new account as they will.

#### transfer.html
Also uses a Jinja loop to show all the users current accounts and gives the user the ability to select a transfer from and a transfer to account. Logic in app.py in the transfer() function checks to see if the transfer from account contains enough funds and an error message is shown. Else, the transfer proceeds and the user is shows index.html with the updated balances for both accounts. history.html also will show the transfer from and the transfer to accounts so the user can track from where funds have moved.

### update.html
This document contains a form for the user to choose an account (using a Jinja loop), select an amount to transact, select a transaction type (a Jinja loop again), and write a description concerning the transaction. Logic checks to ensure all fields are filled in and then checks- if the transaction is a withdrawal- whether the account contains enough funds. If there are not enough funds, the user is given another error mesage. If there are a enough funds or the transaction type is a deposit, the accounts table is updated and the user is redirected to index.html where the updated amounts are shown.

#### app.py
This is the motherload document containing most of the functions used in this project. Each page has a function which matches the pages title for ease of understanding and readability. Towards the top, there are two Python arrays containing transaction types and account types which are included in several of the html templates.

#### extras.py
This file contains only three functions which are used regularly throughout the project and I thought for separation of functions and ease of understanding, it made sense to separate these three functions. There are the login and usd function which I borrowed from Finance and there is an error() function which accepts a message and error code and shows the user an error page containing these two elements.

I genuinely had fun making this semi-real world project. I find it fascinating to see just how much usefulness programs can have in so many varied situations. This course- and this project- inspired me to go back to school for a degree in Computer Science.
