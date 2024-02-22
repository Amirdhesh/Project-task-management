from fastapi import FastAPI
from api.api_v1.api import api
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(    
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app",reload=True)
