from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello ML World"}


@app.get("/square/{x}")
def square_path(x: int):
    return {"x": x , "square": x**2}

@app.get("/predict")
def predict(x: int):
    return {"x": x , "prediction": x**2}