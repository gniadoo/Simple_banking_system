import sys
import sqlite3
from random import randint

con = sqlite3.connect("card.s3db")
cur = con.cursor()
cur.execute("DROP TABLE card")
cur.execute("CREATE TABLE card("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "number TEXT,"
            "pin TEXT,"
            "balance INTEGER DEFAULT 0)")
con.commit()

class Card():
    def __init__(self):
        self.number = None
        self.pin = ""
        self.balance = 0

    def create_card(self):
        print("Your card has been created")
        print("Your card number:")
        while True:
            can = ""
            for i in range(9):
                can += str(randint(0, 9))
            check_sum = 0
            luhm_index = int(1)
            for digit in str(400000) + can:
                if luhm_index % 2 != 0:
                    digit = int(digit) * 2
                if int(digit) > 9:
                    digit = int(digit) - 9
                check_sum += int(digit)
                luhm_index += 1
            last_digit = 10 - (check_sum % 10)
            if last_digit == 10:
                last_digit = 0
            self.number = str(400000) + can + str(last_digit)

            cur.execute("SELECT COUNT (*) FROM card WHERE number = ?", (self.number,))
            is_number_taken = cur.fetchone()[0]
            if is_number_taken == 1:
                continue
            else:
                break

        print(self.number)
        for i in range(4):
            self.pin += str(randint(0, 9))
        print("Your card number:")
        print(self.pin)
        cur.execute("INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)", (self.number, self.pin, self.balance))
        con.commit()

    def log_in_function(self, number):
        while True:
            print("""1. Balance
2. Log out
0. Exit""")
            while True:
                action = input(">")
                if action == str(0) or action == str(1) or action == str(2):
                    break
                else:
                    print("Wrong action index")
            if action == str(1):
                print(" ")
                cur.execute("SELECT balance FROM card WHERE number = ?", (number,))
                print("Balance: {}".format(cur.fetchone()[0]))
                print(" ")
            elif action == str(2):
                print(" ")
                print("You have successfully logged out!")
                print(" ")
                break
            elif action == str(0):
                print(" ")
                print("Bye!")
                print(" ")
                sys.exit()

while True:
    print("""1. Create an account
2. Log into account
0. Exit""")
    while True:
        action = input(">")
        if action == str(0) or action == str(1) or action == str(2):
            break
        else:
            print("Wrong action index")

    if action == str(1):
        print(" ")
        new_card = Card()
        new_card.create_card()
        print(" ")

    elif action == str(2):
        cur.execute("SELECT COUNT (*) FROM card")
        numbers = cur.fetchone()[0]
        if not numbers:
            print(" ")
            print("No account to log in")
            print(" ")
        else:
            print(" ")
            print("Enter your card number:")
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
                    new_card.log_in_function(card_number)
                else:
                    print(" ")
                    print("Wrong card number or PIN!")
                    print(" ")
            except ValueError:
                print(" ")
                print("Wrong card number or PIN!")
                print(" ")

    elif action == str(0):
        break
print(" ")
print("Bye")
print(" ")


