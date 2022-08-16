from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class PicButton(QAbstractButton):
    def __init__(self, pixmaps, parent=None):
        [pixmap, pixmap_hover] = pixmaps
        pixmap_pressed = pixmap_hover
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        if self.underMouse() and self.isEnabled():
            pix = self.pixmap_hover
        else:
            pix = self.pixmap
        if self.isDown() or self.isChecked():
            pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QSize(200, 200)
    
    def heightForWidth(self, width):
        return width