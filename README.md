# Laminaria
A playlist shuffling app for Spotify

Disclaimer: The app may or may not call you stupid and/or poor.

You can find the latest builds for Windows and Linux [here](https://drive.google.com/drive/folders/1pgYlXthc3oFW54fC5xt2GR8Hi7cGflfP?usp=sharing).

### Setup

Some steps need to be followed before executing to make sure that it'll run fine:
- Have Spotify Premium
- Have at least one device with Spotify open in it
- Clear your playback
	- Open you playback queue
	- Press the 'Clear' button
	- If it's already clear, no button will appear
- If you're going to use the Intershuffle method of shuffling, make sure you have at list one music that is shared between playlists (the song doesn't need to be the same for
every playlist)

### Sections of the app

> Device where the music will be played:

Choose which device the generated playback will be played in. If you opened a device after opening the app, give it 30 seconds and press the 'Refresh' button

> Refresh

Refreshes the app. Gets a new list of devices and playlists (in case you opened a new device or created a new playlist when the app was already running).

> Shuffling Mode:

- Intershuffle:
	- A controlled method, it will pick random songs from the starting playlist until	it finds one that is in another playlist, and it switches to that playlist and starts adding musics from there, until it finds another song that is also in another playlist, rinse repeat. It keeps switching playlist until there's no songs in the current playlist. It may go back to a previous playlist, but no song is added twice.
- Chaotic:
	- Joins all selected playlists and shuffles them
 
> Choose starting playlist:

If you chose the Intershuffle method, you need to select a playlist to start it in. You can also check the 'Start on a random playlist' checkbutton to start on a random one.

> Select playlists that will be used as source:

Choose which playlists you want to shuffle. You can select all playlists by pressing the 'Select All' button.

> Run

Run the app using the configurations provided in the options above

> Save Playback as new Playlist

This button only appears after you run the app. If you really liked the shuffled playlist generated, you can press this button to save it permanently as a brand new playlist in your library.

### Generated Files:
The file '.spotipyoauthcache' contains your credentials. If you delete it, you'll need to login again.
The file 'icon.ico' is the icon image. If you delete it, it'll be downloaded again next time you open the app.

### TEST MODE
If you believe the app is having bugs, you may press the Ctrl key to activate the Test Mode. It will save its data structures into json files so that you can take a look at them and check if it's all running as intended. Restart the app to get rid of the Test Mode.

#### Generated test files:
- devices.json
  - List of devices found
- spot_playlist_ids.json
  - List of playlists gotten from your user library (only the first page if you have more than 50)
- playdicst.json
  - Dictionary of sets containing the playlists and their intersections. Only created during with the Intershuffle method.
- formatInterplay.json
  - Final list of musics that will be played in the playback

### Running this project yourself

You need first to register an application on Spotify API. You can learn how to that [here](https://developer.spotify.com/documentation/web-api/quick-start/). Then you need to have python installed in your computer and with that also have the Spotipy library installed. Tkinter is usually a built-in python library but Linux distributions may not have it in the python built-in package. You may need to install it also.

After all that, fill the 'CLIENT_ID' and 'CLIENT_SECRET' variables with their respective values that you'll find in your Spotify Dashboard and run the file 'guiCreatorMain.py'.


# Improvements
If I choose to keep this project going, I'll probably add the following features:
- Add liked musics as if it was another playlist
- Make albums count as playlist
- Have a Dark Mode and the option to switch between Light and Dark
- Accept any public playlists using a link or code (even if the user doesn't have it in the library)
- Round Robin shuffling mode
- Customize Intershuffle. Stay more often on the same playlist or not always change.
- Remove Playback music limit (Currently it's 500)
