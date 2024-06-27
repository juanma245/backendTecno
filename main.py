from fastapi import FastAPI
from routers import users,login

#uvicorn main:app --reload

app = FastAPI()
app.include_router(users.router)
app.include_router(login.router)

@app.get("/")
async def prueba():
    return "hello word"
