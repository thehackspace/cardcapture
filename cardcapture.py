#!/usr/bin/python3

import sqlite3
import time
import re
import os

def validate(card):
    if re.search('^\d\d\d\d\d\d\d\d$', card):
        return True
    else:
        return False

def lookup(db, card):
    cur = db.cursor()
    cur.execute("SELECT name FROM cards WHERE card=:card", {"card": card})
    row = cur.fetchone()
    try:
        return row[0]
    except (NameError, TypeError):
        return None

def clear():
    # It would be nice to do this from within Python, but
    # correctly handling all the different terminal types
    # isn't trivial
    os.system("clear")

def store(db, card, name):
    db.execute("INSERT INTO cards ('card', 'name') VALUES(?, ?)", [card, name])
    db.commit()

def main():
    db = sqlite3.connect('cards.db')
    db.execute("CREATE TABLE IF NOT EXISTS cards (card TEXT PRIMARY KEY, name TEXT NOT NULL)")

    while True:
        clear()
        card = input("Please scan a card: ")
        if not validate(card):
            print("Card not valid")
            continue
        name = lookup(db, card)
        if name is not None:
            print("Hello {}, your card is already registered".format(name))
            time.sleep(5)
        else:
            count = 3
            while count > 0:
                count -= 1
                name = input("Please enter your name: ")
                confirm = input("Is '{}' correct? [Y/N] ".format(name))
                if (confirm == 'Y') or (confirm == 'y'):
                    store(db, card, name)
                    print("Your details have been stored, thank you")
                    time.sleep(5)
                    break


if __name__ == "__main__":
    main()
