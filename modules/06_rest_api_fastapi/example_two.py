from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import uvicorn


# Define the base class for SQLAlchemy models
Base = declarative_base()

class Animal(Base):
    __tablename__ = "animals"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)  # If working with MySql, make sure to add length (e.g., Column(String(255)) )
    species = Column(String)
    age = Column(Integer)


DATABASE_URL = "sqlite:///./test.db"
app = FastAPI()

Engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        native_datetime=True,)

# Add a function for creating SessionLocal to aid in setting up unit tests
def create_db(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    return SessionLocal

SessionLocal = create_db(Engine)
app = FastAPI()


class AnimalSchema(BaseModel):
    name: str
    species: str
    age: int


class AnimalNameSchema(BaseModel):
    name: str


# Dependency for providing a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/api/v1/animals")
def read_all_animals(db: Session = Depends(get_db)):
    animals = db.query(Animal).all()
    return {"animals": animals}


@app.post("/api/v1/animals")
def insert_animal(request: AnimalSchema, db: Session = Depends(get_db)):
    new_animal = Animal(name=request.name,
                        species=request.species,
                        age=request.age)
    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)
    return {"animal": new_animal}

@app.get("/api/v1/animals/{animal_id}")
def read_animal(animal_id: int, db: Session = Depends(get_db)):
    animal_record = db.query(Animal).filter(Animal.id == animal_id).first()
    if animal_record is None:
        raise HTTPException(
            status_code=400, detail=f"Could not find animal with id: {animal_id}"
        )
    return {"animal": animal_record}


@app.post("/api/v1/animals")
def insert_animal(request: AnimalSchema, db: Session = Depends(get_db)):
    new_animal = Animal(name=request.name,
                        species=request.species,
                        age=request.age)
    db.add(new_animal)
    db.commit()
    db.refresh(new_animal)
    return {"animal": new_animal}


@app.put("/api/v1/animals/{animal_id}")
def update_animal(animal_id: int, animal: AnimalSchema, db: Session = Depends(get_db)):
    animal_record = db.query(Animal).filter(Animal.id == animal_id).first()
    if animal_record is None:
        raise HTTPException(
            status_code=400, detail=f"Could not find animal with id: {animal_id}"
        )
    animal_data = animal.dict(exclude_unset=True)
    for key, value in animal_data.items():
        setattr(animal_record, key, value)
    db.add(animal_record)
    db.commit()
    updated_animal_record = db.query(Animal).filter(Animal.id == animal_id).first()
    return {"animal_id": animal_id, "animal": updated_animal_record}


@app.patch("/api/v1/animals/{animal_id}")
def update_animal_name(animal_id: int, animal: AnimalNameSchema, db: Session = Depends(get_db)):
    animal_record = db.query(Animal).filter(Animal.id == animal_id).first()
    if animal_record is None:
        raise HTTPException(
            status_code=400, detail=f"Could not find animal with id: {animal_id}"
        )
    animal_data = animal.dict(exclude_unset=True)
    for key, value in animal_data.items():
        setattr(animal_record, key, value)
    db.add(animal_record)
    db.commit()
    updated_animal_record = db.query(Animal).filter(Animal.id == animal_id).first()
    return {"animal_id": animal_id, "animal": updated_animal_record}


@app.delete("/api/v1/animals/{animal_id}")
def delete_item(animal_id: int, db: Session = Depends(get_db)):
    animal_record = db.query(Animal).filter(Animal.id == animal_id).first()
    if animal_record is None:
        raise HTTPException(
            status_code=400, detail=f"Could not find animal with id: {animal_id}"
        )
    db.delete(animal_record)
    db.commit()
    return {"animal_id": animal_id, "message": "Animal removed"}

    
if __name__ == "__main__":
    uvicorn.run("example_two:app", port=8002, reload=True)
