from PyQt5.QtWidgets import QGroupBox, QLabel, QMessageBox
from PyQt5.QtGui import QImage, QPixmap, QCursor, QPainter, QColor
from PyQt5.QtCore import Qt
from Settings import *
from StatusPanel import StatusPanel
from PyFractal.Fractal import Fractal


class ShowPanel(QGroupBox):
    parent = None
    boost = False
    alwaysFixScale = False
    exp = INIT_EXP
    picbox = None
    rect = None     # Modify next view of image
    is_press_lm = False
    is_press_rm = False
    is_press_shift = False
    is_press_ctrl = False
    is_press_alt = False
    is_moving = False
    start_point = None

    def __init__(self, root):
        super().__init__(root)
        ShowPanel.parent = root
        self.setFixedSize(PIC_WIDTH, PIC_HEIGHT)
        self.move(5, MENU_HEIGHT)
        ShowPanel.picbox = QLabel('', self)
        ShowPanel.picbox.setFixedSize(PIC_WIDTH, PIC_HEIGHT)
        ShowPanel.picbox.move(0, 0)
        ShowPanel.picbox.setCursor(Qt.SizeAllCursor)
        self.setMouseTracking(True)
        ShowPanel.picbox.setMouseTracking(True)
        self.__history = [ViewInfo(INIT_SHIFTX, INIT_SHIFTY, INIT_RX, INIT_RY)]
        # init_pic = QPixmap(PIC_HEIGHT, PIC_WIDTH)
        # init_pic.fill(Qt.white)
        # Fractal.pic = init_pic
        # ShowPanel.picbox.setPixmap(init_pic)
        self.set_new_view(INIT_EXP)

    def refresh_hist_view(self, is_record):
        if ShowPanel.rect is None:
            ShowPanel.rect = Rectangle(0, 0, PIC_WIDTH, PIC_HEIGHT)
        info = self.__history[-1]
        shiftx = info.shiftx - info.rx / PIC_WIDTH * int(
            PIC_WIDTH//2 - ShowPanel.rect.x - ShowPanel.rect.width//2) * 2 * (
            -1 if ShowPanel.is_moving else 1)
        shifty = info.shifty - info.ry / PIC_HEIGHT * int(
            PIC_HEIGHT//2 - ShowPanel.rect.y - ShowPanel.rect.height//2) * 2 * (
            -1 if ShowPanel.is_moving else 1)
        rx = info.rx / (PIC_WIDTH / ShowPanel.rect.width)
        ry = info.ry / (PIC_HEIGHT / ShowPanel.rect.height)
        if rx < 1e-10 or ry < 1e-10:
            StatusPanel.set_status(ERR_TOO_LARGE_SCALE, StatusPanel.INFO_ERROR)
            return
        self.refresh_view(shiftx, shifty, rx, ry, is_record)

    def refresh_view(self, shiftx, shifty, rx, ry, is_record):
        StatusPanel.set_scale(INIT_RX * INIT_RY / (rx * ry))
        StatusPanel.set_details(shiftx, shifty, rx, ry)
        if is_record:
            self.__history.append(ViewInfo(shiftx, shifty, rx, ry))
        try:
            f = Fractal(ShowPanel.parent, ShowPanel.exp, ShowPanel.boost)
        except ValueError as e:
            ShowPanel.errDialog(e.args[0])
            ShowPanel.exp = Fractal.last_exp
            return None
        try:
            f.createFractalImage(PIC_WIDTH, PIC_HEIGHT, shiftx, shifty, rx, ry)
        except Exception as e:
            ShowPanel.errDialog(e.args[0])
            ShowPanel.exp = Fractal.last_exp
            raise e
        self.update_undo()

    @staticmethod
    def errDialog(info):
        QMessageBox.critical(ShowPanel.parent, PLEASE_CHECK, info)

    def undo_view(self):
        if len(self.__history) > 1:
            self.__history.pop()
            info = self.__history[-1]
            self.refresh_view(info.shiftx, info.shifty, info.rx, info.ry, False)
        else:
            print('\a')
        self.update_undo()

    def update_undo(self):
        ShowPanel.parent.set_undo_enabled(len(self.__history) > 1)

    def reset_view(self):
        info = self.__history[0]
        self.__history.clear()
        self.refresh_view(info.shiftx, info.shifty, info.rx, info.ry, True)

    def set_new_view(self, input_exp):
        if Fractal.is_working:
            return
        try:
            Fractal(ShowPanel.parent, input_exp)
        except Exception as e:
            error_content = '{}\n{}\n{}\n{}'.format(YOUR_EXP, input_exp, HAS_ERR, e.args[0])
            ShowPanel.errDialog(error_content)
            StatusPanel.set_status(ERR_INVALID_EXP, StatusPanel.INFO_ERROR)
            return None
        ShowPanel.exp = input_exp
        info = self.__history[0]
        self.__history.clear()
        self.refresh_view(info.shiftx, info.shifty, info.rx, info.ry, True)

    @staticmethod
    def set_press_shift(is_press_shift):
        ShowPanel.is_press_shift = is_press_shift

    @staticmethod
    def set_press_ctrl(is_press_ctrl):
        ShowPanel.is_press_ctrl = is_press_ctrl
        if Fractal.is_working:
            return
        if ShowPanel.is_press_ctrl and not ShowPanel.is_press_lm and not ShowPanel.is_press_rm:
            ShowPanel.picbox.setCursor(QCursor(QPixmap('pic/zoom_in.png')))
        elif not ShowPanel.is_press_lm:
            ShowPanel.picbox.setCursor(QCursor(Qt.SizeAllCursor))
        if ShowPanel.is_press_lm:
            ShowPanel.picbox.setCursor(QCursor(Qt.CrossCursor))
        if not ShowPanel.is_press_lm and not ShowPanel.is_press_ctrl:
            ShowPanel.rect = None
            ShowPanel.force_repaint()
            ShowPanel.rect = Rectangle()

    @staticmethod
    def set_press_alt(is_press_alt):
        ShowPanel.is_press_alt = is_press_alt
        if Fractal.is_working:
            return
        if ShowPanel.is_press_alt and not ShowPanel.is_press_lm and not ShowPanel.is_press_rm:
            ShowPanel.picbox.setCursor(QCursor(QPixmap('pic/zoom_out.png')))
        elif not ShowPanel.is_press_lm:
            ShowPanel.picbox.setCursor(QCursor(Qt.SizeAllCursor))
        if ShowPanel.is_press_lm:
            ShowPanel.picbox.setCursor(QCursor(Qt.CrossCursor))
        if not ShowPanel.is_press_lm and not ShowPanel.is_press_alt:
            ShowPanel.rect = None
            ShowPanel.force_repaint()
            ShowPanel.rect = Rectangle()

    @staticmethod
    def get_image():
        image = QImage(ShowPanel.picbox.pixmap())
        return image

    @staticmethod
    def force_repaint():
        pic = QPixmap(PIC_WIDTH, PIC_HEIGHT)
        qp = QPainter()
        qp.begin(pic)
        qp.drawPixmap(0, 0, PIC_WIDTH, PIC_HEIGHT, Fractal.pic)
        qp.end()
        ShowPanel.picbox.setPixmap(pic)

    @staticmethod
    def makeRectangle(p1, p2):
        print(p1.x, p1.y, p2.x, p2.y)
        if ShowPanel.rect is None:
            return
        if ShowPanel.is_press_lm and (ShowPanel.is_press_ctrl or ShowPanel.is_press_shift):
            return
        if ShowPanel.is_moving:
            x = p2.x - p1.x
            y = p2.y - p1.y
            w = PIC_WIDTH
            h = PIC_HEIGHT
        else:
            p2x = 0 if p2.x < 0 else (PIC_WIDTH - 1 if p2.x > PIC_WIDTH else p2.x)
            p2y = 0 if p2.y < 0 else (PIC_HEIGHT - 1 if p2.y > PIC_HEIGHT else p2.y)
            x = min(p1.x, p2x)
            y = min(p1.y, p2y)
            w = abs(p1.x - p2x)
            h = abs(p1.y - p2y)
            ShowPanel.rect = Rectangle(x, y, w, h)
            if ShowPanel.is_press_shift or ShowPanel.alwaysFixScale:  # Fixed scaling
                w = h = min(w, h)
                if p2.x < p1.x:
                    x = x + p1.x - p2.x - w
                if p2.y < p1.y:
                    y = y + p1.y - p2.y - h
            if ShowPanel.is_press_ctrl:  # 1:1 Scaling
                x -= 0 if p2.x < p1.x else w
                y -= 0 if p2.y < p1.y else h
                w *= 2
                h *= 2
        ShowPanel.rect = Rectangle(x, y, w, h)
        pic = QPixmap(PIC_WIDTH, PIC_HEIGHT)
        qp = QPainter()
        qp.begin(pic)
        qp.drawPixmap(0, 0, PIC_WIDTH, PIC_HEIGHT, Fractal.pic)
        qp.setPen(QColor(200, 200, 0))
        qp.drawRect(x, y, w, h)
        qp.end()
        ShowPanel.picbox.setPixmap(pic)

    def mousePressEvent(self, e):
        if Fractal.is_working:
            return
        if e.buttons() & Qt.LeftButton:
            ShowPanel.is_press_lm = True
        elif e.buttons() & Qt.RightButton:
            ShowPanel.is_press_rm = True

        if ShowPanel.is_press_rm:
            ShowPanel.picbox.setCursor(QCursor(Qt.CrossCursor))
            ShowPanel.start_point = Point(e.x(), e.y())
            ShowPanel.rect = Rectangle()
        elif ShowPanel.is_press_lm and not ShowPanel.is_press_ctrl:
            ShowPanel.is_moving = True
            ShowPanel.start_point = Point(e.x(), e.y())
            if not ShowPanel.is_press_alt and not ShowPanel.is_press_shift and not ShowPanel.is_press_ctrl:
                ShowPanel.rect = Rectangle()
        elif ShowPanel.is_press_lm and ShowPanel.is_press_ctrl:
            ShowPanel.is_moving = False
            # ShowPanel.rect = Rectangle()
        else:
            ShowPanel.rect = None

    def mouseReleaseEvent(self, e):
        if Fractal.is_working:
            return
        if e.button() == 1:  # Release Left Mouse
            ShowPanel.is_press_lm = False
            if ShowPanel.is_press_alt and ShowPanel.rect is not None:
                ShowPanel.rect = Rectangle(ShowPanel.rect.x - PIC_HEIGHT * 3 / 4,
                                           ShowPanel.rect.y - PIC_HEIGHT * 3 / 4,
                                           PIC_WIDTH * 2, PIC_HEIGHT * 2)
        elif e.button() == 2:  # Release Right Mouse
            ShowPanel.is_press_rm = False
            ShowPanel.makeRectangle(ShowPanel.start_point, Point(e.x(), e.y()))
        if ShowPanel.rect.width > 0 and ShowPanel.rect.height > 0:
            self.refresh_hist_view(True)
            ShowPanel.rect = None
        ShowPanel.picbox.setCursor(QCursor(Qt.SizeAllCursor))
        ShowPanel.is_moving = False

    def mouseMoveEvent(self, e):
        if Fractal.is_working:
            return
        if ShowPanel.is_press_lm:
            # Press left button and move
            if e.x() < 0 or e.y() < 0:
                return
            if ShowPanel.is_press_ctrl or ShowPanel.is_press_shift or ShowPanel.is_press_alt:
                return
            ShowPanel.picbox.setCursor(QCursor(Qt.SizeAllCursor))
            if ShowPanel.rect is not None:
                ShowPanel.makeRectangle(ShowPanel.start_point, Point(e.x(), e.y()))
        if ShowPanel.is_press_rm:
            # Press right button and move
            ShowPanel.picbox.setCursor(QCursor(Qt.CrossCursor))
            if ShowPanel.rect is not None:
                ShowPanel.makeRectangle(ShowPanel.start_point, Point(e.x(), e.y()))
        else:
            if ShowPanel.is_press_ctrl or ShowPanel.is_press_alt:
                ShowPanel.is_moving = False
                p = Point(e.x(), e.y())
                p.x = PIC_WIDTH // 4 if p.x < PIC_WIDTH // 4 else (
                    PIC_WIDTH // 4 * 3 if p.x > PIC_WIDTH // 4 * 3 else p.x)
                p.y = PIC_HEIGHT // 4 if p.y < PIC_HEIGHT // 4 else (
                    PIC_HEIGHT // 4 * 3 if p.y > PIC_HEIGHT // 4 * 3 else p.y)
                ShowPanel.rect = Rectangle()
                if ShowPanel.is_press_ctrl:
                    ShowPanel.makeRectangle(p, Point(p.x+PIC_WIDTH//4, p.y + PIC_HEIGHT//4))
                elif ShowPanel.is_press_alt:
                    ShowPanel.makeRectangle(Point(p.x-PIC_WIDTH//4, p.y-PIC_HEIGHT//4),
                                            Point(p.x+PIC_WIDTH//4, p.y+PIC_HEIGHT//4))


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, x=0, y=0, width=1, height=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


class ViewInfo:
    def __init__(self, shiftx, shifty, rx, ry):
        self.__shiftx = shiftx
        self.__shifty = shifty
        self.__rx = rx
        self.__ry = ry

    @property
    def shiftx(self):
        return self.__shiftx

    @property
    def shifty(self):
        return self.__shifty

    @property
    def rx(self):
        return self.__rx

    @property
    def ry(self):
        return self.__ry
