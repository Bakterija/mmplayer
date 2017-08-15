# 4.10
 - Fixed compat widget AppPopup not updating min_hover_height correctly


# 4.00
 - Added AppRecycleView filters property
 - Changed AppRecycleView on_key_down method to scroll a page up/down instead of to start or end when page up/down is pressed
 - Added AppRecycleView scrolling to start/end with start/end keyboard buttons
 - Changed MDMenu on_key_down method to close menu before raising exceptions
 - Added new AppPopup kb_system compat widget
 - Added new AppScrollView kb_system compat widget
 - Added kwargs in logger patch logger functions
 - Removed android pan softinput mode in TemplateApp
 - Added terminal_widget hide plugin
 - Fixed TerminalWidgetSystem type error when text is not a string or unicode
 - Added TextEditor text property
 - Added various_widgets package with PopupLabel widget


# 3.10
 - Added HoverBehavior improvements from my kivy pr


# 3.00
 - Added on_release event dispatch in kb_system compat menu widget
 - Changed template_app TextInput rule to TerminalWidgetTextInput
 - Added print_button_text method for terminal_widget press_button plugin
 - Improved focus behavior integration for for text editor
 - Added quick_open method for text editor popup


# 2.00
 - Added changelog
 - Changed AppRecycleBoxLayout.open_context_menu method to return what is returned by context_menu_function
 - Added AppRecycleView on_key_down method with default keys for scrolling and selecting with keyboard that integrate with kb_system
 - Added AppRecycleView warning when default_height and data dict height is not set
 - Added modified kivy_md menu widgets with kb_system focus behavior compatability
 - Fixed FocusBehavior grabbing focus when is_focusable is set to False
 - Added FocusBehavior.focus_previous method
