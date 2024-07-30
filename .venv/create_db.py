import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user= 'root',
    passwd = 'parsa123',
)

my_cursor = mydb.cursor()

# my_cursor.execute("CREATE DATABASE our_users") 


my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)


# YOU ONLY RUN THIS ONCE AND NEVER DO IT AGAIN, ITS ONLY TO CREATE THE DATABASE AND NOTHING ELSE, 
# ITS A PRETTY BAD METHOD TO DO IT, BUT ITS EASY TO DO SOOO WHY NOT