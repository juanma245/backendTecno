import mysql.connector as mysql
from mysql.connector import Error


def get_db():
   try:
      conexion = mysql.connect(
         host = 'localhost',
         port = '3306',
         user = 'root',
         password = '',
         db = 'tiendaTecno'
      )
      if conexion.is_connected():
         return conexion
   except Error as ex:
       return "no se pudo "
   




