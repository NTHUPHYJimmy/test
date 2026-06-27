# 準備網站後端系統
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
app=FastAPI()
app.add_middleware(SessionMiddleware, secret_key="Sdfdgeg")
# 處理路徑 /hello?name=字串
@app.get("/hello")
def hello(request: Request, name):
    request.session["data"] = name
    return {"msg":"哈囉，"+name}

# 處理路徑 /talk
@app.get("/talk")
def talk(request: Request):
    if "data" in request.session:
        name = request.session["data"]
        return {"msg":name+", 歡迎回來"}
    else:
        return {"msg":"你是誰?"}
    

# 靜態檔案處理 支援前端網頁呈現
app.mount("/",StaticFiles(directory="public",html=True))