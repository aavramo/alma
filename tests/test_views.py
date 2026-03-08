import pytest
from fastapi import status


def test_count_songs(client):
    response = client.get("/catalog/songs/count")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"count": 20405}


def test_search_for_songs(client):
    response = client.get("/catalog/search?q=door&entity=song")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["q"] == "door"
    assert data["entity"] == "song"
    assert data["count"] == 24

    knocking_at_your_back_door = {
        "id": "1VJBQdDrOblSLmoZMeh1xh",
        "name": "Knocking At Your Back Door",
        "billboard": "('Knocking At Your Back Door', 'Deep Purple')",
        "popularity": 46,
        "explicit": False,
        "type": "Solo",
    }
    song = next(
        song for song in data["items"] if song["id"] == knocking_at_your_back_door["id"]
    )
    assert song == knocking_at_your_back_door

def test_search_for_artists(client):
    response = client.get("/catalog/search?q=hendrix&entity=artist")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["q"] == "hendrix"
    assert data["entity"] == "artist"
    assert data["count"] == 1

    jimi_hendrix = {
        "id": "776Uo845nYHJpNaStv1Ds4",
        "name": "Jimi Hendrix",
        "followers": 3460844,
        "popularity": 76,
        "type": "singer",
        "image_url": "https://i.scdn.co/image/14ce65949a921e76421a0164c17f9ebe0a8d76e8"
    }
    artist = data["items"][0]

    assert artist == jimi_hendrix

def test_search_for_albums(client):
    response = client.get("/catalog/search?q=puppets&entity=album")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["q"] == "puppets"
    assert data["entity"] == "album"
    assert data["count"] == 1

    master_of_puppets_remastered = {
        "id": "2Lq2qX3hYhiuPckC8Flj21",
        "name": "Master Of Puppets (Remastered)",
        "billboard": "Master Of Puppets",
        "popularity": 71,
        "total_tracks": 8,
        "type": "album",
    }
    album = next(
        album
        for album in data["items"]
        if album["id"] == master_of_puppets_remastered["id"]
    )
    assert album == master_of_puppets_remastered


def test_search_invalid_entity(client):
    response = client.get("/catalog/search?q=door&entity=invalid")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {
        "detail": [
            {
                "type": "literal_error",
                "loc": ["query", "entity"],
                "msg": "Input should be 'artist', 'song', 'album' or 'track'",
                "input": "invalid",
                "ctx": {"expected": "'artist', 'song', 'album' or 'track'"},
            }
        ]
    }


@pytest.mark.xfail(reason="This test should pass once endpoint is created")
def test_get_album(client):
    response = client.get("/catalog/album/3I9Z1nDCL4E0cP62flcbI5")
    assert response.status_code == status.HTTP_200_OK
    assert response.headers["content-type"] == "application/json"

    assert response.json() == {
        "artists": [
            {
                "followers": 13473817,
                "id": "3qm84nBOXUEQ2vnTfUTTFC",
                "image_url": "https://i.scdn.co/image/80920b4fc80b6d970e2934eb8abe27014fc60632",
                "name": "Guns N' Roses",
                "popularity": 83,
                "type": "band",
            }
        ],
        "billboard": "Appetite For Destruction",
        "id": "3I9Z1nDCL4E0cP62flcbI5",
        "name": "Appetite For Destruction",
        "popularity": 83,
        "songs": [
            {
                "billboard": "('Welcome To The Jungle', \"Guns N' Roses\")",
                "explicit": False,
                "id": "0bVtevEgtDIeRjCJbK3Lmv",
                "name": "Welcome To The Jungle",
                "popularity": 76,
                "type": "Solo",
            },
            {
                "billboard": "('Nightrain', \"Guns N' Roses\")",
                "explicit": False,
                "id": "2vNw57KPaYDzkyPxXYUORX",
                "name": "Nightrain",
                "popularity": 58,
                "type": "Solo",
            },
            {
                "billboard": "('Paradise City', \"Guns N' Roses\")",
                "explicit": False,
                "id": "3YBZIN3rekqsKxbJc9FZko",
                "name": "Paradise City",
                "popularity": 76,
                "type": "Solo",
            },
            {
                "billboard": '("Sweet Child O\' Mine", "Guns N\' Roses")',
                "explicit": False,
                "id": "7o2CTH4ctstm8TNelqjb51",
                "name": "Sweet Child O' Mine",
                "popularity": 80,
                "type": "Solo",
            },
        ],
        "total_tracks": 12,
        "type": "album",
    }
