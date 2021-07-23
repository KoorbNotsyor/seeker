from kivy.config import Config

# Get rid of the multi-touch red dot:
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# Set icon..
Config.set('kivy', 'window_icon', 'app_icon.png')

# Stop ESC quitting app...
Config.set('kivy', 'exit_on_escape', 0)

