from fastapi import FastAPI, Depends
from core.security import JWTChecker
app = FastAPI(
    docs_url="/",
    title="Project Management",
    description="sfpibjfpijpi",    
)
token = JWTChecker()
@app.get("/testhttp", tags=['users'])
def tokencheck(value=Depends(token)):
    print(value)
    return {'status':True}