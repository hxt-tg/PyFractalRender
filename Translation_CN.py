from Settings import APP_VERSION, COPY_SC

# String Settings
APP_NAME = '分形图像渲染器'
APP_TITLE = APP_NAME + ' ' + APP_VERSION
MN_SAVE = '保存 (&S)'
MN_OPTION = '选项 (&O)'
MN_ABOUT = '关于 (&A)'
MNI_COPY = '复制到剪贴板 (&C)'
MNI_SAVE = '保存为文件 (&S)...'
MNI_EXIT = '退出 (&E)'
MNI_UNDO = '回退视图 (&U)'
MNI_SET_VIEW1 = '默认 (&D)'
MNI_SET_VIEW2 = '经典 (&C)'
MNI_SET_VIEW3 = '兔子 (&R)'
MNI_SET_VIEW4 = '龙 (&G)'
MNI_SET_VIEW5 = '飞机 (&P)'
MNI_SET_VIEW6 = '三态 (&T)'
MNI_FIX_SCALING = '固定缩放比例 (&F)'
MNI_OPT_GRAPH = '优化图像颜色(慢) (&O)'
MNI_OPT_SPEED = '优化速度 (&S)'
MNI_HELP = '帮助 (&H)...'
MNI_INFO = '信息 (&I)...'
LBL_STATUS_PANEL = '[状态面板]'
LBL_CTRL_PANEL = '[控制面板]'
LBL_EXP = '请输入表达式: '
LBL_TIME = '用时: '
LBL_PROC = '处理进度: '
LBL_SCALE = '缩放比例: '
LBL_ERR = '错误: '
BTN_LBL_RENDER = '渲染'
BTN_LBL_RESET = '重置视图'
HELP_CONTENT = '帮助信息:\n' \
               '  鼠标左键拖动 => 移动视图\n' \
               '  鼠标右键拖动 => 放大视图\n' \
               '  Ctrl+左键单击 => 放大视图 (2倍)\n' \
               '  Alt+左键单击 => 缩小视图 (0.5倍)\n' \
               '  按住 Ctrl 从中心缩放\n' \
               '  按住 Shift 固定缩放比例'
INFO_TITLE = '信息 - ' + APP_NAME
INFO_DIALOG = "这个优雅的分形图像渲染器是用来研究PyQt5的。\n\n" \
              "                                            2018.07\n"
HELP_TITLE = '帮助 - ' + APP_NAME
HELP_DIALOG = "操作步骤: \n" \
              "  1. 在输入框中输入带z的表达式；\n" \
              "  2. 点击【" + BTN_LBL_RENDER + "】按钮；\n" \
              "  3. 在视图窗口中用鼠标拖动；\n" \
              "  4. 点击【" + BTN_LBL_RESET + "】按钮重置视图；\n" \
              "  5. 在选项菜单中尝试一些内置的函数。\n" \
              "  6. " + COPY_SC + " 可以将图像拷贝至剪贴板\n" \
              "  7. 将图像分享给你的好友，可以在文件菜单保存图像。\n\n" \
              "                                                   2018.07\n"
# Error msg
ERR_AT_CHAR = '在字符 '
ERR_BEFORE_EXP = '在表达式前'
YOUR_EXP = '你的表达式'
HAS_ERR = '有错误:'
PLEASE_CHECK = '请检查！'
ERR_INVALID_EXP = '表达式不可用！'
ERR_TOO_LARGE_SCALE = '已缩放至最大！'
ERR_REQUIRE_EXP = '请输入表达式。'
ERR_START_WITH_E = '表达式不能以e开头。'
ERR_UNEXPECTED_E = '未知的e。'
ERR_I = 'i的使用出错。'
ERR_E = 'e的使用出错'
ERR_INVALID_CHAR = '不可用的字符。'
ERR_INVALID_DOT = '错误的小数点。'
ERR_LOST_CLOSE_BRACKET = '左括号缺失。'
ERR_LOST_OPEN_BRACKET = '右括号不匹配'
ERR_LOST_OPND = '缺失操作数。'
ERR_LOST_OPND_MINUS = '缺失操作数。(你可能需要一对括号)'
ERR_NUM_OVERFLOW = '数字过大。'
ERR_UNEXPECTED_DOT = '错误的小数点。(你可能需要添加一个0)'
ERR_DIV_ZERO = '除数为零。'
ERR_NON_INT_POW = '幂是一个非整数。'
