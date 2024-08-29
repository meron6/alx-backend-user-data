#!/usr/bin/env python3
"""
Main file
"""

from filtered_logger import filter_datum
from encrypt_password import hash_password

fields = ["password", "date_of_birth"]
messages = [
    "name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;",
    "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"
]

for message in messages:
    print(filter_datum(fields, 'xxx', message, ';'))

password = "MyAmazingPassw0rd"
print(hash_password(password))
print(hash_password(password))
