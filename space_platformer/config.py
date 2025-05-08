# config.py

CURRENT_GAMESTATE = "menu"
BUTTON_EDGE_SPACING = 1/3

# Define colors (R, G, B, A) with RGBA
MAP_COLOR_KEYS = {
    (0, 0, 0, 1) : "WALL",        # Black
    (0, 1, 0, 1) : "GOAL",      # Green
    (1, 1, 0, 1) : "PLAYER"   # Yellow
}

MAP_ASSET_KEYS = {
    "WALL": "space_platformer/assets/wall.png",
    "GOAL": "space_platformer/assets/goal.png",
    "PLAYER": "space_platformer/assets/player.png",
}