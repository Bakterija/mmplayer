## Beta 6 - 2016-dec-31

### Changed
 - Progress bar white circle moves together with progress value when not seeking



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
