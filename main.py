import sys
import sqlite3
from random import randint

# Creating database
try:
    con = sqlite3.connect("card.s3db")
except sqlite3.Error as error:
    print('Failed to connect SQLite: ', error)
    sys.exit()

cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS card("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "number TEXT,"
            "pin TEXT,"
            "balance INTEGER DEFAULT 0)")
con.commit()
print('DB has been created')


def card_luhn_generator():  # Creating card number with luhn algorithm
    can = ""
    for i in range(9):
        can += str(randint(0, 9))
    check_sum = 0
    luhn_index = int(1)
    for digit in str(400000) + can:
        if luhn_index % 2 != 0:
            digit = int(digit) * 2
        if int(digit) > 9:
            digit = int(digit) - 9
        check_sum += int(digit)
        luhn_index += 1
    last_digit = 10 - (check_sum % 10)
    if last_digit == 10:
        last_digit = 0
    return str(400000) + can + str(last_digit)


def is_number_valid_with_luhn(number):  # Checking if card is valid with luhn algorithm
    check_sum = 0
    luhn_index = int(1)
    for digit in number:
        if luhn_index % 2 != 0:
            digit = int(digit) * 2
        if int(digit) > 9:
            digit = int(digit) - 9
        check_sum += int(digit)
        luhn_index += 1
    return check_sum % 10


def log_into_account(card):  # Defining whole log in process
    print(" ")
    print("Enter your card number:")
    try:
        card_number = int(input(">"))
        print("Enter your PIN:")
        card_pin = int(input(">"))
        try:
            cur.execute("SELECT COUNT (*) FROM card WHERE number = ? AND pin = ?", (int(card_number), int(card_pin),))
            is_data_valid = cur.fetchone()[0]
            if is_data_valid:
                print(" ")
                print("You have successfully logged in!")
                print(" ")
                card.user_panel(card_number)
            else:
                print(" ")
                print("Wrong card number or PIN!")
                print(" ")
        except ValueError:
            print(" ")
            print("Wrong card number or PIN!")
            print(" ")
    except ValueError:
        print(" ")
        print("Wrong card number/PIN type!\n")


class Card:  # Defining card class
    def __init__(self):
        self.number = None
        self.pin = ""
        self.balance = 0

    def create_card(self):
        print("Your card has been created")
        print("Your card number:")
        while True:
            self.number = card_luhn_generator()
            # Checking if card with this number already exists in database
            cur.execute("SELECT COUNT (*) FROM card WHERE number = ?", (self.number,))
            is_number_taken = cur.fetchone()[0]
            if is_number_taken == 1:
                continue
            else:
                break
        print(self.number)
        for i in range(4):
            self.pin += str(randint(0, 9))
        print("Your card PIN:")
        print(self.pin)
        # Inserting card data to database
        cur.execute("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)", (self.number, self.pin, self.balance))
        con.commit()

    # Defining whole functionality after log in
    def user_panel(self, number):
        while True:
            self.number = number
            print("1. Balance\n"
                  "2. Add income\n"
                  "3. Do transfer\n"
                  "4. Close account\n"
                  "5. Log out\n"
                  "0. Exit\n")
            while True:
                user_action = input(">")
                if user_action == str(0) or user_action == str(1) or user_action == str(2) or\
                   user_action == str(3) or user_action == str(4) or user_action == str(5):
                    break
                else:
                    print("Wrong action index")
            if user_action == str(1):
                print(" ")
                cur.execute("SELECT balance FROM card WHERE number = ?", (number,))
                print("Balance: {}".format(cur.fetchone()[0]))
                print(" ")
            elif user_action == str(2):
                print(" ")
                print("Enter income: ")
                try:
                    income = int(input("> "))
                    cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (income, number,))
                    con.commit()
                    print(" ")
                    print("Income was added!\n")
                except ValueError:
                    print(" ")
                    print("Wrong amount!\n")

            elif user_action == str(3):
                print(" ")
                self.transfer_money(number)
                print(" ")
            elif user_action == str(4):
                print(" ")
                cur.execute("DELETE FROM card WHERE number = ?", (number,))
                con.commit()
                print("The account has been closed!")
                print(" ")
                break
            elif user_action == str(5):
                print(" ")
                print("You have successfully logged out!")
                print(" ")
                break
            elif user_action == str(0):
                print(" ")
                print("Bye!")
                sys.exit()

    # Defining whole money transfer process
    def transfer_money(self, number):
        print("Enter card number:")
        receiving_card = input(">")
        try:
            if int(receiving_card) == int(self.number):
                print("You can't transfer money to the same account!")
                return None
            if is_number_valid_with_luhn(receiving_card):
                print("Probably you made a mistake in the card number. Please try again!")
                return None
            cur.execute("SELECT COUNT (*) FROM card WHERE number = ?", (receiving_card,))
            is_number_taken = cur.fetchone()[0]
            if int(is_number_taken) == 0:
                print("Such a card does not exist.")
                return None
        except ValueError:
            print("Incorrect account type number!")
            return None

        print("Enter how much money you want to transfer:")
        try:
            transfer_money = int(input(">"))
            cur.execute("SELECT balance FROM card WHERE number = ?", (number,))
            if transfer_money > int(cur.fetchone()[0]):
                print("Not enough money!")
                return None
            cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (transfer_money, receiving_card,))
            con.commit()
            cur.execute("UPDATE card SET balance = balance - ? WHERE number = ?", (transfer_money, self.number,))
            con.commit()
            print("Success!")
        except ValueError:
            print("Incorrect money type!")

# Main panel


while True:
    print("1. Create an account\n2. Log into account\n0. Exit")
    while True:
        action = input(">")
        if action == str(0) or action == str(1) or action == str(2):
            break
        else:
            print("Wrong action index")
    new_card = Card()
    if action == str(1):
        print(" ")
        new_card.create_card()
        print(" ")
    elif action == str(2):
        cur.execute("SELECT COUNT (*) FROM card")
        card_numbers_in_database = cur.fetchone()[0]
        if not card_numbers_in_database:
            print(" ")
            print("No account to log in")
            print(" ")
        else:
            log_into_account(new_card)
    elif action == str(0):
        break
print(" ")
print("Bye")
print(" ")
cur.close()
