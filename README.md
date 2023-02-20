# Decrypt and display data from HidePass Password Manager

Decrypt and display data from HidePass Password Manager - com.sisomobile.android.passwordsafe
https://play.google.com/store/apps/details?id=com.sisomobile.android.passwordsafe&hl=en&gl=US

The data is stored in the following sqlite database:
````
/data/data/com.sisomobile.android.passwordsafe/databases/my_password.db
````

The password is a sha-256 hash that is found in:
````
/data/data/com.sisomobile.android.passwordsafe/files/com.sisomobile.android.passwordsafe_preferences.xml
````

The hash needs to be cracked and the plaintext password must be supplied to succesfully decrypt the information.
Ex:
````
hashcat.bin -m 1400 -a 3 --increment --increment-min 4 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08 ?a?a?a?a?a?a?a?a
...
user@s0-Smaz:~/passwordsafe$ echo -n test | sha256sum 
9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08  -
user@s0-Smaz:~/passwordsafe$ python3 decrypt.py -p test -db my_password.db
seq, group_name, title, id, password, url, note, memo_title_01, memo_content_01, memo_title_02, memo_content_02, memo_title_03, memo_content_03, memo_title_04, memo_content_04, memo_title_05, memo_content_05, memo_title_06, memo_content_06, memo_title_07, memo_content_07, memo_title_08, memo_content_08, memo_title_09, memo_content_09, memo_title_10, memo_content_10, memo_count, is_favorite
1, folder1, title1, id1, password1, homepage1, , note1, , , , , , , , , , , , , , , , , , , , 2, 0, 
2, folder1, title2, id2, password2, homepage2, , , , , , , , , , , , , , , , , , , , , , 0, 0, 
3, folder2, title3, id3, password3, homepage3, , , , , , , , , , , , , , , , , , , , , , 0, 0,
````
