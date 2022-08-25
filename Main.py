from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from flacloader import FlacLoader 


_FlackLoader = FlacLoader("./config.ini")
app = FastAPI()
origins = {
    '*'
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/main")
async def newmain_list():
    return _FlackLoader.GetMusicData()

@app.get("/api/v1/artist_album/{artist}")
async def ArtistAlbum(artist):
    try:
        return _FlackLoader.GetAlbum(artist)
    except ValueError as e:
        return e.args

   
@app.get("/api/v1/album_title/{album}")
async def AlbumTitle(album):
    try:
        return _FlackLoader.GetTitle(album)
    except ValueError as e:
        return e.args

@app.get("/api/v1/songinfo/{artist}/{album}/{title}")
async def Info(artist,album,title):
    try:
        return _FlackLoader.SongInfo(artist,album,title)
    except ValueError as e:
        return e.args

@app.get("/api/v1/songplay/{artist}/{album}/{title}")
async def checkandplay(artist,album,title):
    try:
        return FileResponse(_FlackLoader.GetSongPath(artist,album,title))
    except ValueError as e:
        return e.args 


@app.get("/api/v1/artistlist")
async def artistlist():
    return _FlackLoader.GetArtistList()
@app.get("/api/v1/albumlist")
async def albumlist():
    return _FlackLoader.GetAlbumList()
@app.get("/api/v1/titlelist")
async def titlelist():
    return _FlackLoader.GetTitleList()


