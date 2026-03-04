from fastapi import FastAPI

from .views import router

app = FastAPI(
    title="Alma Music API",
    summary="A simple API for searching artists, albums, and songs.",
    description='''
        It is a simple API that allows you to search for artists, albums, and songs. 
        You can also get the total number of songs in the database and get detailed information about an album.
    '''.strip(),
)
app.include_router(router)
