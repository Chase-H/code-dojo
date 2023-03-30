from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn


class Animal(BaseModel):
    name: str
    species: str
    age: int
        

class AnimalName(BaseModel):
    name: str
        

app = FastAPI()

animal_cache = dict()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/api/v1/animals")
def read_all_animals():
    return {"animals": animal_cache}



@app.get("/api/v1/animals/{animal_id}")
def read_animal(animal_id: int):
    if animal_id in animal_cache:
        return {"animal": animal_cache[animal_id].dict()}
    else:
        raise HTTPException(
            status_code=400, detail=f"Could not find animal with id: {animal_id}"
        )


@app.post("/api/v1/animals")
def insert_animal(animal: Animal):
    new_id = max(animal_cache.keys() or [0])
    animal_cache[new_id + 1] = animal
    return {"animal": animal}


@app.put("/api/v1/animals/{animal_id}")
def update_animal(animal_id: int, animal: Animal):
    if animal_id in animal_cache:
        animal_cache[animal_id] = animal
        return {"animal_id": animal_id, "animal": animal_cache[animal_id]}
    else:
        raise HTTPException(
            status_code=400, detail=f"Could not find animal with id: {animal_id}"
        )
        
        
@app.patch("/api/v1/animals/{animal_id}")
def update_animal_name(animal_id: int, animal: AnimalName):
    if animal_id in animal_cache:
        animal_record = animal_cache[animal_id]
        animal_data = animal.dict(exclude_unset=True)
        for key, value in animal_data.items():
            setattr(animal_record, key, value)
        animal_cache[animal_id] = animal_record
        return {"animal_id": animal_id, "animal": animal_cache[animal_id]}
    else:
        raise HTTPException(
            status_code=400, detail=f"Could not find animal with id: {animal_id}"
        )


@app.delete("/api/v1/animals/{animal_id}")
def delete_item(animal_id: int):
    if animal_id in animal_cache:
        del animal_cache[animal_id]
        return {"animal_id": animal_id, "message": "Animal removed"}
    else:
        raise HTTPException(
            status_code=400, detail=f"Could not find animal with id: {animal_id}"
        )

        
if __name__ == "__main__":
    uvicorn.run("example_one:app", port=8000, reload=True)
