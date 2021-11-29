from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from deta import Deta
from uvicorn import run

deta = Deta("c0mx9zpp_9vpjDEgVd7VtHECEkpD56YfwxeSyhYxs")
db = deta.Base("articles")
app = FastAPI()


class ArticleModel(BaseModel):
    title: str
    content: str


class UpdateArticleModel(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


@app.get('/', tags=['home'])
async def root():
    return {
        'message':
        'Hello World ! Welcome To RestArticles ! Go to /docs to learn more about this API .'
    }


@app.get("/articles", tags=['article'])
async def get_articles():
    return {"articles": db.fetch()}


@app.post("/articles", tags=['article'])
async def add_article(Article: ArticleModel):
    db.insert({"title": Article.title, "content": Article.content})
    return {"message": "Article Added Successfully !"}


@app.get('/articles/{key}', tags=['article'])
async def get_article(key: str):
    article = db.get(key)
    return {"article": article}


@app.put('/articles/{key}', tags=['article'])
async def update_article(key: str, Article: UpdateArticleModel):
    db.update({"title": Article.title, "content": Article.content}, key)
    return {"message": "Article Updated Successfully !"}


@app.delete('/articles/{key}', tags=['article'])
async def delete_article(key: str):
    db.delete(key)
    return {"message": "Article Deleted Successfully !"}


if __name__ == '__main__':
    run(app, host='localhost', port=3000)
