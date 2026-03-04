from enum import StrEnum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, declarative_base, relationship

Base = declarative_base()


class ArtistType(StrEnum):
    DJ = "DJ"
    BAND = "band"
    DUO = "duo"
    RAPPER = "rapper"
    SINGER = "singer"


class AlbumType(StrEnum):
    ALBUM = "album"
    SINGLE = "single"
    COMPILATION = "compilation"
    EP = "EP"


class SongType(StrEnum):
    SONG = "song"
    REMIX = "remix"
    COVER = "cover"
    COLLABORATION = "Collaboration"
    SOLO = "Solo"


class Artist(Base):
    __tablename__ = "artists"

    id: Mapped[str] = Column(String, primary_key=True, index=True)
    name: Mapped[str | None] = Column(String)
    followers: Mapped[int | None] = Column(Integer)
    popularity: Mapped[int | None] = Column(Integer)
    type: Mapped[ArtistType | None] = Column(
        Enum(ArtistType), index=True, nullable=True
    )
    image_url: Mapped[str | None] = Column(String)

    albums: Mapped[list["Album"]] = relationship(
        "Album",
        secondary="album_artists",
        back_populates="artists",
    )


class Album(Base):
    __tablename__ = "albums"

    id: Mapped[str] = Column(String, primary_key=True, index=True)
    name: Mapped[str | None] = Column(String)
    billboard: Mapped[str | None] = Column(String)
    popularity: Mapped[int | None] = Column(Integer)
    total_tracks: Mapped[int | None] = Column(Integer)
    type: Mapped[AlbumType | None] = Column(Enum(AlbumType), index=True, nullable=True)

    artists: Mapped[list["Artist"]] = relationship(
        "Artist", secondary="album_artists", back_populates="albums"
    )
    songs: Mapped[list["Song"]] = relationship("Song", secondary="tracks")


class AlbumArtist(Base):
    __tablename__ = "album_artists"

    album_id = Column(String, ForeignKey("albums.id"), primary_key=True)
    artist_id = Column(String, ForeignKey("artists.id"), primary_key=True)


class Song(Base):
    __tablename__ = "songs"

    id: Mapped[str] = Column(String, primary_key=True, index=True)
    name: Mapped[str | None] = Column(String)
    billboard: Mapped[str | None] = Column(String)
    popularity: Mapped[int | None] = Column(Integer)
    explicit: Mapped[bool | None] = Column(Boolean)
    type: Mapped[SongType | None] = Column(Enum(SongType), index=True, nullable=True)

    track: Mapped["Track"] = relationship("Track", viewonly=True)


class SongArtist(Base):
    __tablename__ = "song_artists"

    song_id = Column(String, ForeignKey("songs.id"), primary_key=True)
    artist_id = Column(String, ForeignKey("artists.id"), primary_key=True)


class Track(Base):
    __tablename__ = "tracks"

    song_id: Mapped[str] = Column(String, ForeignKey("songs.id"), primary_key=True)
    album_id: Mapped[str] = Column(String, ForeignKey("albums.id"), primary_key=True)
    track_number: Mapped[int | None] = Column(Integer)
