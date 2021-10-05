from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict:
    """Basic hello world route."""
    return {"Hello": "World"}
