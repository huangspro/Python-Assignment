import os

# Game window settings
SCREENSIZE = (1200, 600)
FPS = 60

# Audio paths
AUDIO_PATHS = {
    'die': os.path.join(os.getcwd(), 'resources/audios/die.wav'),
    'jump': os.path.join(os.getcwd(), 'resources/audios/jump.wav'),
    'point': os.path.join(os.getcwd(), 'resources/audios/point.wav')
}

# Image paths
IMAGE_PATHS = {
    'cacti': [
        os.path.join(os.getcwd(), 'resources/images/cacti-big.svg'),
        os.path.join(os.getcwd(), 'resources/images/cacti-small.svg')
    ],
    'cloud': os.path.join(os.getcwd(), 'resources/images/cloud.svg'),
    'dino': [
        os.path.join(os.getcwd(), 'resources/images/dino.svg'),
        os.path.join(os.getcwd(), 'resources/images/dino_ducking.svg')
    ],
    'ground': os.path.join(os.getcwd(), 'resources/images/ground-4x.svg'),
    'ptera': os.path.join(os.getcwd(), 'resources/images/ptera.svg'),
    'replay': os.path.join(os.getcwd(), 'resources/images/replay.svg')
}

# Font paths
FONT_PATHS = {
    'joystix': os.path.join(os.getcwd(), 'resources/fonts/JoystixMonospace-Regular.ttf')
}

# Colors
BACKGROUND_COLOR = (235, 235, 235)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
