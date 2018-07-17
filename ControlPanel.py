from PyQt5.QtWidgets import QGroupBox, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
from Settings import *
from PyFractal.Fractal import Fractal


class ControlPanel(QGroupBox):
    txt_exp = None

    def __init__(self, root):
        self.__root = root
        super().__init__(LBL_CTRL_PANEL, root)
        self.setFixedSize(CTRL_WIDTH-15, CTRL_HEIGHT-10)
        self.move(PIC_WIDTH+10, MENU_HEIGHT)
        lbl_exp = QLabel(LBL_EXP, self)
        lbl_exp.setFixedSize(125, 12)
        lbl_exp.move(15, 20)
        lbl_fz = QLabel('f(z)=', self)
        lbl_fz.setFixedSize(80, 12)
        lbl_fz.move(18, 44)
        ControlPanel.txt_exp = QLineEdit(INIT_EXP, self)
        ControlPanel.txt_exp.setFixedSize(CTRL_WIDTH-80, 20)
        ControlPanel.txt_exp.move(56, 40)
        btn_render = QPushButton(BTN_LBL_RENDER, self)
        btn_render.setFixedSize(180, 30)
        btn_render.move(25, 70)
        btn_reset = QPushButton(BTN_LBL_RESET, self)
        btn_reset.setFixedSize(180, 30)
        btn_reset.move(25, 110)
        lbl_help = QLabel(HELP_CONTENT, self)
        lbl_help.setStyleSheet("color: rgb(127, 127, 127);")
        lbl_help.setFixedSize(205, 130)
        lbl_help.move(15, 145)
        btn_render.pressed.connect(self.render)
        btn_reset.pressed.connect(self.reset)

    # To solve Ctrl keys conflict
    # def limited_keyboard_event(self, e):
    #     if e.modifiers() & Qt.ControlModifier or e.modifiers() & Qt.ShiftModifier and e.modifiers() & Qt.AltModifier:
    #         e.ignore()
    #     e.accept()

    def render(self):
        if Fractal.is_working:
            return
        self.__root.show_panel.set_new_view(ControlPanel.txt_exp.text())

    def reset(self):
        if Fractal.is_working:
            return
        self.__root.show_panel.reset_view()


# To solve Ctrl keys conflict
# class NoCtrlLineEdit(QLineEdit):
#     def keyPressEvent(self, e):
#         if e.modifiers() & Qt.ControlModifier or e.modifiers() & Qt.ShiftModifier and e.modifiers() & Qt.AltModifier:
#             return
#         super().keyPressEvent(e)
