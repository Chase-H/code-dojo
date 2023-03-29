from fastapi import FastAPI
import httpx
import uvicorn

app = FastAPI()

async def fetch_data(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()

@app.get("/api/v1/data")
async def get_data():
    url = "https://jsonplaceholder.typicode.com/todos/1"
    data = await fetch_data(url)
    return {"data": data}


if __name__ == "__main__":
    uvicorn.run("async_example:app", port=8003, reload=True)