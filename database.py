import mysql.connector as mysql
from mysql.connector import Error
from const.encrypConst import dbConst
from fastapi import HTTPException, status


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
   except Error:
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="connection with database failled")
   




