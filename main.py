import uvicorn
from fastapi import FastAPI, HTTPException
from database.db_connection import ConnectionDB
from logs.log_step import app_logger

conn_db = ConnectionDB()
app = FastAPI()


@app.get("/")
def home():
    return "welcome"





if __name__ == "__main__":
    # conn_db.create_database()
    # conn_db.create_tables()
    uvicorn.run("main:app", port=8000, reload=True)
    app_logger.info("The server is up.")