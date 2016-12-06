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
 - Side bar, lower bar, upper bar animate out of window when video screen is selected (Side bar can be brought back in by moving mouse to the windows left side and lower bar by moving mouse to the bottom)

### Changed
 - Right click and mouse scroll do not seek or change volume while mouse is hovering over sliders anymore
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
 - App displays video in a resizable lower corner frame when video screen is not active

### Changed
 - Increased min sidebar width from 20 dp to 4 cm
 - Limited max sidebar width to 8 cm

### Fixed
 - Fixed playlist loading on windows
 - Active media stays highlighted after switching playlists
