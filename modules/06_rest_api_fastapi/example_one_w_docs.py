from fastapi import FastAPI, HTTPException, Path, Body
from pydantic import BaseModel
import uvicorn


class Animal(BaseModel):
    name: str
    species: str
    age: int
        
class AnimalName(BaseModel):
    name: str
        

tags_metadata = [
    {
        "name":"Create",
        "description": "These endpoints create new internal resources.",
    },
    {
        "name": "Read",
        "description": "These endpoints read existing internal resources.",
    },
    {
        "name": "Update",
        "description": "These endpoints update an existing internal resource.",
        "externalDocs": {
            "description": "External docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "Delete",
        "description": "These endpoints remove existing internal resources.",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

animal_cache = dict()


@app.get("/", 
         summary="Root Endpoint", 
         description="A simple root endpoint for the FastAPI application.",
         tags=["Read"])
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/api/v1/animals/{animal_id}",
         summary="Get an Animal",
         description="Retrieve an animal by its ID.",
         tags=["Read"])
def read_animal(animal_id: int = Path(..., description="The ID of the animal to retrieve.")):
    if animal_id in animal_cache:
        return {"animal": animal_cache[animal_id].dict()}
    else:
        raise HTTPException(
            status_code=400, detail=f"Could not find animal with id: {animal_id}"
        )


@app.post("/api/v1/animals/",
          summary="Create an Animal",
          description="Create a new animal with the provided details.",
         tags=["Create"])
def insert_animal(animal: Animal = Body(..., example={"name": "Tiger", "species": "Panthera tigris", "age": 3})):
    new_id = max(animal_cache.keys() or [0])
    animal_cache[new_id] = animal
    return {"animal": animal}


@app.put("/api/v1/animals/{animal_id}",
         summary="Update an Animal",
         description="Update an entire existing animal by providing its ID and the updated details.",
         tags=["Update"])
def update_animal(animal_id: int = Path(..., description="The ID of the animal to update."),
                animal: Animal = Body(..., example={"name": "Lion", "species": "Panthera leo", "age": 4})):
    if animal_id in animal_cache:
        animal_cache[animal_id] = animal
        return {"animal_id": animal_id, "animal": animal_cache[animal_id]}
    else:
        raise HTTPException(
            status_code=400, detail=f"Could not find animal with id: {animal_id}"
        )
        
@app.patch("/api/v1/animals/{animal_id}",
           summary="Update an Animal",
           description="Update a partial existing animal by providing its ID and the new name.",
           tags=["Update"])
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



@app.delete("/api/v1/animals/{animal_id}",
            summary="Delete an Animal",
            description="Delete an existing animal by providing its ID.",
            tags=["Delete"])
def delete_item(animal_id: int = Path(..., description="The ID of the animal to delete.")):
    if animal_id in animal_cache:
        del animal_cache[animal_id]
        return {"animal_id": animal_id, "message": "Animal removed"}
    else:
        raise HTTPException(
            status_code=400, detail=f"Could not find animal with id: {animal_id}"
        )
        
        
if __name__ == "__main__":
    uvicorn.run("example_one_w_docs:app", port=8001, reload=True)
