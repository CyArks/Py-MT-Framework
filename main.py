from MusicTool import Playlist, APISettings, logObj
import os


playlistId = ['PLei_nvJru1BDnEvoYmigBWl25hnV5WhFH']

logObj.enableLogger(True)

p = Playlist(playlistId)
playlistItems = p.getPlaylistVideos()

for item in playlistItems:
    print(item)

if playlistItems:
    print(p.getPlaylistVideos())
    p.createBackup(backupPath=os.getcwd(), items=playlistItems)
    p.setDownloadDir(downloadDir=os.getcwd())
    p.downloadPlaylist()
