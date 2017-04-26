## Beta 11 - 2017-apr-26

### Other
 - Added python3 compatability



## Beta 10 - 2017-jan-30

### Other
 - Removed old and unused service from App initialisation



## Beta 9 - 2017-jan-19

### Added
 - New Terminal widget with text input field, openable with tilde key, can play source with "play {path}" or switch screen with "screen {screen name}"
 - Remove info widget text boxes with click or touch

### Changed
 - MediaPlayer switches to next in playlist when current can not be played

### Fixed
 - MediaPlayer doesn't stop working after attempting to play file with unplayable extension

### Other
 - Added warning and exit for python3 in main.py
 - New hotkeys for terminal widget in app_configs/keybinds.py
 - Moved standalone widgets to app_modules/widgets_standalone and others to app_modules/widgets_integrated
 - Removed unneeded widgets
 - More code cleanup



## Beta 8.1 - 2017-jan-16

### Fixed
 - AudioPlayer length shouldn't be set to 0 anymore while playing
 - AudioPlayer can load unicode again



## Beta 8 - 2017-jan-16

### Added
 - Volume is saved between sessions

### Changed
 - Playback bar displays pos and max position as 00:00 when no media is loaded again
 - Added delay betweeen seeking and seek progress bar update to make the progress slider smoother
 - Removed terminal screen

### Fixed
 - Video file queueing works again
 - Play/Pause button text changes when MediaPlayer is paused or resumed again

### Other
 - More code cleanup
 - Added app_configs package with new AppConfigHandler class and Config objects
 - Moved key binding, directory making, setting handling, sidebar item loading from main.py to app_configs package Config modules
 - Renamed MediaGUI to MediaController and moved app_modules/media_gui to app_modules/media_controller, changed a lot of imports and object names, values
 - Removed a lot of unnecessary imports
 - Changed screen names and ids in app_modules/layouts/screen_manager.kv
 - Replaced on_resume MediaPlayer mode with on_play
 - Added on_play modes triggering in MediaPlayer play() method



## Beta 7.1 - 2017-jan-15

### Changed
 - Sped up animations in video screen 2 times

### Fixed
 - Side bar and lower bar don't animate out in other screens while video is playing anymore

### Other
 - More code cleanup
 - Removed Global_Callbacks class and it's instance, and added media players background switch method to App on_pause method
 - Removed service starter from main.py



## Beta 7 - 2017-jan-15

### Fixed
 - Audio Player pauses media properly instead of switching to next file

### Other
 - Rewrote a lot of app_modules/media_player package modules
 - Improved media playback and cleaned up code
 - Removed settings.ini
 - Removed Setting loaders and attributes
 - Removed app_modules/setting_handler.py



## Beta 6 - 2016-dec-31

### Changed
 - Replaced app GPL license with app MIT license
 - Progress bar white circle moves together with progress value when not seeking
 - Playlists display file names instead of paths



## Beta 5 - 2016-dec-27

### Added
 - Window maximize toggle on video double click, auto restore on screen switch

### Changed
 - Side bar and lower bar animate out when cursor leaves window (while
   watching video)
 - White circle in progress bars disappears when cursor leaves window
 - Circle in progress bar moves instantly on click
 - Circle stays at beginning and doesn't move when nothing is playing

### Fixed
 - Adjusted side bar resize border position and size to not interfere with
   it's slider
 - Many Kivy GstPlayer errors

### Other
 - Added garden.progressspinner and garden.contextmenu packages
 - Disabled multitouch for linux and windows




## Beta 4 - 2016-dec-9

### Added
 - InfoWidget in right upper corner displays errors, warnings, info
 - InfoWidget will display a error label when MediaPlayer can't play a file
 - User places in windows os

### Changed
 - Volume hotkeys (up arrow, down arrow) now require ctrl modifier
 - Made scrollbars always visible and have their own space instead of drawing
   over other widgets
 - Screen size changes when side bar is resized while no video is playing

### Fixed
 - Small video widget should not animate in while no video is playing anymore
 - Updated resizable behavior and removed white blocks in windows os
 - Adjusted side bar animations to work with resizing



## Beta 3.1 - 2016-dec-6 - hotfix

### Fixed
 - High cpu usage and memory leak in PlaybackBar



## Beta 3 - 2016-dec-6

### Added
 - Play / pause toggle with spacebar hotkey
 - Play / pause button changes text on pause and on play
 - MediaPlayer module can seek relative values
 - Relative seek(4 sec) with shift + left / right arrow
 - Relative seek(60 sec) with ctrl + left / right arrow
 - Change video volume with mousewheel
 - Left click on small video widget switches to video screen
 - Side bar, lower bar, upper bar animate out of window when video screen is
   selected (Side bar can be brought back in by moving mouse to the windows
   left side and lower bar by moving mouse to the bottom)

### Changed
 - Right click and mouse scroll do not seek or change volume while mouse is
   hovering over sliders anymore
 - MediaPlayer logs a warning instead of crashing when playlist is empty

### Fixed
 - Error when switching to video screen before opening any video
 - Application should not hang when stopping after an init error anymore
 - Pausing audio works properly again
 - Volume slider shows actual media player volume on startup



## Beta 2 - 2016-dec-4

### Added
 - Can add files to unopened playlists
 - Can add files to beginning or end of playlist
 - App displays video in a resizable lower corner frame when video screen is
   not active

### Changed
 - Increased min sidebar width from 20 dp to 4 cm
 - Limited max sidebar width to 8 cm

### Fixed
 - Fixed playlist loading on windows
 - Active media stays highlighted after switching playlists
