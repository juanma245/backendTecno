import mysql.connector as mysql
from mysql.connector import Error
from const.encrypConst import dbConst
from fastapi import HTTPException, status
from const.encrypConst import ErrorConst


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
   
def executeInsert(sql : str, datos : tuple):
   connection = get_db()
   try:
        cursor = connection.cursor()
        cursor.execute(sql,datos)
        connection.commit()   
   except Error:
      raise ErrorConst.executeSql
   finally:
      connection.close()
   
def executeSelectAll(sql : str, datos : tuple):
   connection = get_db()
   try:
      cursor = connection.cursor()
      cursor.execute(sql,datos)
      register = cursor.fetchall()
      return register
   except Error:
      raise ErrorConst.executeSql
   finally:
      connection.close()

def executeSelectOne(sql : str, datos : tuple):
   connection = get_db()
   try:
      cursor = connection.cursor()
      cursor.execute(sql,datos)
      register = cursor.fetchone()
      return register
   except Error:
      raise ErrorConst.executeSql
   finally:
      connection.close()

   




