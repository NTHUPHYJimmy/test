# 準備資料庫連線
import mysql.connector
con = mysql.connector.connect(
    user="root",
    password = "bill88510",
    host = "localhost",
    database = "fastapi"
)
print("資料庫連線成功")
# 準備網站後端系統
from fastapi import FastAPI ,Body , Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI()
# 準備 SessionMiddleware 管理使用者狀態
app.add_middleware(SessionMiddleware, secret_key="Sdfdgeg")
# 建立後端 RESTful API

# 註冊帳號 API
import json
@app.post("/api/member")
def signup(body= Body(None)):
    body = json.loads(body)
    name = body["name"]
    email = body["email"]
    password = body["password"]
    # 檢查 email 是否重複
    cursor = con.cursor()
    cursor.execute("select * from member where email=%s",[email])
    result = cursor.fetchone()
    if result == None: # 代表 email 沒有重複 可以註冊
        cursor.execute("insert into member(name,email,password) values(%s,%s,%s)",[name,email,password])
        con.commit()
        return {"ok":True}
    else: # 代表 email 重複 不能註冊
        return {"ok":False}
    
# 登入帳號 API
@app.put("/api/member/auth")
def signin(request:Request , body= Body(None)):
    body= json.loads(body)
    email = body["email"]
    password = body["password"]
    # 根據前端輸入的 email 及 password 從資料庫取得對應的資料
    cursor = con.cursor()
    cursor.execute("select * from member where email=%s and password=%s",[email,password])
    result=cursor.fetchone()
    if result == None: # 資料庫中沒有對應資料 登入失敗
        request.session["member"] = None
        return {"ok":False}
    else: # 登入成功
        request.session["member"] = {
            "name":result[1], "email":result[2]
        }
        return {"ok":True}

# 檢查登入狀態的 API
@app.get("/api/member/auth")
def check_status(request: Request):
    if "member" in request.session and request.session["member"] != None: # 已經登入
        member= request.session["member"]
        return {"ok":True, "name":member["name"], "email": member["email"]}
    else: # 沒有登入
        return {"ok":False}

# 登出 API
@app.delete("/api/member/auth")
def out(request: Request):
    request.session["member"]=None
    return {"ok":True}

# 靜態檔案處理 支援前端網頁呈現
app.mount("/",StaticFiles(directory="public",html=True))