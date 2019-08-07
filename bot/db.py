import pymysql


class Database:

    def __init__(self):
        self.db     = pymysql.connect("127.0.0.1","root","","whatsapp", cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.db.cursor() 
        print("[+] Conectado ao banco de dados...")

    def insert_contact(self, contact):
        query = ("INSERT INTO contacts (user_id, name, number, picture) VALUES (%s, %s, %s, %s)")
        self.cursor.execute(query, (
            contact['user_id'],
            contact['name'],
            contact['number'], 
            contact['picture']
        ))
        self.db.commit()
        print("[+] Novo contato inserido...")
    
    def insert_message(self, msg):
        query = ("INSERT INTO messages (contact_id, content, hour, status) VALUES (%s, %s, %s, 1)")
        self.cursor.execute(query, (msg['contact_id'], msg['content'], msg['hour']) )
        self.db.commit()
        print("[+] Nova mensagem inserido...")
    
    def get_messages_to_sent(self):
        query = ("SELECT * FROM messages WHERE status = 0")
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        if(data == None):
            print("[+] Nenhuma mensagem na fila...")
        return data
    
    #CHECK IF CONTACT EXISTS BY NUMBER
    # RETURN: 0 IF NOT EXIST / 1 IF EXIST
    def get_contact_by_number(self, number):
        query = ("SELECT * FROM contacts WHERE number = (%s)")
        self.cursor.execute(query, (number,))
        data = self.cursor.fetchone()
        if(data != None):
            print("[+] Contato ja existente, apenas vou atualizar...")
        return data
    
    def get_contact_by_id(self, idx):
        query = ("SELECT * FROM contacts WHERE id = (%s)")
        self.cursor.execute(query, (idx,))
        data = self.cursor.fetchone()
        if(data == None):
            print("[+] Nenhum contato existente com o ID: {}...".format(idx))
        return data
