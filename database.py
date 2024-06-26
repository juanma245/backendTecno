import mysql.connector as mysql
from mysql.connector import Error
from const.encrypConst import dbConst


def get_db():
   try:
      conexion = mysql.connect(
         host = dbConst.host,
         port = dbConst.port,
         user = dbConst.user,
         password = dbConst.password,
         db = dbConst.db
      )
      if conexion.is_connected():
         return conexion
   except Error as ex:
       return "no se pudo "
   




