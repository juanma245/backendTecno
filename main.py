from fastapi import FastAPI
from routers import users,login,permissions,products,stores,reviews
from fastapi.middleware.cors import CORSMiddleware


# Configura CORS
origins = [
    "http://localhost:5173",
]


#uvicorn main:app --reload

app = FastAPI()
app.include_router(users.router)
app.include_router(login.router)
app.include_router(permissions.router)
app.include_router(products.router)
app.include_router(stores.router)
app.include_router(reviews.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def prueba():
    return "hello word"

@app.get("/test")
async def test():
   pass

