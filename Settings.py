import os

APP_VERSION = 'v1.0'

# Menu shortcuts
COPY_SC = 'Ctrl+D'
SAVE_SC = 'Ctrl+S'
EXIT_SC = 'Ctrl+Q'
UNDO_SC = 'Ctrl+Z'

# Translation
if os.getenv('LANG', 'zh-hans'):
    LANG = 'CN'
else:
    LANG = 'EN'

LANG = 'EN'

if LANG == 'EN':
    from Translation_EN import *
elif LANG == 'CN':
    from Translation_CN import *
else:
    raise EnvironmentError('No language specified.')

# Layout Settings
PIC_WIDTH = 400
PIC_HEIGHT = 400
CTRL_WIDTH = 250
CTRL_HEIGHT = 290
STATUS_WIDTH = 250
STATUS_HEIGHT = PIC_HEIGHT - CTRL_HEIGHT
MENU_HEIGHT = 27
DEFAULT_WIDTH = PIC_WIDTH + CTRL_WIDTH
DEFAULT_HEIGHT = PIC_HEIGHT + MENU_HEIGHT


# Calculation
MAX_ITER = 50
MAX_MOD = 4
FREQ_UPDATE_LINE = 2
EXP_VIEW1 = 'z^2+0.3'
EXP_VIEW2 = 'z^2-0.75'
EXP_VIEW3 = 'z^2-0.123+0.745i'
EXP_VIEW4 = 'z^2-0.8+0.15i'
EXP_VIEW5 = 'z^2-1.755'
EXP_VIEW6 = 'z^3-0.6+0.3i'

# Initial Image Settings
INIT_EXP = '99'
EMPTY_EXP = '99'
INIT_SHIFTX = 0
INIT_SHIFTY = 0
INIT_RX = 2
INIT_RY = 2
