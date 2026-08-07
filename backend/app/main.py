from fastapi import FastAPI

from backend.app.db import check_database_connection
from backend.app.routes.create import router as create_router
from backend.app.routes.select import router as select_router


app = FastAPI(title="Vegan Cook Website")
app.include_router(create_router)
app.include_router(select_router)


@app.get("/api/health")
def health_check(): 
    check_database_connection()

    return {
        "status": "ok",
        "database": "reachable",
    }

def creat_user():
    UserName = str(input("Enter your username: ")),
    UserEmail = str(input("Enter your email: ")),
    UserPassword = str(input("Enter your password: "))

    hashed_password = create_router.hash_password(UserPassword)

    create_router.create_user(UserName, UserEmail, hashed_password)



def main():
    creat_user()

if __name__ == "__main__":
    main()