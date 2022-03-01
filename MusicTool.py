"""
Music Tagger and MP3 Download Framework by ©Florian Manhartseder
More functions and bug fixes coming soon. Stay tuned!
Visit my GitHub Profile: https://github.com/CyArks

None commercial use only!
"""


import pandas as pd
import httplib2
import sys
import os

import googleapiclient.errors
from googleapiclient.discovery import build

from AccessData import APILoginData

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

CHECK_DEPENDENCIES = True

if CHECK_DEPENDENCIES:
    import Dependencies  # All dependencies for this project

# https://musicbrainz.org/doc/MusicBrainz_API
# 28.02.2022: create access variables in Musicbrainz class and assign AccessData.py values
MB_AccessSecret = APILoginData["AccessSecret"]
MB_APIPassword = APILoginData["Password"]
MB_APIUsername = APILoginData["Username"]
MB_AccessKey = APILoginData["AccessKey"]
MB_Email = APILoginData["Email"]


def get_authenticated_service(settings=None):
    if settings is None:
        settings = APISettings.YouTubeDataAPISettings

    flow = flow_from_clientsecrets(settings.CLIENT_SECRETS_FILE, scope=settings.YOUTUBE_SCOPE,
                                   message=settings.MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)

    return build(settings.YOUTUBE_API_SERVICE_NAME, settings.YOUTUBE_API_VERSION,
                 http=credentials.authorize(httplib2.Http()))


class Sample:  # ToDo. Rework / complete Sample function and test it
    def __init__(self, fileLoc, paths=None):
        self.paths = paths
        self.fileLoc = fileLoc
        self.file = open(self.fileLoc, "rb")
        self.sample = self.file.read()
        self.file.close()

    def delFile(self):  # Removes obj file path
        os.remove(self.fileLoc)

    def compareSample(self, sample2):  # Returns True if Samples are equal ToDo. Test function
        if sample2.__class_ is Sample:
            sample2 = sample2.sample

        if sample2 == self.sample:
            return True

        else:
            return False

    def delAllDoubleOnPaths(self):  # ToDo. test function
        samples = []
        pathsDict = []
        i = 0
        for path in self.paths:
            sample = Sample(path)
            pathsDict[i] = path
            samples[i] = sample
            i += 1

        x = 0
        y = 0
        for sample1 in samples:
            x += 1
            for sample2 in samples:
                y += 1
                if sample2 == sample1 and x != y:
                    print(f"Double @ {pathsDict[x]} and {pathsDict[x]}")


class Search:  # ToDo. Test search function
    def __init__(self, searchKey):
        self.youtube = get_authenticated_service()
        self.searchKey = searchKey
        self.response = self._search()

    def _search(self):  # search by Keyword
        self.response = self.youtube.search().list(
            part="snippet",
            maxResults=50,
            q=self.searchKey
        )
        return self.response.execute()


class Video:
    def __init__(self, videoID):
        self.id = videoID

        self.title = None
        self.length = None
        self.artist = None

    # coming soon
    def getLength(self):
        pass

    # coming soon
    def getTitle(self):
        pass

    # coming soon
    def getPopularVideos(self):
        pass


class Logger:  # ToDo. implement Logger to all classes
    from datetime import datetime
    date = datetime.now().strftime("%H:%M:%S").replace(":", ".")

    def __init__(self):
        import os
        self.logFileDir = os.getcwd() + f"\\logFile{self.date}.txt"
        self.loggerEnable = False
        self.logData = []

    def enableLogger(self, value):
        self.loggerEnable = value

        if self.loggerEnable:
            logObj.info(f"{self.__class__}: Logger started!")

    def warning(self, message="\n"):
        time = self.datetime.now().strftime("%H:%M:%S")
        if self.loggerEnable:
            with open(self.logFileDir, "a") as logFile:
                logFile.write(str(f"[{time}, WARNING]: " + message))
                if message != "\n":
                    logFile.write("\n")
                logFile.close()

    def critical(self, message="\n"):
        time = self.datetime.now().strftime("%H:%M:%S")
        if self.loggerEnable:
            with open(self.logFileDir, "a") as logFile:
                logFile.write(str(f"[{time}, CRITICAL]: " + message))
                if message != "\n":
                    logFile.write("\n")
                logFile.close()

    def info(self, message="\n"):
        time = self.datetime.now().strftime("%H:%M:%S")
        if self.loggerEnable:
            with open(self.logFileDir, "a") as logFile:
                logFile.write(str(f"[{time}, INFO]: " + message))
                if message != "\n":
                    logFile.write("\n")
                logFile.close()

    def debug(self, message="\n"):
        time = self.datetime.now().strftime("%H:%M:%S")
        if self.loggerEnable:
            with open(self.logFileDir, "a") as logFile:
                logFile.write(str(f"[{time}, DEBUG]: " + message))
                if message != "\n":
                    logFile.write("\n")
                logFile.close()

    def error(self, message="\n"):
        time = self.datetime.now().strftime("%H:%M:%S")
        if self.loggerEnable:
            with open(self.logFileDir, "a") as logFile:
                logFile.write(str(f"[{time}, ERROR]: " + message))
                if message != "\n":
                    logFile.write("\n")
                logFile.close()

    def import_(self, message="\n"):
        time = self.datetime.now().strftime("%H:%M:%S")
        if self.loggerEnable:
            with open(self.logFileDir, "a") as logFile:
                logFile.write(str(f"[{time}, IMPORT]: " + message))
                if message != "\n":
                    logFile.write("\n")
                logFile.close()

    def init(self, message="\n"):
        time = self.datetime.now().strftime("%H:%M:%S")
        if self.loggerEnable:
            with open(self.logFileDir, "a") as logFile:
                logFile.write(str(f"[{time}, INIT]: " + message))
                if message != "\n":
                    logFile.write("\n")
                logFile.close()

    def settings(self, message="\n"):
        time = self.datetime.now().strftime("%H:%M:%S")
        if self.loggerEnable:
            with open(self.logFileDir, "a") as logFile:
                logFile.write(str(f"[{time}, SETTINGS]: " + message))
                if message != "\n":
                    logFile.write("\n")
                logFile.close()


logObj = Logger()


def _getMetadataFromMusicbrainz(self, settings=None):  # returns JSON Data
    try:
        logObj.import_(f": Importing datetime, hashlib, json, base64, hmac and time.")
        import datetime
        import hashlib
        import json
        import base64
        import hmac
        import time
        logObj.import_(f": Successfully imported datetime, hashlib, json, base64, hmac and time.")
    except ImportError as e:
        logObj.warning(f": Import error: {e}.")
        raise ImportError

    if settings is None:
        settings = APISettings.MusicbrainzAPISettings()

    logObj.info(f": Opening File for sampling.")
    file = open(self.path, "rb")
    sample = file.read()
    file.close()
    logObj.info(f": Sampling completed.")

    timestamp = int(time.mktime(datetime.datetime.utcfromtimestamp(time.time()).timetuple()))
    query_data = sample[:5000000]  # make sure sample is not too big
    sample_bytes = str(len(query_data))

    string_to_sign = settings.http_method + "\n" + settings.http_url_file + "\n" + settings.accessKey + \
                                            "\n" + settings.dataType + "\n" + settings.signatureVersion + \
                                            "\n" + str(timestamp)

    encodedResponse = hmac.new(settings.accessSecret.encode('ascii'),
                               string_to_sign.encode('ascii'),
                               digestmod=hashlib.sha1).digest()

    sign = base64.b64encode(encodedResponse).decode('ascii')
    fields = {
        'access_key': settings.accessKey,
        'sample_bytes': sample_bytes,
        'timestamp': str(timestamp),
        'signature': sign,
        'data_type': settings.dataType,
        "signature_version": settings.signatureVersion
    }

    logObj.info(f"{self.__class__}: Accessing Musicbrainz API")
    response_object = post_multipart('http://' + settings.host +
                                     settings.http_url_file, fields, {"sample": query_data})
    ares = response_object.read().decode('utf8')
    logObj.info(f"{self.__class__}: Response received")

    logObj.info(f"{self.__class__}: Extracting Data from response object")
    extractDataObj = _ExtractData()
    title, album, artists, genres, yt_link = extractDataObj.extract_data_from_dict(
        myDict=self.Dict(json.loads(ares)))
    logObj.info(f"{self.__class__}: Successfully extracted Data from response object.")
    return title, album, artists, genres, yt_link


class File:
    try:
        logObj.import_("<class 'Musictool.File'>: Importing mutagen, addict and mp3_tagger.")
        from mutagen import MutagenError
        # pip install addict
        from addict import Dict

        # https://pypi.org/project/mp3-tagger/
        # pip install mp3-tagger
        from mp3_tagger import MP3File

        logObj.import_("<class 'Musictool.File'>: Successfully imported mutagen, addict and mp3_tagger.")
    except ImportError as e:
        logObj.warning(f"<class 'Musictool.File'>: Import error: {e}.")
        raise ImportError

    def __init__(self, path):
        logObj.init("Init File class.")
        self.path = path
        self.mp3 = self.MP3File(path)
        self.title = self.mp3.song
        self.album = self.mp3.album
        self.artist = self.mp3.artist
        self.genres = None
        self.yt_link = None
        self.mp3_path = path
        self.mp3 = self.MP3File(self.mp3_path)
        logObj.init("Successfully inited File class Object")

    def getMetadataFromMusicbrainz(self, settings: None or object):  # ToDo. Test function
        if settings is None:
            settings = APISettings.MusicbrainzAPISettings()
        return _getMetadataFromMusicbrainz(settings)

    def setMetadataFromMusicbrainz(self, settings=None or object):  # ToDo. Test function

        logObj.info(f"{self.__class__}: Setting mp3 Metadata from Musicbrainz")
        self.title, self.album, self.artist, self.genres, self.yt_link = self.getMetadataFromMusicbrainz(settings)
        self.setTitle(self.title)
        self.setAlbum(self.album)
        self.setArtist(self.artist)

    def getTitle(self):  # ToDo. Test function
        return self.mp3.song

    def setTitle(self, title):  # ToDo. Test function
        try:
            del self.mp3.song
            self.mp3.song = title
            print("Title metadata added: ", title)
            logObj.info(f"{self.__class__}: Title metadata added: " + title + ".")
            self.mp3.save()
        except self.MutagenError as e:
            logObj.error(f"{self.__class__}: Title Tag error! {e}")
            print("Tag Error!")

    def getAlbum(self):  # ToDo. Test function
        return self.mp3.album

    def setAlbum(self, album_name):  # ToDo. Test function
        try:
            del self.mp3.album
            self.mp3.album = album_name
            self.mp3.save()
            print("Album metadata added: ", album_name)
            logObj.info(f"{self.__class__}: Album metadata added: " + album_name + ".")
        except self.MutagenError as e:
            print("Tag Error!")
            logObj.import_(f"{self.__class__}: Album Tag error! {e}")

    def getArtist(self):  # ToDo. Test function
        return self.mp3.artist

    def setArtist(self, artist_name):  # ToDo. Test function
        try:
            del self.mp3.artist
            self.mp3.song = artist_name
            self.mp3.save()
            print("Artist metadata added: ", artist_name)
            logObj.info(f"{self.__class__}: Artist metadata added: " + artist_name + ".")
        except self.MutagenError as e:
            print("Tag Error!")
            logObj.error(f"{self.__class__}: Artist Tag error! {e}")

    # coming soon
    def setGenre(self, genre):  # ToDo. Code and Test function
        pass

    def delFile(self):  # ToDo. Test delete function
        logObj.info(f"{self.__class__}: Deleted File @{self.path}")
        del self.path
        return "Done"


class _ExtractData:
    def __init__(self):
        pass

    def dict_generator(self, indict, pre=None):
        pre = pre[:] if pre else []
        if indict is None:
            print("Indict can not be None type!")
        if isinstance(indict, dict):
            for key, value in indict.items():
                if isinstance(value, dict):
                    for d in self.dict_generator(value, pre + [key]):
                        yield d
                elif isinstance(value, list) or isinstance(value, tuple):
                    for v in value:
                        for d in self.dict_generator(v, pre + [key]):
                            yield d
                else:
                    yield pre + [key, value]
        else:
            yield pre + [indict]

    def extract_data_from_dict(self, myDict):
        import time
        gen = (self.dict_generator(indict=myDict))
        title = None
        album = None
        artists = None
        genres = None
        yt_link = None

        while True:
            try:
                data = next(gen)
            except StopIteration:
                break
            for obj in data:
                if obj == "title":
                    title = data[3]
                if obj == "artists":
                    artists = data[4]
                if obj == "album":
                    album = data[4]
                if obj == "genres":
                    genres = data[4]
                if obj == "vid":
                    yt_link = data[4]

            time.sleep(0.01)

        return title, album, artists, genres, yt_link


class APISettings:
    class MusicbrainzAPISettings(super):
        def __init__(self):
            super().__init__()

            self.host = 'identify-eu-west-1.acrcloud.com'
            self.accessKey = MB_AccessKey
            self.accessSecret = MB_AccessSecret
            self.http_url_file = "/v1/identify"
            self.dataType = "audio"
            self.signatureVersion = "1"
            self.userAgent = ("ID3 Tagger / Playlist downloader", "V1.3", MB_Email)
            self.http_method = "POST"
            self.musicbrainAccData = {'username': MB_APIUsername,
                                      'password': MB_APIPassword}

        def setHTTPUrlFile(self, URLFile):
            logObj.settings(f"{self.__class__}: HTTP Request URL set to: " + URLFile + ".")
            self.http_url_file = URLFile

        def setSignatureVersion(self, sigVers):
            logObj.settings(f"{self.__class__}: Signature version set to: " + sigVers + ".")
            self.signatureVersion = sigVers

        def setUserAgent(self, userAgent):
            logObj.settings(f"{self.__class__}: User agent set to: " + userAgent + ".")
            self.userAgent = userAgent

        def setDataTyp(self, dataType):
            logObj.settings(f"{self.__class__}: DataType set to: " + dataType + ".")
            self.dataType = dataType

        def setHTTPMethod(self, method):
            logObj.settings(f"{self.__class__}: HTTP Methode set to: " + method + ".")
            self.http_method = method

        def setHost(self, host):
            logObj.settings(f"{self.__class__}: Host set to: " + host + ".")
            self.host = host

        def setAccessKey(self, accessKey):
            logObj.settings(f"{self.__class__}: AccessKey set to: " + accessKey + ".")
            self.accessKey = accessKey

        def setAccessSecret(self, accessSecret):
            logObj.settings(f"{self.__class__}: AccessSecret set to {accessSecret}.")
            self.accessSecret = accessSecret

        def setAccountLoginData(self, loginData):
            self.musicbrainAccData = loginData

    class PyTubeSettings:

        def __init__(self):
            self.OAuth = True
            self.allowOAuthCache = True

        def useOAuth(self, value=bool):
            self.OAuth = value

        def allowOAuthCache(self, value=bool):
            self.allowOAuthCache = value

    class YouTubeDataAPISettings:
        YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"
        YOUTUBE_API_SERVICE_NAME = "youtube"
        YOUTUBE_API_VERSION = "v3"
        CLIENT_SECRETS_FILE = "client_secrets.json"
        MISSING_CLIENT_SECRETS_MESSAGE = """
           WARNING: Please configure OAuth 2.0

           To make this sample run you will need to populate the client_secrets.json file
           found at:

           %s

           with information from the Cloud Console
           https://cloud.google.com/console

           For more information about the client_secrets.json file format, please visit:
           https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
           """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                              CLIENT_SECRETS_FILE))

        def __init__(self):
            pass

        def setScope(self, scope):
            self.YOUTUBE_SCOPE = scope

        def setAPIServiceName(self, APIServiceName):
            self.YOUTUBE_API_SERVICE_NAME = APIServiceName

        def setAPIVersion(self, APIVersion):
            self.YOUTUBE_API_VERSION = APIVersion

        def setClientSecretFile(self, ClientSecretFile):
            self.CLIENT_SECRETS_FILE = ClientSecretFile


class Song(APISettings, _ExtractData, File):
    import os
    from mutagen import MutagenError
    import musicbrainzngs
    import pytube

    def __init__(self, url, pytubeSettingsObj=None, musicbrainzSettingsObj=None):
        super().__init__()
        self.url = url
        self.file = None

        if pytubeSettingsObj is not None:
            self.pytubeSettingsObj = pytubeSettingsObj
        else:
            self.pytubeSettingsObj = APISettings.PyTubeSettings()

        if musicbrainzSettingsObj is None:  # If no setting obj is passed then one is created by default constructor
            self.musicbrainzSettings = APISettings.MusicbrainzAPISettings()
        else:
            self.musicbrainzSettings = musicbrainzSettingsObj

        self.yt = self.pytube.YouTube(self.url,
                                      use_oauth=self.pytubeSettingsObj.OAuth,
                                      allow_oauth_cache=self.pytubeSettingsObj.allowOAuthCache)
        self.yt_metadata = self.yt.metadata
        self.thumbnail_path = self.os.getcwd() + "\\thumbnail.jpg"

        self.musicbrainzngs.auth(u=self.musicbrainzSettings.musicbrainAccData["username"],
                                 p=self.musicbrainzSettings.musicbrainAccData["password"])
        self.musicbrainzngs.set_useragent(self.musicbrainzSettings.userAgent, version=1)  # version usually unfilled

    def getMetadataFromMusicbrainz(self, settings: None or object):
        return _getMetadataFromMusicbrainz(settings)

    def getMetadataFromYoutube(self):  # ToDo. Test function
        try:
            if len(self.yt_metadata.raw_metadata) > 0:
                yt_title = self.yt_metadata[0]['Song']
                yt_artists = self.yt_metadata[0]['Artist']
                yt_album = self.yt_metadata[0]['Album']
                return yt_title, yt_artists, yt_album
        except KeyError or IndexError:
            print("Error")

    def FileObj(self):
        if self.mp3_path is not None:
            self.file = File(path=self.mp3_path)
            return self.file

    def setMetadataFromYoutube(self):  # ToDo. Test function
        yt_title, yt_artists, yt_album = self.getMetadataFromYoutube()
        self.setTitle(yt_title)
        self.setAlbum(yt_album)
        self.setArtist(yt_artists)

    def getTitle(self):
        return self.mp3.song

    def setTitle(self, title):  # ToDo. Test function
        try:
            del self.mp3.song
            self.mp3.song = title
            print("Title metadata added: ", title)
        except self.MutagenError:
            print("Tag Error!")

    def getAlbum(self):  # ToDo. Test function
        return self.mp3.album

    def setAlbum(self, album_name):  # ToDo. Test function
        try:
            del self.mp3.album
            self.mp3.album = album_name
            print("Album metadata added: ", album_name)
        except self.MutagenError:
            print("Tag Error!")

    def setArtist(self, artist_name):  # ToDo. Test function
        try:
            del self.mp3.artist
            self.mp3.song = artist_name
            print("Artist metadata added: ", artist_name)
        except self.MutagenError:
            print("Tag Error!")

    def getArtist(self):  # ToDo. Test function
        return self.mp3.artist

    def DownloadSong(self, setMetadataFromYoutube=False, targetFolder=os.getcwd()):  # Returns download path
        import os
        import subprocess
        import pytube

        pytubeObj = pytube.YouTube(self.url)

        print("Downloading: ", pytubeObj.title)
        out_file = pytubeObj.streams.filter(only_audio=True).first().download(targetFolder)

        self.mp3_path = out_file.replace("mp4", "mp3")
        if not os.path.exists(self.mp3_path):
            try:
                if not os.path.exists(self.mp3_path):
                    subprocess.run([
                        'ffmpeg',
                        '-i', os.path.join(out_file),
                        os.path.join(self.mp3_path)
                    ])
                    os.remove(out_file)

                    self.mp3 = self.MP3File(self.mp3_path)

                    # set mp3 tags from yt
                    if setMetadataFromYoutube is True:
                        self.setMetadataFromYoutube()
                else:
                    self.mp3 = self.MP3File(self.mp3_path)

            except FileExistsError:
                print("File already exists!")
        return self.mp3_path


def _create_log(log_data, log_file_dir):  # ToDo. Rework log function!
    logObj.import_("Importing datetime from date.")
    from datetime import date
    logObj.import_("Successfully imported datetime from date.")

    with open(log_file_dir, "w") as log:
        log.write(str(log_data['last_download_url']) + "\n")
        log.write(str(log_data['last_download_id']) + "\n")
        log.write(log_data['last_time_updated'] + " " + date.today().strftime("%d/%m/%Y") + "\n")


def _check_for_existing_log(log_file_dir):  # ToDo. Rework log function!
    import os

    log_data = []
    if os.path.exists(log_file_dir):
        with open(log_file_dir, "r") as log:
            for line in log:
                log_data.append(line)

        existing_log = {
            'last_download_url': log_data[0].replace("\n", ""),
            'last_download_id': log_data[1].replace("\n", ""),
            'last_time_updated': log_data[2].replace("\n", ""),
        }
        return existing_log


class Playlist:
    import os

    def __init__(self, playlistURL, daemon=False, downloadDir=os.getcwd(), log_file_dir=os.getcwd(),
                 targetFolderAddress=None, offset=0, sleepTime=4):
        import pytube

        self.daemon = daemon
        self.downloadDir = downloadDir
        self.log_file_dir = log_file_dir
        self.mp3_path = ""
        self.offset = offset
        self.sleepTime = sleepTime
        self.youtube = get_authenticated_service()

        if playlistURL[0:4] == "PLei":
            self.playlistURL = "https://www.youtube.com/playlist?list=" + playlistURL
        else:
            self.playlistURL = playlistURL

        self.id = self.playlistURL.replace('https://www.youtube.com/playlist?list=', '')

        self.yt = pytube.Playlist(self.playlistURL)
        self.playlist_title = self.yt.title
        self.playlist_length = self.yt.length

        if targetFolderAddress is not None:
            self.targetFolderAddress = targetFolderAddress
        else:
            self.targetFolderAddress = self.downloadDir + "\\" + self.playlist_title

    def AddItem(self, videoID: str, position=None):  # ToDo. Test function
        try:
            add_video_request = self.youtube.playlistItems().insert(
                part="snippet",
                body={
                    'snippet': {
                        'playlistId': self.id,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': videoID
                            # if position is not None:
                            #    'position': 0  # ToDo. position of added song in a playlist
                        }
                    }
                }
            )
            add_video_request.execute()
        except googleapiclient.errors.HttpError as e:
            print("Playlist not found \n ", e)

    def getTitle(self):
        response = self.youtube.playlists().list(
            part="snippet",
            id=self.id
        ).execute()

        title = response.get('items')[0]['snippet'].get('localized').get('title')
        return title

    # coming soon
    def editName(self, name):  # ToDo. Code Playlist name edit function
        pass

    def delete(self):  # ToDo. Test function
        self.youtube.playlists().delete().execute()

    def getPlaylistVideos(self):  # ToDo. Test function
        try:
            maxResults = 50
            items = []

            response = self.youtube.playlistItems().list(
                part='contentDetails,snippet',
                playlistId=self.id,
                maxResults=maxResults
            ).execute()

            items.extend(response.get('items'))
            nextPageToken = response.get('nextPageToken')

            while nextPageToken:
                response = self.youtube.playlistItems().list(
                    part='contentDetails,snippet',
                    playlistId=self.id,
                    maxResults=maxResults,
                    pageToken=nextPageToken
                ).execute()
                items.extend(response.get('items'))
                nextPageToken = response.get('nextPageToken')
            return items

        except Exception as e:
            print(e)
            return

    def getLength(self):  # ToDo. Code Playlist get length function
        length = len(self.getPlaylistVideos())
        return length

    # coming soon
    def getStatus(self):  # ToDo. Code Playlist get Status function
        # public / private / link-shared
        # status =
        # return status
        pass

    # coming soon
    def setStatus(self, status):  # ToDo. Code Playlist set Status function
        pass

    def createNewPlaylist(self, title: str, status: str, description="", tags=None):  # ToDo. Test function
        request = self.youtube.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": [
                        tags
                    ],
                    "defaultLanguage": "en"
                },
                "status": {
                    "privacyStatus": status
                }
            }
        )
        return request.execute()
        # self.id = createdID

    def listItems(self):  # ToDo. Test function
        try:
            items = []
            response = self.youtube.playlists().list(
                part="snippet,contentDetails",
                maxResults=25,
                mine=True).execute()
            items.extend(response.get('items'))
            nextPageToken = response.get('nextPageToken')

            while nextPageToken:
                response = self.youtube.playlists().list(
                    part="snippet,contentDetails",
                    maxResults=25,
                    mine=True).execute()
                items.extend(response.get('items'))
                nextPageToken = response.get('nextPageToken')
            return items
        except Exception as err:
            print(err)
            return

    def listMine(self):  # ToDo. Test function
        try:
            items = []
            response = self.youtube.playlists().list(
                part="snippet,contentDetails",
                maxResults=250,
                mine=True
            ).execute()
            items.extend(response.get('items'))
            nextPageToken = response.get('nextPageToken')

            while nextPageToken:
                response = self.youtube.playlists().list(
                    part="snippet,contentDetails",
                    maxResults=250,
                    mine=True
                ).execute()
                items.extend(response.get('items'))
                nextPageToken = response.get('nextPageToken')

            return items
        except Exception as err:
            print(err)
            return

    def listAllPlaylistsForChannel(self, channelID: str):  # ToDo. Test function
        try:
            items = []
            response = self.youtube.playlists().list(
                part="snippet,contentDetails",
                channelId=channelID,
                maxResults=25
            ).execute()
            items.extend(response.get('items'))
            nextPageToken = response.get('nextPageToken')

            while nextPageToken:
                response = self.youtube.playlists().list(
                    part="snippet,contentDetails",
                    channelId=channelID,
                    maxResults=25,
                    nextPageToken=nextPageToken
                ).execute()
                items.extend(response.get('items'))
                nextPageToken = response.get('nextPageToken')
            return items
        except Exception as err:
            print(err)
            return

    def listMyLikes(self):  # ToDo. Test function
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            myRating="like",
            maxResults=300
        )
        return request.execute()

    def listMyDislikes(self):  # ToDo. Test function
        request = self.youtube.videos().list(
            part="snippet,contentDetails,statistics",
            maxResults=300,
            myRating="dislike"
        )
        return request.execute()

    def createBackup(self, items: list, backupPath=None):  # ToDo. Test function and code import Backup function
        if backupPath is None:
            backupPath = f"{os.getcwd()}\\{self.getTitle()}_backup.xlsx"
        try:
            if not backupPath.endswith('.xlsx'):
                print("Warning! Invalid excel path, path hast to end with xlsx!")
                return

            xlWriter = pd.ExcelWriter(backupPath)
            df = pd.DataFrame(items)

            df['snippet'].apply(pd.Series).to_excel(xlWriter, sheet_name='snippet', index=False)
            df['contentDetails'].apply(pd.Series).to_excel(xlWriter, sheet_name='contentDetails', index=False)
            xlWriter.save()

            print(f'Export is saved at {backupPath}')
        except Exception as e:
            print(e)
            return

    def setDownloadDir(self, downloadDir):
        self.downloadDir = downloadDir

    def setDaemon(self, daemon):
        self.daemon = daemon
        # log("Daemon set to True")

    def getDaemon(self):
        return self.daemon
        # log("Daemon set to True")

    def getPlURL(self):
        return self.playlistURL

    # Deprecated
    def __DownloadPlaylist(self):
        from slugify import slugify
        import sys
        import os

        self.playlist_title = slugify(self.playlist_title)

        # creating Paths for log and music
        self.log_file_dir = self.targetFolderAddress + "\\" + self.playlist_title + "_log.txt"

        # Get existing log
        log = _check_for_existing_log(log_file_dir=self.log_file_dir)

        if log:
            if self.offset >= self.playlist_length:
                print("!Playlist " + self.playlist_title + " is up to date!")
                sys.exit(0)

            print("Log found! Continuing from log data! \n", log)
            print("Downloading Playlist: " + self.playlist_title)
            self.offset = int(log["last_download_id"])

            print("Playlist: " + self.playlist_title)
            print("Last Video id: " + log["last_download_id"])
            print("Last time updated: " + log["last_time_updated"])
            print("Last mp3 downloaded: " + log["last_download_url"])
            print("---------------------------------------------------------------- \n")

        if not os.path.exists(self.targetFolderAddress):
            os.mkdir(self.targetFolderAddress)

        self.__startThread()

    def downloadPlaylist(self):  # ToDo Debug function
        from datetime import datetime
        import threading
        import time

        i = 0
        threads = []
        for url in self.yt.video_urls:
            i += 1
            x = Song(url)
            thread = threading.Thread(target=x.DownloadSong)
            threads.append(thread)
            try:
                thread.start()
                time.sleep(self.sleepTime)
            except ConnectionResetError:
                time.sleep(3)
                thread.start()

                # creating log
        log = {
            'last_download_url': self.yt.video_urls[-1],
            'last_download_id': i + self.offset,
            'last_time_updated': datetime.now().strftime("%H:%M:%S")
        }

        print("!Writing log...")
        _create_log(log_data=log, log_file_dir=self.log_file_dir)
        print("Done.")

    # Deprecated
    def __startThread(self):
        import threading
        import time
        i = 0

        for url in self.yt.video_urls:
            i += 1
            t = threading.Thread(target=Song(url=url).DownloadSong(targetFolder=self.targetFolderAddress))
            t.daemon = self.daemon
            t.start()
            print(t)
            print(url)
            t.join()
            time.sleep(4)

    def getSongObjects(self):  # Yields Song object for each song in Playlist  ToDo. Test function
        for url in self.yt.video_urls:
            SongObject = Song(url)
            yield SongObject

    def mergePlaylistIntoSeasonPly(self):  # ToDo. code function
        pass

    def getEstimatedTimeToDownload(self):  # ToDo. code function to estimate the time it takes to download Playlist
        pass


def EncodeMultipartFormData(fields, files):  # ToDo check function
    from time import time
    boundary = "*****2016.05.27.acrcloud.rec.copyright." + str(
        time()) + "*****"
    CRLF = '\r\n'
    L = []
    for (key, value) in list(fields.items()):
        L.append('--' + boundary)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    body = CRLF.join(L).encode('ascii')
    for (key, value) in list(files.items()):
        L = [CRLF + '--' + boundary, 'Content-Disposition: form-data; name="%s"; filename="%s"' % (key, key),
             'Content-Type: application/octet-stream', CRLF]
        body = body + CRLF.join(L).encode('ascii') + value
    body = body + (CRLF + '--' + boundary + '--' + CRLF + CRLF).encode('ascii')
    content_type = 'multipart/form-data; boundary=%s' % boundary
    return content_type, body


def post_multipart(url, fields, files):
    import urllib.request

    content_type, body = EncodeMultipartFormData(fields, files)
    req = urllib.request.Request(url, data=body)

    req.add_header('Content-Type', content_type)
    req.add_header('Referer', url)
    response = urllib.request.urlopen(req)

    return response
