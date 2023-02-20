# Decrypt and display data from HidePass Password Manager - com.sisomobile.android.passwordsafe
# V1:
# 2023-02-18 https://github.com/Magpol/
#
#Ex output:
#
#user@s0-Smaz:~/passwordsafe$ python3 decrypt.py -p test -db my_password.db
#seq, group_name, title, id, password, url, note, memo_title_01, memo_content_01, memo_title_02, memo_content_02, memo_title_03, memo_content_03, memo_title_04, memo_content_04, memo_title_05, memo_content_05, memo_title_06, memo_content_06, memo_title_07, memo_content_07, memo_title_08, memo_content_08, memo_title_09, memo_content_09, memo_title_10, memo_content_10, memo_count, is_favorite
#1, folder1, title1, id1, password1, homepage1, , note1, , , , , , , , , , , , , , , , , , , , 2, 0, 
#2, folder1, title2, id2, password2, homepage2, , , , , , , , , , , , , , , , , , , , , , 0, 0, 
#3, folder2, title3, id3, password3, homepage3, , , , , , , , , , , , , , , , , , , , , , 0, 0,
#


from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import hashlib
import binascii
import sqlite3
import re
import argparse

class AESCipher:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    def encrypt(self, data):
        self.cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return b64encode(self.cipher.encrypt(pad(data.encode('utf-8'), 
            AES.block_size)))

    def decrypt(self, data):
        data = b64decode(data)
        self.cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        return unpad(self.cipher.decrypt(data), AES.block_size)          

def isBase64(s):
    if isinstance(s, str) and len(s) > 4:
        s = ''.join([s.strip() for s in s.split("\n")])
        try:
            enc = b64encode(b64decode(s)).strip()
            return True
        except TypeError:
            return False
    else:
        return False

def generateAppKey(hashedPassword):
    hashedciphertext = AESCipher(hashedPassword[:16].encode('utf-8'),hashedPassword[:16].encode('utf-8')).encrypt("sisomobile").decode('utf-8')
    return bytes(hashedPassword[8:16] + hashedciphertext[1:17] + hashedPassword[0:8],'utf-8')

def main():
    try:
        parser = argparse.ArgumentParser(description = "Decrypt and display data from HidePass Password Manager - com.sisomobile.android.passwordsafe.\n\nThe data is stored /data/data/com.sisomobile.android.passwordsafe/databases/my_password.db\nThe password is a sha-256 hash that is found in /data/data/com.sisomobile.android.passwordsafe/files/com.sisomobile.android.passwordsafe_preferences.xml\nThe hash needs to be cracked and the plaintext password must be supplied to succesfully decrypt the information.",formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument("-p", "--password", metavar="PASSWORD",required=True, help = "Password")
        parser.add_argument("-db", "--database", metavar="DATABASE",required=True, help = "Path to my_password.db")

        args = parser.parse_args()

        hashedPassword = hashlib.sha256((args.password).encode('utf-8')).hexdigest()
        sisoKey = generateAppKey(hashedPassword)

        tableName = "safe"
        connection = sqlite3.connect(args.database)
        cursor = connection.cursor()

        cursor.execute("SELECT group_concat(name, ', ') FROM pragma_table_info(?)", (tableName,))
        headers = cursor.fetchone()
        print(*headers)
        rows = cursor.execute(f"select * from {tableName}")
        for row in rows:
            for item in row:
                if isBase64(item):
                    print(AESCipher(sisoKey,sisoKey[0:16]).decrypt(item).decode('utf-8'), end = ', ')
                else:
                    print(item, end = ', ')
            print(f"")

    except (ValueError, KeyError) as e:
        print(str(e)) 

if __name__ == "__main__":
    main()
