from fastapi import FastAPI
from routers import users,login,permissions,products,stores
from database import executeInsert

#uvicorn main:app --reload

app = FastAPI()
app.include_router(users.router)
app.include_router(login.router)
app.include_router(permissions.router)
app.include_router(products.router)
app.include_router(stores.router)

@app.get("/")
async def prueba():
    return "hello word"

@app.get("/test")
async def test():
    sql = """
                       INSERT INTO etiqueta(nombre) 
                       VALUES(%s)
                       """
    datos = ('ios',)

    register = executeInsert(sql,datos)
    return register

