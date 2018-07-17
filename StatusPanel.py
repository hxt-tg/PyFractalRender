from PyQt5.QtWidgets import QGroupBox, QLabel
from PyQt5.QtGui import qRgb
from Settings import *


class StatusPanel(QGroupBox):
    INFO_SUCCESS = 1
    INFO_PROCESS = 2
    INFO_ERROR = 3
    DARK_GREEN = qRgb(0, 127, 0)
    lbl_time = None
    lbl_scale = None
    lbl_sx = None
    lbl_sy = None
    lbl_rx = None
    lbl_ry = None

    def __init__(self, root):
        super().__init__(LBL_STATUS_PANEL, root)
        self.setFixedSize(STATUS_WIDTH-15, STATUS_HEIGHT)
        self.move(PIC_WIDTH+10, MENU_HEIGHT+CTRL_HEIGHT)
        StatusPanel.lbl_time = QLabel('', self)
        StatusPanel.lbl_scale = QLabel('', self)
        StatusPanel.lbl_sx = QLabel('', self)
        StatusPanel.lbl_sy = QLabel('', self)
        StatusPanel.lbl_rx = QLabel('', self)
        StatusPanel.lbl_ry = QLabel('', self)
        StatusPanel.lbl_time.setFixedSize(200, 30)
        StatusPanel.lbl_time.move(20, 7)
        StatusPanel.lbl_scale.setFixedSize(200, 30)
        StatusPanel.lbl_scale.move(20, 21)
        StatusPanel.lbl_sx.setFixedSize(200, 30)
        StatusPanel.lbl_sx.move(20, 35)
        StatusPanel.lbl_sy.setFixedSize(200, 30)
        StatusPanel.lbl_sy.move(20, 49)
        StatusPanel.lbl_rx.setFixedSize(200, 30)
        StatusPanel.lbl_rx.move(20, 63)
        StatusPanel.lbl_ry.setFixedSize(200, 30)
        StatusPanel.lbl_ry.move(20, 77)

    @staticmethod
    def set_details(shiftx, shifty, rx, ry):
        StatusPanel.lbl_sx.setText('sx: {}'.format(shiftx))
        StatusPanel.lbl_sy.setText('sy: {}'.format(shifty))
        StatusPanel.lbl_rx.setText('rx: {}'.format(rx))
        StatusPanel.lbl_ry.setText('ry: {}'.format(ry))

    @staticmethod
    def set_scale(value):
        if value < 1:
            StatusPanel.lbl_scale.setText(LBL_SCALE + ' x {:f}'.format(value))
        else:
            StatusPanel.lbl_scale.setText(LBL_SCALE + ' x {:d}'.format(int(value)))

    @staticmethod
    def set_status(info, info_type):
        if info_type == StatusPanel.INFO_SUCCESS:
            StatusPanel.lbl_time.setStyleSheet("color: rgb(0, 127, 0);")
            StatusPanel.lbl_time.setText(LBL_TIME + str(info) + ' secs')
        elif info_type == StatusPanel.INFO_PROCESS:
            StatusPanel.lbl_time.setStyleSheet("color: rgb(127, 127, 0);")
            StatusPanel.lbl_time.setText(LBL_PROC + str(info))
        elif info_type == StatusPanel.INFO_ERROR:
            StatusPanel.lbl_time.setStyleSheet("color: rgb(200, 0, 0);")
            StatusPanel.lbl_time.setText(LBL_ERR + str(info))
        else:
            StatusPanel.lbl_time.setStyleSheet("color: rgb(0, 0, 0);")
            StatusPanel.lbl_time.setText(str(info))
