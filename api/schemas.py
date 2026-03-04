from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator

from api.models import AlbumType, ArtistType, SongType


class SongsCountSchema(BaseModel):
    count: int


class ArtistEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str = Field(validation_alias='artist_id')
    name: str
    followers: int
    popularity: int
    type: Optional[ArtistType] = Field(None, validation_alias='artist_type')
    image_url: Optional[str]

    @field_validator('type', mode='before')
    @classmethod
    def validate_type(cls, value: str) -> ArtistType | None:
        try:
            return ArtistType(value)
        except ValueError:
            return None

    @field_validator('followers', 'popularity', mode='before')
    @classmethod
    def ensure_int(cls, value: Any) -> int:
        match value:
            case int():
                return value or 0
            case str():
                try:
                    return int(value)
                except:
                    return 0
            case _:
                return 0



class SongEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str = Field(validation_alias='song_id')
    name: Optional[str] = Field(None, validation_alias='song_name')
    billboard: Optional[str] = None
    popularity: Optional[int] = None
    explicit: bool = False
    type: Optional[SongType] = Field(None, validation_alias='song_type')

    @field_validator('type', mode='before')
    @classmethod
    def validate_type(cls, value: str) -> SongType | None:
        try:
            return SongType(value)
        except ValueError:
            return None


class AlbumEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: str = Field(validation_alias='album_id')
    name: Optional[str] = None
    billboard: Optional[str] = None
    popularity: Optional[int] = None
    total_tracks: Optional[int] = None
    type: Optional[AlbumType] = Field(None, validation_alias='album_type')

    @field_validator('type', mode='before')
    @classmethod
    def validate_type(cls, value: str) -> AlbumType | None:
        try:
            return AlbumType(value)
        except ValueError:
            return None


class SearchResponse(BaseModel):
    q: str
    entity: str
    count: int
    items: list[ArtistEntry] | list[SongEntry] | list[AlbumEntry]
