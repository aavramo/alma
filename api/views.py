from operator import attrgetter
from typing import Literal

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import PlainTextResponse
from sqlalchemy import select

from .dependencies import DBSession
from .models import Album, Artist, Song
from .schemas import SearchResponse, SongsCountSchema


router = APIRouter(prefix="/catalog", tags=["Catalog"])


@router.get(
    "/songs/count",
    name="songs:count",
    summary="Get the total number of songs in the database",
)
async def count_songs(session: DBSession) -> SongsCountSchema:
    stmt = select(Song)
    songs = session.execute(stmt).scalars().all()
    return SongsCountSchema(count=len(songs))


@router.get(
    "/search", name="search", summary="Search for artists, albums, or songs by name"
)
async def search(
    session: DBSession, q: str, entity: Literal["artist", "song", "album", "track"]
) -> SearchResponse:
    model_mapping: dict[str, type[Album] | type[Artist] | type[Song]] = {
        "album": Album,
        "artist": Artist,
        "song": Song,
    }
    model = model_mapping[entity]
    stmt = select(model).where(model.name.like(f"%{q}%"))
    result = session.execute(stmt).scalars().all()

    return SearchResponse(q=q, entity=entity, count=len(result), items=result)
