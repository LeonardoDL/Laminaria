import spotipy
import re
from spotipy.oauth2 import SpotifyOAuth
import json
import datetime
from random import randint, randrange, shuffle
from collections import Counter

sp = [None]
targetDevice = [None]
playlists = []
all_tracks = dict()

spot_playlists = dict()
spot_playlist_ids = [None]
startingPlaylist = [None]

plCount = [None]
sendList = []

testVersion = [False]

def Init():
    print("Init...")
    scope = "playlist-read-private playlist-modify-private playlist-read-collaborative playlist-modify-public user-library-read user-modify-playback-state user-read-playback-state user-read-email user-read-private"
    cache = '.spotipyoauthcache'

    CLIENT_ID = ''
    CLIENT_SECRET = ''

    sp[0] = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=CLIENT_ID, redirect_uri='http://localhost:5000/token/', client_secret=CLIENT_SECRET,cache_path=cache))

def Restart():
    targetDevice.clear()
    targetDevice.append(None)

    startingPlaylist.clear()
    startingPlaylist.append(None)

def GetDevices():
    print("Getting Devices...")
    # Check for active devices
    devices = sp[0].devices()
    targetDevice[0] = None

    if testVersion[0]:
        with open('devices.json', 'w') as fp:
            json.dump(devices, fp, indent=4)

    if devices == None or len(devices['devices']) <= 0:
        raise Exception("No devices available!")
    else:
        # Simplification
        devices = devices['devices']

        for d in devices:
            if d['is_active']:
                targetDevice[0] = d['id']
                break
        
        # If no devices are active choose a computer
        if targetDevice[0] == None:
            for d in devices:
                if d['type'] == "Computer":
                    targetDevice[0] = d['id']
                    break
        
        # If there are no computers pick any
        if targetDevice[0] == None:
            targetDevice[0] = devices[0]['id']
    
    return devices

def SetDevice(option):
    print(option)
    devices = sp[0].devices()
    targetDevice[0] = None

    if devices == None or len(devices['devices']) <= 0:
        raise Exception("No devices available!")
    else:
        # Simplification
        devices = devices['devices']
        match = re.search('(.+) \((.+)\)', option)
        name = match.group(1)
        type = match.group(2)

        for d in devices:
            if d['name'] == name and d['type'] == type:
                targetDevice[0] = d['id']
    pass

# --------------------------------------------------------------------------------------------------------------------

def GetSpotPlaylists():
    print("Getting playlists...")
    spot_playlist_ids[0] = sp[0].current_user_playlists(limit=50)
    if testVersion[0]:
        with open('spot_playlist_ids.json', 'w') as fp:
            json.dump(spot_playlist_ids[0], fp, indent=4)
        

def GetPlaylists():
    print("Restarting playlists...")
    playlists.clear()
    all_tracks.clear()
    spot_playlists.clear()

    plreturn = []

    # jsonFlag = False

    while True:
        for item in spot_playlist_ids[0]['items']:
            spot_pl = sp[0].playlist(item['id'])
            spot_playlists[item['id']] = spot_pl

            g = dict()
            g['id'] = item['id']
            g['name'] = item['name']
            pl = set()
            _tracks = spot_pl['tracks']
            localCount = 0

            while True:
                if _tracks['previous'] == None:
                    for single_track in _tracks['items']:

                        # if not jsonFlag:
                        #     jsonFlag = True
                        #     with open('track.json', 'w') as fp:
                        #         json.dump(single_track, fp, indent=4)

                        if single_track['is_local'] or single_track['track']['is_local']:
                            localCount += 1
                            continue
                        track = single_track['track']['id']
                        all_tracks[track] = single_track
                        pl.add(track)
                else:
                    for single_track in _tracks['items']:
                        if single_track['is_local']:
                            localCount += 1
                            continue
                        track = single_track['track']['id']
                        all_tracks[track] = single_track
                        pl.add(track)
                        spot_playlists[item['id']]['tracks']['items'].append(single_track)
                if _tracks['next']:
                    _tracks = sp[0].next(_tracks)
                else:
                    break;

            g['set'] = pl
            playlists.append(g)
            plreturn.append(item['name'])
        
        if spot_playlist_ids[0]['next']:
            spot_playlist_ids[0] = sp[0].next(spot_playlist_ids[0])
        else:
            break

    plCount[0] = len(playlists)

    counter = Counter(plreturn)
    for k in counter.keys():
        if counter[k] > 1:
            it = 1
            for p in playlists:
                if p['name'] == k:
                    p['name'] += f" ({str(it)})"
                    it += 1
    
    plreturn.clear()
    for p in playlists:
        plreturn.append(p['name'])

    return plreturn

def GetPlaylistsCached():
    print("Restarting playlists (Cached)...")
    playlists.clear()
    all_tracks.clear()

    plreturn = []

    for item in spot_playlist_ids[0]['items']:
        spot_pl = spot_playlists[item['id']]
        g = dict()
        g['id'] = item['id']
        g['name'] = item['name']
        pl = set()

        localCount = 0
        for single_track in spot_pl['tracks']['items']:
            if single_track['is_local']:
                localCount += 1
                continue
            track = single_track['track']['id']
            all_tracks[track] = single_track
            pl.add(track)

        g['set'] = pl
        playlists.append(g)
        plreturn.append(item['name'])

    plCount[0] = len(playlists)

    counter = Counter(plreturn)
    for k in counter.keys():
        if counter[k] > 1:
            it = 1
            for p in playlists:
                if p['name'] == k:
                    p['name'] += f" ({str(it)})"
                    it += 1
    
    plreturn.clear()
    for p in playlists:
        plreturn.append(p['name'])
    
    return plreturn

def main(names):
    print("Starting...\n")

    if len(names) > 0:
        for item in reversed(playlists):
            if item['name'] not in names:
                playlists.remove(item)
    else:
        raise Exception("No playlist selected")
        return

# --------------------------------------------------------------------------------------------------------------------

    # first_copy = []
    # for item in playlists:
    #     first_copy.append(item.copy())

    # for item in first_copy:
    #     item['set'] = list(item['set'])
    
    # with open('playlists.json', 'w') as fp:
    #     json.dump(first_copy, fp, indent=4)

# --------------------------------------------------------------------------------------------------------------------

    if len(playlists) <= 0:
        raise Exception("Error, couldn't generate intershuffle playlist!")

    playdicts = dict()

    acc = 0
    for i in playlists:
        acc += len(i['set'])

    if len(playlists) == 1 or acc <= 1:
        print("Sneaky Branching...\n")

        interPlaylist = list()
        
        if len(all_tracks) <= 1:
            for p in playlists:
                try:
                    interPlaylist.append(p.pop())
                except KeyError:
                    continue
        else:
            for p in playlists[0]['set']:
                interPlaylist.append(p)
        
        if len(interPlaylist) <= 0:
            raise Exception("Error, couldn't generate intershuffle playlist!")

        print("Calculating Interplaylist...\n")
        
        sendList.clear()
        for id in interPlaylist:
            tr = all_tracks[id]['track']
            g = list()
            g.append(str(id))
            g.append(str(tr['name']))
            g.append(str(tr['artists'][0]['name']))
            sendList.append(str(tr['uri']))

        print("Starting playback...")

        sp[0].transfer_playback(device_id=targetDevice[0], force_play=True)
        sp[0].shuffle(False)
        sp[0].start_playback(device_id=targetDevice[0], uris=sendList)

        print("Finished!\n\n")
        return
    

    for i, itemi in enumerate(playlists):
        for j, itemj in enumerate(playlists):
            if i < j:
                inter = itemi['set'] & itemj['set']
                # If intersection is not zero
                if len(inter) > 0:
                    # Put set i in the dict
                    if str(i) in playdicts:
                        # If it exists, update it
                        playdicts[str(i)]['next'].append(f"{i}+{j}")
                    else:
                        # If it doesnt, create one
                        subPlaylist = dict()
                        subPlaylist['id'] = itemi['id']
                        subPlaylist['name'] = itemi['name']
                        subPlaylist['set'] = itemi['set']
                        subPlaylist['next'] = []
                        subPlaylist['next'].append(f"{i}+{j}")
                        playdicts[str(i)] = subPlaylist
                    
                    # Put intersection set in the dict
                    subPlaylist = dict()
                    subPlaylist['set'] = inter
                    subPlaylist['next'] = []
                    subPlaylist['next'].append(str(i))
                    subPlaylist['next'].append(str(j))
                    playdicts[f"{i}+{j}"] = subPlaylist

                    # Put set j in the dict
                    if str(j) in playdicts:
                        # If it exists, update it
                        playdicts[str(j)]['next'].append(f"{i}+{j}")
                    else:
                        # If it doesnt, create one
                        subPlaylist = dict()
                        subPlaylist['id'] = itemj['id']
                        subPlaylist['name'] = itemj['name']
                        subPlaylist['set'] = itemj['set']
                        subPlaylist['next'] = []
                        subPlaylist['next'].append(f"{i}+{j}")
                        playdicts[str(j)] = subPlaylist
                else:
                    if str(i) not in playdicts:
                        # If it doesnt exist, create one
                        subPlaylist = dict()
                        subPlaylist['id'] = itemi['id']
                        subPlaylist['name'] = itemi['name']
                        subPlaylist['set'] = itemi['set']
                        subPlaylist['next'] = []
                        playdicts[str(i)] = subPlaylist

                    # Put set j in the dict
                    if str(j) not in playdicts:
                        # If it doesnt exist, create one
                        subPlaylist = dict()
                        subPlaylist['id'] = itemj['id']
                        subPlaylist['name'] = itemj['name']
                        subPlaylist['set'] = itemj['set']
                        subPlaylist['next'] = []
                        playdicts[str(j)] = subPlaylist
            

# --------------------------------------------------------------------------------------------------------------------

    playcopy = playdicts.copy()

    for idx in playcopy.keys():
        playcopy[idx] = playcopy[idx].copy()
        playcopy[idx]['set'] = list(playcopy[idx]['set'])
        playcopy[idx]['next'] = playcopy[idx]['next'].copy()
            
    if testVersion[0]:
        with open('playdicts.json', 'w') as fp:
            json.dump(playcopy, fp, indent=4)

# --------------------------------------------------------------------------------------------------------------------

    print("Calculating Interplaylist...\n")

    # Start creating playlist
    interPlaylist = list()
    idxi = ""

    print("Starting with " + str(startingPlaylist[0]))

    if startingPlaylist[0] != None:
        for k in list(playdicts.keys()):
            if "+" in k:
                continue
            if playdicts[k]['name'] == startingPlaylist[0]:
                idxi = k
                break

    if startingPlaylist[0] == None or idxi == "":
        keys = list(playdicts.keys())
        if len(keys) <= 0:
            raise Exception("Error, couldn't generate intershuffle playlist!")
            return

        idxi = keys[ randrange(0, len(keys)) ]

        if "+" in idxi:
            idxi = idxi.split("+")[0]
    
    print("Starting with " + idxi)

    while True:
        copy = list(playdicts[idxi]['set'].copy())
        shuffle(copy)

        if len(copy) == 1:
            interPlaylist.append(copy[0])
            break

        for id in copy:
            if id == None:
                continue
            # Add to playlist and remove from set
            interPlaylist.append(id)
            playdicts[idxi]['set'].remove(id)
            
            flag = False
            subcopy = playdicts[idxi]['next'].copy()
            change = ""
            # If the track is in an intersection
            for idxj in subcopy:
                if id in playdicts[idxj]['set']:
                    # Remove from the intersection
                    playdicts[idxj]['set'].remove(id)
                    # Find out the direction
                    xs = idxj.split('+')
                    temp = ""
                    if xs[0] == idxi:
                        temp = xs[1]
                    elif xs[1] == idxi:
                        temp = xs[0]
                    playdicts[temp]['set'].remove(id)
                    if not flag:
                        change = temp
                        flag = True
            
            if flag:
                idxi = change
                break
        
        if len(playdicts[idxi]['set']) <= 0:
            break

# --------------------------------------------------------------------------------------------------------------------

    if len(interPlaylist) <= 0:
        raise Exception("Error, couldn't generate intershuffle playlist!")

    if len(interPlaylist) > 500:
        interPlaylist = interPlaylist[:500]

    formatList = list()
    sendList.clear()
    for id in interPlaylist:
        tr = all_tracks[id]['track']
        g = list()
        g.append(str(id))
        g.append(str(tr['name']))
        g.append(str(tr['artists'][0]['name']))
        formatList.append(g)
        sendList.append(str(tr['uri']))

    if testVersion[0]:
        with open('formatInterplay.json', 'w') as fp:
            json.dump(formatList, fp, indent=4)

    print("Starting playback...")

    sp[0].transfer_playback(device_id=targetDevice[0], force_play=True)
    sp[0].shuffle(False)
    sp[0].start_playback(device_id=targetDevice[0], uris=sendList)

    print("Finished!\n\n")

def chaoticMain(playset):
    print("Starting...\n")

    if len(playset) > 0:
        for item in reversed(playlists):
            if item['name'] not in playset:
                playlists.remove(item)
    else:
        raise Exception("No playlist selected")
        return


    pFinal = []
    for item in playset:
        for p in playlists:
            if p['name'] == item:
                for track in p['set']:
                    pFinal.append(track)
    
    shuffle(pFinal)
    if len(pFinal) > 500:
        pFinal = pFinal[:500]

# --------------------------------------------------------------------------------------------------------------------

    if len(pFinal) <= 0:
        raise Exception("Error, couldn't generate chaotic playlist!")

    formatList = list()
    sendList.clear()
    for id in pFinal:
        tr = all_tracks[id]['track']
        g = list()
        g.append(str(id))
        g.append(str(tr['name']))
        g.append(str(tr['artists'][0]['name']))
        formatList.append(g)
        sendList.append(str(tr['uri']))
    
    if testVersion[0]:
        with open('formatInterplay.json', 'w') as fp:
            json.dump(formatList, fp, indent=4)

    print("Starting playback...")

    sp[0].transfer_playback(device_id=targetDevice[0], force_play=True)
    sp[0].shuffle(False)
    sp[0].start_playback(device_id=targetDevice[0], uris=sendList)
 
    print("Finished!\n\n")

def savePlaybackToPlaylist(method):
    me = sp[0].me()
    nm = (str(plCount[0])+str(len(sendList))).rjust(8,'0')
    ts = str(datetime.datetime.now().timestamp())
    ts = ts.replace('.','')[3:][:10].rjust(8,'0')

    new_play = sp[0].user_playlist_create(user=me['id'], name=f"{method} Mix {nm}:{ts}", description="Playlist created using the Laminaria app for Playlist shuffling by Leonardo Del Lama")
    for tracks in [sendList[i:i+100] for i in range(0, len(sendList), 100)]:
        sp[0].playlist_add_items(new_play['id'], tracks)


# The MIT License (MIT)
#
# Copyright (c) 2014 Paul Lamere
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.