from fastapi import FastAPI, Request, Form
import uvicorn
import os
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, HTMLResponse
from fastapi.responses import Response
from textSummarizer.pipeline.prediction import PredictionPipeline

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.post("/predict")
async def predict_route(request: Request, text: str = Form(...)):
    try:
        obj = PredictionPipeline()
        summary = obj.predict(text)
        return templates.TemplateResponse("index.html", {"request": request, "result": summary})
    except Exception as e:
        return Response(f"Error Occurred! {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
