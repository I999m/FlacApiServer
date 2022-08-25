from collections import defaultdict
from mutagen.flac import FLAC
from starlette.responses import FileResponse
import configparser
from pathlib import Path


class FlacLoader():
    def __init__(self, configini):
        #configparser作成
        self._config_ini_directory = configini
        self._config_ini = configparser.ConfigParser()


        #インスタンス変数

        #音源のパスを格納
        self._path_list = []
        #音源から取得したデータをソートして格納
        self._musicdata = {}
        #音源から取得したアーティスト名を格納
        self._artistlist = []
        #音源から取得したアルバム名を格納
        self._albumlist = []
        #音源から取得した曲名を格納
        self._titlelist = []


        #初期処理実行
        self._OnInitialized()


    #初期処理
    def _OnInitialized(self):
        self._config_ini.read(self._config_ini_directory, encoding='utf-8')
        self._path_list = [i for i in Path(self._config_ini['DEFAULT']['path']).glob("**/*.flac")]
        self._musicdata = self._AddMusicData()
        self._artistlist = [i for i in self._musicdata["artist_album"]]
        self._albumlist = [i for i in self._musicdata["album_title"]]
        self._titlelist = [i["title"] for i in self._musicdata["title"]]
    
    def GetUpdate(self):
        self._OnInitialized()

    #指定のディレクトリに存在する音源を読み取り、各種データを保存
    def _AddMusicData(self):
        #最終的にソートしたデータを返す際に使う変数
        artist_album = defaultdict(list)
        album_title = defaultdict(list)
        titlelist = []
        #ソートの処理
        def FlacTagSort(index,path):
            artist = "empty"
            album = "empty"
            title = f"empty{index}"
            flac = FLAC(path)
            flactags = [j[0] for j in flac.tags]
            #アーティスト名を格納
            if "artist" or "ARTIST" in flactags:
                artist = flac.tags["artist"][0]
            elif "albumartist" or "ALBUMARTIST" in flactags:
                artist = flac.tags["ALBUMARTIST"][0]
            else:
                artist = "empty"

            #アルバム名を格納
            if "album" or "ALBUM" in flactags:
                album = flac.tags["album"][0]
            else:
                pass

            #曲名を格納
            if "title" or "TITLE" in flactags:
                title = flac.tags["title"][0].strip()

            else:
                pass
            #artist_albumにアーティスごとのアルバム名を格納
            if album in artist_album[artist]:
                pass
            else:
                artist_album[artist].append(
                    album
                )
            if title in album_title[album]:
                pass
            else:
                album_title[album].append(
                    title
                )
            titlelist.append({
                "path": path,
                "title":title,
                "album":album,
                "artist":artist
            })
        #音源のパスを読み取ってソートを行う
        for index,path in enumerate(self._path_list):           
            FlacTagSort(index,path)
        #ディクショナリとして、ソートを行ったデータを返す
        return {
            "artist_album": artist_album,
            "album_title": album_title,
            "title": titlelist,     
        }
    #_musicdataを返す
    def GetMusicData(self):
        return self._musicdata

    #アーティストのアルバムを返す
    def GetAlbum(self, artist):
        if artist in self._musicdata["artist_album"]:
            return self._musicdata["artist_album"][artist]
        raise ValueError("none")

    #アルバムのタイトルを返す
    def GetTitle(self, album):
        if album in self._musicdata["album_title"]:
            return self._musicdata["album_title"][album]
        raise ValueError("none")

    #アーティスト　アルバム　曲名をもとに音源の情報を返す
    def SongInfo(self,artist,album,song):     
        for i in self._musicdata["title"]:
            if song == i["title"]:
                if artist == i["artist"]:
                    if album == i["album"]:
                        return i
        raise ValueError("none")

    #アーティスト　アルバム　曲名をもとに音源のパスを返す
    def GetSongPath(self,artist,album,song):     
        for i in self._musicdata["title"]:
            if song == i["title"]:
                if artist == i["artist"]:
                    if album == i["album"]:
                        return i["path"]
        raise ValueError("none")
    
    
    def GetArtistList(self):
        return self._artistlist
    def GetAlbumList(self):
        return self._albumlist
    def GetTitleList(self):
        return self._titlelist

         
