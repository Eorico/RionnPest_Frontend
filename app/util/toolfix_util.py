# -*- coding: utf-8 -*-
"""
Global custom tooltip system - fixes black tooltip bug on frameless/translucent windows.
Import and call install_custom_tooltips(app) once after creating QApplication.
"""
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QEvent, QPoint, QTimer, QObject
from PyQt5.QtGui import QFont, QFontMetrics, QColor, QPainter, QPainterPath, QPen


class _CustomTooltip(QWidget):
    """
    Standalone tooltip window that paints itself white.
    Bypasses Qt's broken native tooltip rendering on frameless/translucent windows.
    """
    _instance = None

    def __init__(self):
        super().__init__(None, Qt.ToolTip | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)
        self.setWindowFlags(
            Qt.ToolTip
            | Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.BypassGraphicsProxyWidget
        )
        self._text = ""
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.hide)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def show_tip(self, global_pos: QPoint, text: str, duration: int = 3000):
        if not text:
            self.hide()
            return
        self._text = text
        fm = QFontMetrics(QFont("Segoe UI", 9))
        text_rect = fm.boundingRect(text)
        pad_x, pad_y = 14, 8
        w = text_rect.width()  + pad_x * 2
        h = text_rect.height() + pad_y * 2
        self.setFixedSize(w, h)

        screen = QApplication.screenAt(global_pos)
        if screen:
            sr = screen.availableGeometry()
            x = min(global_pos.x() + 12, sr.right()  - w - 4)
            y = min(global_pos.y() + 20, sr.bottom() - h - 4)
        else:
            x = global_pos.x() + 12
            y = global_pos.y() + 20
        self.move(x, y)
        self.show()
        self.raise_()
        self._hide_timer.start(duration)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        
        # White background with green border
        path = QPainterPath()
        path.addRoundedRect(0.5, 0.5,
                            self.width() - 1, self.height() - 1, 6, 6)
        p.setBrush(QColor("#FFFFFF"))
        p.setPen(QPen(QColor("#A8D5BA"), 1.0))
        p.drawPath(path)
        
        # Green text
        p.setPen(QColor("#1B4332"))
        p.setFont(QFont("Segoe UI", 9))
        p.drawText(self.rect(), Qt.AlignCenter, self._text)
        p.end()


class _TooltipEventFilter(QObject):
    """
    Global event filter that intercepts all tooltip events
    and shows our custom white tooltip instead.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.ToolTip:
            widget = obj
            if isinstance(widget, QWidget) and widget.toolTip():
                _CustomTooltip.instance().show_tip(
                    event.globalPos(), widget.toolTip())
            return True  # swallow native tooltip
        if event.type() == QEvent.Leave:
            _CustomTooltip.instance().hide()
        return False


def install_custom_tooltips(app: QApplication):
    """
    Install custom white tooltips globally across the entire application.
    
    Call this ONCE after creating QApplication:
        app = QApplication(sys.argv)
        install_custom_tooltips(app)  # ← Add this line
        
    This fixes black tooltips on frameless/translucent windows by replacing
    Qt's native tooltip rendering with a custom-painted white tooltip widget.
    """
    f = _TooltipEventFilter(app)
    app.installEventFilter(f)
    # Keep reference to prevent garbage collection
    app._tooltip_filter = f