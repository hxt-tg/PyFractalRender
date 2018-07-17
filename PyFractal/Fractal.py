from math import sin
from PyQt5.QtGui import QColor, QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from Settings import *
from PyFractal.Complex import Complex
from PyFractal.CalTree import CalTree
import time
from StatusPanel import StatusPanel

FINISHED_SIG = 99999999
COLOR_UPDATE_LINE = QColor(255, 255, 25)
WIDTH_UPDATE_LINE = 2.5


def _get_color(iter_times):
    if iter_times == MAX_ITER:
        return QColor(0, 0, 0)
    else:
        return QColor(((iter_times * 20) % 256), ((iter_times * 15 + 85) % 256), (iter_times * 30 + 171) % 256)


def _get_sin_color(iter_times):
    return (sin(iter_times * 2 * 3.1415926 / 510 - 3.1415926 * 0.5) + 1) * 0.5 * 255


def _get_color2(iter_times):
    if iter_times == MAX_ITER:
        return QColor(0, 0, 0)
    else:
        return QColor(int(_get_sin_color(iter_times * 20)),
                      int(_get_sin_color(iter_times * 15 + 85)),
                      int(_get_sin_color(iter_times * 30 + 171)))


class Fractal:
    last_exp = INIT_EXP
    is_working = False
    pic = None

    def __init__(self, root, exp, boost_graph=False):
        self.__root = root
        self.__boost = boost_graph
        self.caltree = CalTree(exp)
        self.exp = exp
        self.thread0 = None
        self.thread1 = None
        self.pic0 = None
        self.pic1 = None
        self.t = 0
        Fractal.last_exp = INIT_EXP

    def iter_times(self, c):
        i = 0
        while i < MAX_ITER:
            if c.mod >= MAX_MOD:
                break
            c = self.caltree.value_of(c)
            i += 1
        Fractal.last_exp = self.exp
        return i

    def createFractalImage(self, width, height, x0, y0, rx, ry):
        Fractal.is_working = True
        self.t = time.clock()
        color = _get_color2 if self.__boost else _get_color
        self.pic0 = QPixmap(width, height // 2)
        self.pic1 = QPixmap(width, height // 2)
        self.pic0.fill(Qt.white)
        self.pic1.fill(Qt.white)
        self.thread0 = FractalThread(self, width, height, x0, y0, rx, ry, color, self.pic0, 0)
        self.thread0.changeStatus.connect(self.update_status)
        self.thread0.start()
        self.thread1 = FractalThread(self, width, height, x0, y0, rx, ry, color, self.pic1, 1)
        self.thread1.changeStatus.connect(self.update_status)
        self.thread1.start()

    def update_status(self, w0, w1):
        if w0 == FINISHED_SIG or w1 == FINISHED_SIG:
            progress = FINISHED_SIG
        else:
            progress = w0 + w1
        Fractal.pic = QPixmap(PIC_WIDTH, PIC_HEIGHT)
        painter = QPainter()
        painter.begin(Fractal.pic)
        painter.drawPixmap(0, 0, PIC_WIDTH, PIC_HEIGHT // 2, self.pic0)
        painter.drawPixmap(0, PIC_HEIGHT // 2, PIC_WIDTH, PIC_HEIGHT // 2, self.pic1)
        if FractalThread.workers[0] != FINISHED_SIG or FractalThread.workers[1] != FINISHED_SIG:
            h0 = PIC_WIDTH / 2 if w0 == FINISHED_SIG else w0 + 1
            h1 = PIC_WIDTH / 2 if w1 == FINISHED_SIG else (PIC_HEIGHT - w1) - 1
            try:
                painter.setPen(QPen(COLOR_UPDATE_LINE, WIDTH_UPDATE_LINE))
            except Exception as e:
                print(e)
            painter.drawLine(0, h0, PIC_WIDTH, h0)
            painter.drawLine(0, h1, PIC_WIDTH, h1)
        painter.end()
        self.__root.update_pic(Fractal.pic)
        if progress != FINISHED_SIG:
            StatusPanel.set_status('{:.2f}%'.format(progress * 100 / PIC_HEIGHT),
                                   StatusPanel.INFO_PROCESS)
        else:
            if FractalThread.workers[0] != FINISHED_SIG or FractalThread.workers[1] != FINISHED_SIG:
                return
            # Both workers are finished
            StatusPanel.set_status(time.clock()-self.t, StatusPanel.INFO_SUCCESS)
            Fractal.is_working = False


class FractalThread(QThread):
    changePixmap = pyqtSignal(QPixmap)
    changeStatus = pyqtSignal(int, int)
    workers = [0, 0]

    def __init__(self, f, width, height, x0, y0, rx, ry, color_func, pic, wid):
        QThread.__init__(self)
        FractalThread.workers = [0, 0]
        self.t = time.clock()
        self.wid = wid
        self.p = pic
        self.f = f
        self.color_func = color_func
        self.w = width
        self.h = height
        self.x0 = x0
        self.y0 = y0
        self.rx = rx
        self.ry = ry

    def __del__(self):
        self.wait()

    def run(self):
        painter = QPainter()
        painter.begin(self.p)
        z = Complex(0, 0)
        if self.wid == 0:
            rows = range(0, self.h//2+1)
        else:
            rows = range(self.h, self.h//2-1, -1)
        for j in rows:
            for i in range(self.w):
                x = (2 * self.rx) * i / self.w + self.x0 - self.rx
                y = (2 * self.ry) * j / self.h + self.y0 - self.ry
                z.real = x
                z.imag = y
                it = self.f.iter_times(z)
                painter.setPen(self.color_func(it))
                if self.wid:
                    painter.drawPoint(i, j - PIC_HEIGHT//2)
                else:
                    painter.drawPoint(i, j)
            # if time.clock() - self.t > 0.05:
            #     self.changeStatus.emit(FractalThread.workers[0], FractalThread.workers[1])
            # self.t = time.clock()
            if j % FREQ_UPDATE_LINE != 0:
                continue
            if self.wid == 0:
                FractalThread.workers[0] = j
            else:
                FractalThread.workers[1] = (self.h - j)
            try:
                self.changeStatus.emit(FractalThread.workers[0], FractalThread.workers[1])
            except Exception as e:
                print(e)
        painter.end()
        if self.wid == 0:
            self.changeStatus.emit(FINISHED_SIG, FractalThread.workers[1])
        else:
            self.changeStatus.emit(FractalThread.workers[0], FINISHED_SIG)
        FractalThread.workers[self.wid] = FINISHED_SIG
