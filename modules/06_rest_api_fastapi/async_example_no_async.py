from fastapi import FastAPI
import requests
import uvicorn

app = FastAPI()

def fetch_data(url: str):
    response = requests.get(url)
    return response.json()

@app.get("/api/v1/data")
def get_data():
    url = "https://jsonplaceholder.typicode.com/todos/1"
    data = fetch_data(url)
    return {"data": data}


if __name__ == "__main__":
    uvicorn.run("async_example:app", port=8004, reload=True)