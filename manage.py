import sqlite3
conn = sqlite3.connect('database.db')
c = conn.cursor()

query = "Update member set height = ? where username = ?"
age = str(32)
username = 'adit'
# check = c.execute("SELECT * FROM member WHERE username=?",(username,))

c.execute("INSERT INTO member VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?) ", (username, "emailid", "password","gender","mobileno",None,None,None,None,None,None, None,"Yes"))
conn.commit()
c.execute("select * from member")
# print(c.fetchall())
check = c.fetchall()
print(check)
conn.close()