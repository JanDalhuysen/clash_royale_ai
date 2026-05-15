import pygetwindow as gw

# List all windows to find the correct title
# print(gw.getAllTitles())

# Find the game window
win = gw.getWindowsWithTitle("Clash Royale - JanDalhuysen")[0]

# Activate and resize to a static resolution (e.g., 540x960)
win.activate()
win.resizeTo(1000, 1000)
win.moveTo(0, 50)
