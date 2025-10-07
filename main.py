from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scales import get_scale as get_scale_from_lib, get_chord as get_chord_from_lib

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/scale/{scale_type}/{note}")
def get_scale(scale_type: str, note: str):
    try:
        scale = get_scale_from_lib(note, scale_type)
        return {"note": note, "scaleType": scale_type, "scale": scale}
    except ValueError as e:
        return {"error": str(e)}

@app.get("/chord/{chord_type}/{note}")
def get_chord(chord_type: str, note: str):
    try:
        chord = get_chord_from_lib(note, chord_type)
        return {"note": note, "chordType": chord_type, "chord": chord}
    except ValueError as e:
        return {"error": str(e)}