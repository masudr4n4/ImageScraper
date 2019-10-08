import sqlite3
import os
import sys
try:
  os.mkdir('Database')
except:
  pass

class User:
  def __init__(self):
    self.path = 'Database'
    self.connection = sqlite3.connect(os.path.join(self.path,'userinfo.db'))
    self.cur = self.connection.cursor()
    self.cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='loginCredential' ''')
    if not self.cur.fetchone()[0] == 1:
      self.cur.execute('''Create Table loginCredential(
        Mail char(20),
        password char(15)
      )''')
      self.connection.commit()

  def check_mail(self,mail):
    cmd = '''select Mail from loginCredential where Mail = '{0}';'''.format(mail)
    self.cur.execute(cmd)
    if self.cur.fetchone() is not  None:
      print('Accout already created with this email \n Try another mail pls') 
      return False
    else:
      return True

  def creat_account(self,mail,password):
    cmd = '''insert into loginCredential values('{0}','{1}')'''.format(mail,password)
    self.cur.execute(cmd)
    self.connection.commit()
    self.connection.close()
    print('Account created successfully')

  def log_in(self,mail,password):
    try:
      email = self.cur.execute('''select Mail from loginCredential where password =='{0}';'''.format(password)).fetchone()[0]
    except:
      email = None
    try:
      Pass = self.cur.execute('''select Password from loginCredential where Mail == '{0}';'''.format(email)).fetchone()[0]
    except:
      Pass = None
    if email is not None and email == mail and password is not None and password == Pass:
      print('SuccessFully logged in')
      return True
    else:
      print('Your email or password is wrong try with correct password and email')
      return False

    
def creat():
  s = User()
  r = False
  Email = ''
  while r == False:
    mail = input("Enter you Email address: ")
    g = s.check_mail(mail)
    if g == True:
      r = True
      Email = mail
  password = input('Enter your password to creat account: ')
  s.creat_account(Email,password)
def login():
  s = User()
  Mail = input('Enter your email address: ')
  password = input('Enter you password: ')
  #s.log_in(Mail,password)
  if s.log_in(Mail,password) != True:
    login()

def main():
  print('\n\n---------------------Thank you for testing--------------------------')
  info = 'Choose option to go ahead\n\n1.Create a new account\n2.login\n3.exit'
  print(info)
  choice = input('Enter your choice to do (must be interger): ')
  if int(choice) >=3 :
    print('wanted to exit?')
    n = input('Enter y for yes,enter n for no ')
    if n.lower() == 'y':
      sys.exit()
    else:
      main()
  if int(choice) == 1:
    creat()
  if int(choice) == 2:
    login()

if __name__ == "__main__":
  main()
 
