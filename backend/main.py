from fastapi import FastAPI
from tools import scrape_wuwa_build

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "WuWa Agent Online"}

@app.get("/test-tool")
def test_tool(name: str):
    data = scrape_wuwa_build.invoke(name)
    return {"character": name, "data": data}