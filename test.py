import time
from webwhatsapi import WhatsAPIDriver
from webwhatsapi.objects.message import Message
import os
import sys

driver = WhatsAPIDriver()
print("Waiting for QR")
driver.wait_for_login()

print("Bot started")

while True:
    time.sleep(3)
    print('Checking for more messages')
    print(len(driver.get_unread()))