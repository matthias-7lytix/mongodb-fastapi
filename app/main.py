from fastapi import FastAPI
from beanie import init_beanie

from app.db import db
from app.auth import User, router as auth_router
from app.user_groups import router as groups_router
from app.experiments import router as experiments_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(groups_router)
app.include_router(experiments_router)


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=db,
        document_models=[User]
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
