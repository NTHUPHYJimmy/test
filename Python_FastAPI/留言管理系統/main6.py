# 按照 RESTful 的設計思維及模式 所以叫做 RESTful API
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
from typing import Annotated
from fastapi import FastAPI ,Body
from fastapi.staticfiles import StaticFiles
import json
app = FastAPI()
# 建立後端 RESTful APIs
# 新增留言的 API
@app.post("/api/message")
def create_message(body = Body(None)):
    # 預期前端透過 Request Body 請求文本傳遞 {"author":"姓名", "content":"內容"}
    body=json.loads(body)
    author=body["author"]
    content=body["content"]
    # 連線到資料庫 將資料新增到資料表中
    cursor = con.cursor()
    cursor.execute("insert into message(author,content) values(%s,%s)",[author,content])
    con.commit()
    return {"ok":True}

@app.get("/api/message")
def get_message():
    # 連線到資料庫 取得留言傳回給前端
    cursor = con.cursor(dictionary=True)
    cursor.execute("select * from message")
    data = cursor.fetchall()
    return data

@app.delete("/api/message/{id}")
def delete_message(id):
    # 連線到資料庫 根據 id 刪除留言資料
    cursor = con.cursor()
    cursor.execute("delete from message where id=%s",[id])
    con.commit()
    return {"ok":True}

# 靜態檔案處理 支援前端網頁呈現
app.mount("/",StaticFiles(directory="public",html=True))