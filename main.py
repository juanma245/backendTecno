from fastapi import FastAPI
from routers import users,login,permissions,products,stores

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
