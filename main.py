from fastapi import FastAPI, HTTPException, status
from sqlmodel import SQLModel, Field, create_engine, Session, select

#Modelo
class Estudiante(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    apellido: str
    correo: str
    edad: int

#Schema
class EstudianteCreate(SQLModel):
    nombre: str
    apellido: str
    correo: str
    edad: int

sqlite_url = "sqlite:///estudiantes.db" 

engine = create_engine(
    sqlite_url,
    echo=True,
)

def create_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(lifespan=create_tables())

@app.post("/estudiantes")
def crear_estudiante(datos: EstudianteCreate):
    estudiante = Estudiante(**datos.model_dump())
    with Session(engine) as session:
        session.add(estudiante)
        session.commit()
        session.refresh(estudiante)
        return estudiante

@app.get("/estudiantes")
def obtener_estudiantes():
    with Session(engine) as session:
        return session.exec(select(Estudiante)).all()

@app.get("/estudiantes/{estudiante_id}")
def obtener_estudiante(estudiante_id: int):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, estudiante_id)
        if not estudiante:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        return estudiante

@app.delete("/estudiantes/{estudiante_id}")
def eliminar_estudiante(estudiante_id: int):
    with Session(engine) as session:
        estudiante = session.get(Estudiante, estudiante_id)
        if not estudiante:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Estudiante no encontrado")
        session.delete(estudiante)
        session.commit()
        return {"message": "Estudiante eliminado exitosamente"}