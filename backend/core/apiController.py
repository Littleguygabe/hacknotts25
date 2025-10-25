from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()


origins = [
    "*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials=True,
    allow_methods = ['*'],    
    allow_headers = ['*']
)

@app.get('/')
def read_root():
    return {"message":"Hello! Your fast api backend is running"}

@app.get("/test")
def test_api_call(message: str):
    print(f'received api request with message > {message}')

    ### fastAPI auto converts python dictionaries into json data
    return {'message':'thank you for your api call'}

if __name__ == '__main__':
    uvicorn.run(app,host="127.0.0.1",port=8000)


