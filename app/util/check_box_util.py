from PyQt5.QtGui import QPainter, QPen, QColor as QC, QBrush
from PyQt5.QtCore import QRect, Qt as _Qt
from PyQt5.QtWidgets import QCheckBox
 
class _GreenCheckBox(QCheckBox):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        size  = min(w, h) - 4          # leave a 2 px margin all around
        x     = (w - size) // 2
        y     = (h - size) // 2
        rect  = QRect(x, y, size, size)

        if self.isChecked():
            # ── Filled green box ──────────────────────────────────────────────
            painter.setPen(QPen(QC("#1B4332"), 2))
            painter.setBrush(QBrush(QC("#2D6A4F")))
            painter.drawRoundedRect(rect, 5, 5)

            # ── White checkmark ───────────────────────────────────────────────
            pen = QPen(QC("#FFFFFF"), 2.5)
            pen.setCapStyle(_Qt.RoundCap)
            pen.setJoinStyle(_Qt.RoundJoin)
            painter.setPen(pen)
            painter.setBrush(QBrush())           # no fill

            # Checkmark: short left stroke + long right stroke
            cx, cy = x + size // 2, y + size // 2
            painter.drawLine(
                int(x + size * 0.20), int(y + size * 0.52),
                int(x + size * 0.42), int(y + size * 0.72),
            )
            painter.drawLine(
                int(x + size * 0.42), int(y + size * 0.72),
                int(x + size * 0.80), int(y + size * 0.28),
            )

        else:
            # ── Empty white box with green border ────────────────────────────
            hover = self.underMouse()
            border_color = QC("#1B4332") if hover else QC("#2D6A4F")
            bg_color     = QC("#D6F0E0") if hover else QC("#FFFFFF")

            painter.setPen(QPen(border_color, 2))
            painter.setBrush(QBrush(bg_color))
            painter.drawRoundedRect(rect, 5, 5)

        painter.end()

    def enterEvent(self, event):
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.update()
        super().leaveEvent(event)