from operator import attrgetter
from typing import Literal

from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import PlainTextResponse
from sqlalchemy import select, func

from .dependencies import DBSession
from .models import Album, Artist, Song
from .schemas import SearchResponse, SongsCountSchema, AlbumWithArtistsAndSongsEntry

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
    session: DBSession, q: str, entity: Literal["artist", "song", "album", "track"], limit: int, offset: int
) -> SearchResponse:
    model_mapping: dict[str, type[Album] | type[Artist] | type[Song]] = {
        "album": Album,
        "artist": Artist,
        "song": Song,
    }
    model = model_mapping[entity]
    count = session.query(func.count(model.id)).where(model.name.like(f"%{q}%")).scalar()
    stmt = select(model).where(model.name.like(f"%{q}%")).offset(offset).limit(limit)
    result = session.execute(stmt).scalars().all()

    return SearchResponse(q=q, entity=entity, count=count, items=result)

@router.get(
    "/album/{album_id}", name="albums", summary="Get an album by id"
)
async def album(request: Request, session: DBSession, album_id: str) -> AlbumWithArtistsAndSongsEntry:
    stmt = select(Album).where(Album.id == album_id)

    album = session.execute(stmt).scalars().first()

    accept = request.headers.get("accept", "")
    if "text/plain" in accept:
        album.songs.sort(key=lambda s: s.track.track_number)
        return PlainTextResponse(__format_album_text_specs1(album))

    return AlbumWithArtistsAndSongsEntry.model_validate(album)


def __format_album_text_specs1(album: Album) -> str:
    lines = [f"{album.name}", ""]

    for song in album.songs:
        track_number = song.track.track_number
        lines.append(f"{__indent(track_number)}{track_number}. {song.name}")

    lines.append("")
    lines.append(f"Total tracks: {album.total_tracks}")
    lines.append("")

    return "\n".join(lines)

def __indent(track_number: int) -> str:
    digit = len(str(track_number))
    match digit:
        case 1:
            return "    "
        case 2:
            return "   "
        case 3:
            return "  "
        case 4:
            return " "
        case _:
            return ""
