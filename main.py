from fastapi import FastAPI
from src.core.routers import registration
import uvicorn

app = FastAPI()


@app.get("/")
def welcome():
    return "success"


app.include_router(registration.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
