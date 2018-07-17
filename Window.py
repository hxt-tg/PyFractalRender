from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QAction, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from Settings import *
from ShowPanel import ShowPanel
from StatusPanel import StatusPanel
from ControlPanel import ControlPanel
from PyFractal.Fractal import Fractal
import sys


class Window(QMainWindow):
    menubar = None
    miUndo = None
    show_panel = None
    status_panel = None
    ctrl_panel = None

    def __init__(self):
        super().__init__()
        self.initUI()
        Window.status_panel = StatusPanel(self)
        Window.ctrl_panel = ControlPanel(self)
        Window.show_panel = ShowPanel(self)
        self.show()

    def initUI(self):
        self.setFixedWidth(DEFAULT_WIDTH)
        self.setFixedHeight(DEFAULT_HEIGHT)
        self.setMouseTracking(True)
        self.center()
        self.build_menu()
        self.setWindowTitle(APP_TITLE)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def build_menu(self):
        Window.menubar = self.menuBar()
        mnFile = Window.menubar.addMenu(MN_SAVE)
        miCopy = QAction(MNI_COPY, self)
        miSave = QAction(MNI_SAVE, self)
        miExit = QAction(MNI_EXIT, self)
        mnFile.addAction(miCopy)
        mnFile.addAction(miSave)
        mnFile.addSeparator()
        mnFile.addAction(miExit)
        mnOption = Window.menubar.addMenu(MN_OPTION)
        Window.miUndo = QAction(MNI_UNDO, self)
        Window.miUndo.setEnabled(False)
        miView1 = QAction(MNI_SET_VIEW1, self)
        miView2 = QAction(MNI_SET_VIEW2, self)
        miView3 = QAction(MNI_SET_VIEW3, self)
        miView4 = QAction(MNI_SET_VIEW4, self)
        miView5 = QAction(MNI_SET_VIEW5, self)
        miView6 = QAction(MNI_SET_VIEW6, self)
        miFixScaling = QAction(MNI_FIX_SCALING, self, checkable=True)
        miFixScaling.setChecked(False)
        miOptimizeGraph = QAction(MNI_OPT_GRAPH, self, checkable=True)
        miOptimizeGraph.setChecked(False)
        mnOption.addAction(Window.miUndo)
        mnOption.addSeparator()
        mnOption.addAction(miView1)
        mnOption.addAction(miView2)
        mnOption.addAction(miView3)
        mnOption.addAction(miView4)
        mnOption.addAction(miView5)
        mnOption.addAction(miView6)
        mnOption.addSeparator()
        mnOption.addAction(miFixScaling)
        mnOption.addAction(miOptimizeGraph)
        mnAbout = Window.menubar.addMenu(MN_ABOUT)
        miHelp = QAction(MNI_HELP, self)
        miInfo = QAction(MNI_INFO, self)
        mnAbout.addAction(miHelp)
        mnAbout.addSeparator()
        mnAbout.addAction(miInfo)

        # Shortcuts
        miCopy.setShortcut(COPY_SC)
        miSave.setShortcut(SAVE_SC)
        miExit.setShortcut(EXIT_SC)
        Window.miUndo.setShortcut(UNDO_SC)

        # Action Trigger
        miCopy.triggered.connect(self.copy_image)
        miSave.triggered.connect(self.save_image)
        miExit.triggered.connect(QApplication.instance().quit)
        Window.miUndo.triggered.connect(self.undo_view)
        miView1.triggered.connect(self.set_view1)
        miView2.triggered.connect(self.set_view2)
        miView3.triggered.connect(self.set_view3)
        miView4.triggered.connect(self.set_view4)
        miView5.triggered.connect(self.set_view5)
        miView6.triggered.connect(self.set_view6)
        miFixScaling.triggered.connect(self.fix_scaling)
        miOptimizeGraph.triggered.connect(self.optimize_graph)
        miHelp.triggered.connect(self.show_help)
        miInfo.triggered.connect(self.show_info)

    def keyPressEvent(self, e):
        if e.modifiers() & Qt.ControlModifier:
            ShowPanel.set_press_ctrl(True)
        if e.modifiers() & Qt.ShiftModifier:
            ShowPanel.set_press_shift(True)
        if e.modifiers() & Qt.AltModifier:
            ShowPanel.set_press_alt(True)
            e.ignore()

    def keyReleaseEvent(self, e):
        modifiers = QApplication.keyboardModifiers()
        if modifiers & Qt.ControlModifier:
            ShowPanel.set_press_ctrl(False)
        if modifiers & Qt.ShiftModifier:
            ShowPanel.set_press_shift(False)
        if modifiers & Qt.AltModifier:
            ShowPanel.set_press_alt(False)
            e.ignore()

    @staticmethod
    def copy_image():
        QApplication.clipboard().setPixmap(ShowPanel.picbox.pixmap())

    def save_image(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "",
                                              "PNG Image file (*.png)")
        if path:
            pixmap = ShowPanel.picbox.pixmap()
            pixmap.save(path, "PNG")

    def undo_view(self):
        if Fractal.is_working:
            return
        Window.show_panel.undo_view()

    def set_view1(self):
        if Fractal.is_working:
            return
        self.set_exp(EXP_VIEW1)
        ControlPanel.txt_exp.setText(EXP_VIEW1)

    def set_view2(self):
        if Fractal.is_working:
            return
        self.set_exp(EXP_VIEW2)
        ControlPanel.txt_exp.setText(EXP_VIEW2)

    def set_view3(self):
        if Fractal.is_working:
            return
        self.set_exp(EXP_VIEW3)
        ControlPanel.txt_exp.setText(EXP_VIEW3)

    def set_view4(self):
        if Fractal.is_working:
            return
        self.set_exp(EXP_VIEW4)
        ControlPanel.txt_exp.setText(EXP_VIEW4)

    def set_view5(self):
        if Fractal.is_working:
            return
        self.set_exp(EXP_VIEW5)
        ControlPanel.txt_exp.setText(EXP_VIEW5)

    def set_view6(self):
        if Fractal.is_working:
            return
        self.set_exp(EXP_VIEW6)
        ControlPanel.txt_exp.setText(EXP_VIEW6)

    def fix_scaling(self, state):
        ShowPanel.alwaysFixScale = state

    def optimize_graph(self, state):
        ShowPanel.boost = state

    def show_help(self):
        QMessageBox.about(self, HELP_TITLE, HELP_DIALOG)

    def show_info(self):
        QMessageBox.about(self, INFO_TITLE, INFO_DIALOG)

    @staticmethod
    def set_undo_enabled(status):
        if Window.menubar is not None:
            Window.miUndo.setEnabled(status)

    @staticmethod
    def set_exp(exp):
        if Fractal.is_working:
            return
        Window.show_panel.set_new_view(exp)

    @staticmethod
    def update_pic(pic):
        Window.show_panel.picbox.setPixmap(pic)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
