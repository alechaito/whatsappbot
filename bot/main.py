from whats import Whatsapp 
from db import Database
import time

def main():
    #DB    = Database()
    Whats = Whatsapp()
    time.sleep(3)
    #Whats.update_messages()
    Whats.search_contact('ale')
    #print("oi")
    #DB.insert_contact({"user_id": '1', "number": '378273', "picture": 'test'})
    #DB.get_contact('378273')

main()