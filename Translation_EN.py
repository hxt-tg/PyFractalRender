from Settings import APP_VERSION, COPY_SC

# String Settings
APP_NAME = 'Fractal Render'
APP_TITLE = APP_NAME + ' ' + APP_VERSION
MN_SAVE = '&Save'
MN_OPTION = '&Option'
MN_ABOUT = '&About'
MNI_COPY = '&Copy to clipboard'
MNI_SAVE = '&Save as file ...'
MNI_EXIT = '&Exit'
MNI_UNDO = '&Undo View'
MNI_SET_VIEW1 = '&Default'
MNI_SET_VIEW2 = '&Classic'
MNI_SET_VIEW3 = '&Rabbits'
MNI_SET_VIEW4 = 'Dra&gon'
MNI_SET_VIEW5 = '&Plane'
MNI_SET_VIEW6 = '&Tri-Julia'
MNI_FIX_SCALING = '&Fixed scaling'
MNI_OPT_GRAPH = '&Optimize Graph (Slow)'
MNI_OPT_SPEED = 'Optimize &Speed'
MNI_HELP = '&Help...'
MNI_INFO = '&Info...'
LBL_STATUS_PANEL = '[Status Panel]'
LBL_CTRL_PANEL = '[Control Panel]'
LBL_EXP = 'Expression Here: '
LBL_TIME = 'Time: '
LBL_PROC = 'Processing: '
LBL_SCALE = 'Scale: '
LBL_ERR = 'Error: '
BTN_LBL_RENDER = 'Render'
BTN_LBL_RESET = 'Reset View'
HELP_CONTENT = 'Help:\n' \
               '  Left mouse drag => Move\n' \
               '  Right mouse drag => Zoom\n' \
               '  Ctrl + Click => Zoom in (x2)\n' \
               '  Alt + Click => Zoom out (x0.5)\n' \
               '  Ctrl for operation from center\n' \
               '  Shift for fixed scaling'
INFO_TITLE = 'Info - ' + APP_NAME
INFO_DIALOG = "This beautiful fractal render is for \n" \
              "Python Qt GUI study and final assignment.\n\n" \
              "                                            2018.07\n"
HELP_TITLE = 'Help - ' + APP_NAME
HELP_DIALOG = "Steps: \n" \
              "  1. Input expressions with z in plane text box;\n" \
              "  2. Click '" + BTN_LBL_RENDER + "' button;\n" \
              "  3. Use your mouse to move in view box;\n" \
              "  4. Click '" + BTN_LBL_RESET + "' button to reset;\n" \
              "  5. Try some built-in exps in Option menu.\n" \
              "  6. " + COPY_SC + " can copy this pic to clipboard;\n" \
              "  7. Share pics to your friend. You can save\n" \
              "     it in File menu.\n\n" \
              "                                                   2018.07\n"
# Error msg
ERR_AT_CHAR = 'At char '
ERR_BEFORE_EXP = 'Before expression'
YOUR_EXP = 'Your expression'
HAS_ERR = 'has error:'
PLEASE_CHECK = 'Please check it out!'
ERR_INVALID_EXP = 'Expression not valid!'
ERR_TOO_LARGE_SCALE = 'Too large scaling!'
ERR_REQUIRE_EXP = 'Require expression.'
ERR_START_WITH_E = 'Cannot start with e.'
ERR_UNEXPECTED_E = 'Unexpected e.'
ERR_I = 'Error use for i.'
ERR_E = 'Error use for e.'
ERR_INVALID_CHAR = 'Invalid char.'
ERR_INVALID_DOT = 'Invalid dot.'
ERR_LOST_CLOSE_BRACKET = 'Lost close bracket.'
ERR_LOST_OPEN_BRACKET = 'Right bracket not fitted.'
ERR_LOST_OPND = 'Lost operand.'
ERR_LOST_OPND_MINUS = 'Lost operand. (You may need a pair of brackets)'
ERR_NUM_OVERFLOW = 'Number overflow.'
ERR_UNEXPECTED_DOT = 'Invalid dot. (You may need add a zero)'
ERR_DIV_ZERO = 'Divided by zero.'
ERR_NON_INT_POW = 'Powered by a non-int number.'
