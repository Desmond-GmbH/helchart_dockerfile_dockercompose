from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.config import initialize_database
from app.entrypoint.routes import email_routes
from app.entrypoint.routes import sms_routes

app = FastAPI()

app.include_router(email_routes.router, prefix="/email", tags=["Email"])
app.include_router(sms_routes.router, prefix="/sms", tags=["SMS"])
initialize_database()

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("app/templates/index.html") as file:
        return file.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
