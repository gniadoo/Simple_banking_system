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
            self.number = number
            print("""1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
            while True:
                action = input(">")
                if action == str(0) or action == str(1) or action == str(2) or action == str(3) or action == str(4) or action == str(5):
                    break
                else:
                    print("Wrong action index")
            if action == str(1):
                print(" ")
                cur.execute("SELECT balance FROM card WHERE number = ?", (number,))
                print("Balance: {}".format(cur.fetchone()[0]))
                print(" ")
            elif action == str(2): #add income
                print(" ")
                print("Enter income: ")
                income = int(input("> "))
                cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?", (income,number,))
                con.commit()
                print("Income was added!")
                print(" ")
            elif action == str(3): #do transfer
                print(" ")
                self.transfer_money(number)
                print(" ")
            elif action == str(4): #close account
                print(" ")
                cur.execute("DELETE FROM card WHERE number = ?", (number,))
                con.commit()
                print("The account has been closed!")
                print(" ")
                break
            elif action == str(5):
                print(" ")
                print("You have successfully logged out!")
                print(" ")
                break
            elif action == str(0):
                print(" ")
                print("Bye!")
                print(" ")
                sys.exit()

    def transfer_money(self, number):
        #self.number = number
        print("Enter card number:")
        receiving_card = input(">")
        if int(receiving_card) == int(self.number):
            print("You can't transfer money to the same account!")
            return None
        check_sum = 0
        luhm_index = int(1)
        for digit in receiving_card:
            if luhm_index % 2 != 0:
                digit = int(digit) * 2
            if int(digit) > 9:
                digit = int(digit) - 9
            check_sum += int(digit)
            luhm_index += 1
        if check_sum % 10 != 0:
            print("Probably you made a mistake in the card number. Please try again!")
            return None
        cur.execute("SELECT COUNT (*) FROM card WHERE number = ?", (receiving_card,))
        is_number_taken = cur.fetchone()[0]
        if int(is_number_taken) == 0:
            print("Such a card does not exist.")
            return None
        print("Enter how much money you want to transfer:")
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


#4000004700836582
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




