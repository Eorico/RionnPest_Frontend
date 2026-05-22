# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEvent, QPoint, QTimer, pyqtProperty
from PyQt5.QtGui import QFontMetrics, QFont as QGuiFont, QColor, QPainter, QPainterPath, QPen

_G100 = "#C6F6D5"
_G200 = "#74C69D"
_G400 = "#2D6A4F"
_G600 = "#1B4332"
_G800 = "#081C15"

_SURFACE    = "#FFFFFF"
_BG         = "#F4FAF7"
_TEXT       = _G600
_MUTED      = "#6B8F78"
_BORDER     = "#E0EDE6"
_HEADER_BG  = _G400
_SIDEBAR_BG = "#1A3D2B"

class _CustomTooltip(QtWidgets.QWidget):
    _instance = None
    def __init__(self):
        super().__init__(None, QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating, True)
        self.setWindowFlags(QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.BypassGraphicsProxyWidget)
        self._text = ""
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self.hide)

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def show_tip(self, global_pos, text, duration=3000):
        if not text:
            self.hide(); return
        self._text = text
        fm = QFontMetrics(QGuiFont("Segoe UI", 9))
        tr = fm.boundingRect(text)
        px, py = 14, 8
        self.setFixedSize(tr.width() + px*2, tr.height() + py*2)
        screen = QtWidgets.QApplication.screenAt(global_pos)
        if screen:
            sr = screen.availableGeometry()
            x = min(global_pos.x()+12, sr.right()-self.width()-4)
            y = min(global_pos.y()+20, sr.bottom()-self.height()-4)
        else:
            x, y = global_pos.x()+12, global_pos.y()+20
        self.move(x, y); self.show(); self.raise_()
        self._hide_timer.start(duration)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0.5, 0.5, self.width()-1, self.height()-1, 6, 6)
        p.setBrush(QColor("#FFFFFF"))
        p.setPen(QPen(QColor("#A8D5BA"), 1.0))
        p.drawPath(path)
        p.setPen(QColor("#1B4332"))
        p.setFont(QGuiFont("Segoe UI", 9))
        p.drawText(self.rect(), QtCore.Qt.AlignCenter, self._text)
        p.end()

class _TooltipEventFilter(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setVisible(False)
    def eventFilter(self, obj, event):
        if event.type() == QEvent.ToolTip:
            if isinstance(obj, QtWidgets.QWidget) and obj.toolTip():
                _CustomTooltip.instance().show_tip(event.globalPos(), obj.toolTip())
            return True
        if event.type() == QEvent.Leave:
            _CustomTooltip.instance().hide()
        return False

def install_custom_tooltips(target):
    f = _TooltipEventFilter(target)
    target.installEventFilter(f)
    target._tooltip_filter = f

class _ShadowWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, shadow_inset=18, bg="#F4FAF7", corner_r=10):
        super().__init__(parent)
        self._si = shadow_inset
        self._bg = bg
        self._corner_r = corner_r
        self.__opacity = 1.0
        self.setAttribute(QtCore.Qt.WA_StyledBackground, False)
        self.setStyleSheet("background: transparent;")

    def _get_opacity(self):
        return self.__opacity
    def _set_opacity(self, val):
        self.__opacity = max(0.0, min(1.0, val))
        self.update()
    cardOpacity = pyqtProperty(float, _get_opacity, _set_opacity)

    def paintEvent(self, event):
        if self.__opacity <= 0: return
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setOpacity(self.__opacity)
        si = self._si
        card = self.rect().adjusted(si, si, -si, -si)
        for spread, alpha in [(16,0.05),(12,0.07),(8,0.09),(4,0.11),(2,0.08)]:
            sr = card.adjusted(-spread//4, spread//3, spread//4, spread)
            path = QPainterPath()
            path.addRoundedRect(float(sr.x()), float(sr.y()),
                                float(sr.width()), float(sr.height()),
                                float(self._corner_r+2), float(self._corner_r+2))
            p.setBrush(QColor(27, 67, 50, int(alpha*255)))
            p.setPen(QtCore.Qt.NoPen)
            p.drawPath(path)
        card_path = QPainterPath()
        card_path.addRoundedRect(float(card.x()), float(card.y()),
                                 float(card.width()), float(card.height()),
                                 float(self._corner_r), float(self._corner_r))
        p.setBrush(QColor(self._bg))
        p.setPen(QPen(QColor("#E0EDE6"), 0.8))
        p.drawPath(card_path)
        p.end()

_SIDEBAR_HEADER_SS = f"""
QLabel {{ background: #0F2419; color: rgba(198,246,213,0.40);
    font: 600 7pt 'Segoe UI'; letter-spacing: 2px; padding: 8px 14px; border: none; }}
"""
_LIST_SS = f"""
QListWidget {{ background: transparent; color: {_G100}; border: none;
    font: 10pt 'Segoe UI'; outline: none; padding: 4px 0; }}
QListWidget::item {{ padding: 8px 14px; border-radius: 6px; margin: 1px 6px;
    color: rgba(198,246,213,0.70); }}
QListWidget::item:hover {{ background: rgba(255,255,255,0.07); color: {_G100}; }}
QListWidget::item:selected {{ background: rgba(198,246,213,0.14); color: #fff;
    border-left: 3px solid {_G200}; padding-left: 11px; }}
QScrollBar:vertical {{ background: transparent; width: 5px; border-radius: 2px; }}
QScrollBar::handle:vertical {{ background: rgba(198,246,213,0.25); border-radius: 2px; min-height: 20px; }}
QScrollBar::handle:vertical:hover {{ background: rgba(198,246,213,0.45); }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
"""
_SPLITTER_SS = f"""
QSplitter#leftSplitter::handle {{ background: rgba(255,255,255,0.06); height: 1px; }}
QSplitter#leftSplitter::handle:hover {{ background: rgba(198,246,213,0.20); }}
"""
_SCROLL_AREA_SS = f"""
QScrollArea#pageScrollArea {{ background: {_BG}; border: none; }}
QWidget#scrollAreaContent {{ background: {_BG}; }}
QScrollBar:vertical {{ background: transparent; width: 10px; border-radius: 5px; margin: 4px 2px; }}
QScrollBar::handle:vertical {{ background: rgba(45,106,79,0.25); border-radius: 5px; min-height: 30px; }}
QScrollBar::handle:vertical:hover {{ background: rgba(45,106,79,0.40); }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{ background: transparent; height: 10px; border-radius: 5px; margin: 2px 4px; }}
QScrollBar::handle:horizontal {{ background: rgba(45,106,79,0.25); border-radius: 5px; min-width: 30px; }}
QScrollBar::handle:horizontal:hover {{ background: rgba(45,106,79,0.40); }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
"""
_TABLE_SS = f"""
QTableWidget#inventoryTable1 {{
    background: {_SURFACE}; alternate-background-color: {_BG};
    gridline-color: {_BORDER}; color: {_TEXT}; font: 10pt 'Segoe UI';
    border: none; selection-background-color: {_G100}; selection-color: {_TEXT};
}}
QTableWidget#inventoryTable1::item {{ padding: 8px 12px; border: none; }}
QTableWidget#inventoryTable1::item:hover {{ background: #E8F5EE; }}
QTableWidget#inventoryTable1 QHeaderView::section {{
    background: {_G400}; color: #fff; font: 600 9pt 'Segoe UI';
    padding: 10px 14px; border: none; border-right: 1px solid {_G600};
    min-height: 40px;
}}
QTableCornerButton::section {{ background: {_G400}; border: none; }}
QScrollBar:vertical {{ background: {_BG}; width: 6px; border-radius: 3px; }}
QScrollBar::handle:vertical {{ background: {_G200}; border-radius: 3px; min-height: 20px; }}
QScrollBar::handle:vertical:hover {{ background: {_G400}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
"""
_NOTES_SS = f"""
QTextEdit#notesEdit {{ background: {_SURFACE}; color: {_TEXT}; font: 10pt 'Segoe UI';
    border: none; padding: 8px 4px; selection-background-color: {_G100}; }}
QTextEdit#notesEdit:focus {{ border: none; background: {_SURFACE}; }}
"""
_TITLE_BAR_H = 48
_CAPTION_IDLE_SS = f"""
QPushButton {{ background: transparent; color: rgba(255,255,255,0.75); border: none;
    border-radius: 0px; font: 10pt 'Segoe MDL2 Assets','Segoe UI Symbol','Segoe UI',sans-serif;
    min-width: 46px; min-height: {_TITLE_BAR_H}px; max-height: {_TITLE_BAR_H}px; }}
QPushButton:hover {{ background: rgba(255,255,255,0.13); color: #fff; }}
QPushButton:pressed {{ background: rgba(255,255,255,0.22); color: #fff; }}
"""
_CAPTION_CLOSE_SS = f"""
QPushButton {{ background: transparent; color: rgba(255,255,255,0.85); border: none;
    border-radius: 0px; font: 10pt 'Segoe MDL2 Assets','Segoe UI Symbol','Segoe UI',sans-serif;
    min-width: 46px; min-height: {_TITLE_BAR_H}px; max-height: {_TITLE_BAR_H}px; }}
QPushButton:hover {{ background: #C42B1C; color: #fff; }}
QPushButton:pressed {{ background: #A31C12; color: #fff; }}
"""
_TOOLBAR_BTN_SS = f"""
QPushButton {{ background: transparent; color: rgba(198,246,213,0.80);
    border: 1px solid transparent; border-radius: 5px; padding: 3px 10px;
    font: 10pt 'Segoe UI'; min-width: 48px; }}
QPushButton:hover {{ background: rgba(255,255,255,0.12); border-color: rgba(198,246,213,0.28); color: #fff; }}
QPushButton:pressed {{ background: rgba(255,255,255,0.20); }}
"""
_ZOOM_LABEL_SS = f"""
QLabel {{ color: rgba(198,246,213,0.90); font: 600 9pt 'Segoe UI';
    background: rgba(0,0,0,0.15); border-radius: 4px;
    padding: 2px 8px; border: none; min-width: 46px; }}
"""

def _caption_btn(symbol, close=False):
    btn = QtWidgets.QPushButton(symbol)
    btn.setFixedSize(46, _TITLE_BAR_H)
    btn.setFlat(True)
    btn.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    btn.setStyleSheet(_CAPTION_CLOSE_SS if close else _CAPTION_IDLE_SS)
    return btn


class Ui_DocxViewer(object):

    def setupUi(self, DocxViewer):
        DocxViewer.setObjectName("DocxViewer")
        DocxViewer.setMinimumSize(1280, 860)
        DocxViewer.resize(1416, 988)
        DocxViewer.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        DocxViewer.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        DocxViewer.setStyleSheet("QMainWindow { background: transparent; }")

        _SI = 18
        self._shadow_widget = _ShadowWidget(DocxViewer, shadow_inset=_SI, bg=_BG, corner_r=10)
        DocxViewer.setCentralWidget(self._shadow_widget)

        inner_container = QtWidgets.QWidget(self._shadow_widget)
        inner_container.setObjectName("innerContainer")
        inner_container.setStyleSheet("QWidget#innerContainer { background: transparent; border-radius: 10px; }")

        inner_layout = QtWidgets.QVBoxLayout(self._shadow_widget)
        inner_layout.setContentsMargins(_SI, _SI, _SI, _SI)
        inner_layout.setSpacing(0)
        inner_layout.addWidget(inner_container)

        root = QtWidgets.QVBoxLayout(inner_container)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── TITLE BAR ─────────────────────────────────────────────────────────
        self.titleBar = QtWidgets.QFrame()
        self.titleBar.setObjectName("titleBar")
        self.titleBar.setFixedHeight(_TITLE_BAR_H)
        self.titleBar.setStyleSheet(
            f"QFrame#titleBar {{ background: {_HEADER_BG}; border: none; "
            f"border-top-left-radius: 10px; border-top-right-radius: 10px; }}")

        tb_h = QtWidgets.QHBoxLayout(self.titleBar)
        tb_h.setContentsMargins(14, 0, 0, 0)
        tb_h.setSpacing(10)

        icon_pill = QtWidgets.QLabel("📄")
        icon_pill.setFixedSize(30, 30)
        icon_pill.setAlignment(QtCore.Qt.AlignCenter)
        icon_pill.setStyleSheet("background: rgba(255,255,255,0.12); border-radius: 7px; "
                                "font: 14pt 'Segoe UI'; color: #fff; border: none;")
        tb_h.addWidget(icon_pill)

        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(0); title_col.setContentsMargins(0,0,0,0)
        h_title = QtWidgets.QLabel("Document Viewer")
        h_title.setStyleSheet("color: #fff; font: 700 10pt 'Segoe UI'; background: transparent; border: none;")
        h_sub = QtWidgets.QLabel("Raionn Pest Solutions")
        h_sub.setStyleSheet("color: rgba(198,246,213,0.55); font: 8pt 'Segoe UI'; background: transparent; border: none;")
        title_col.addWidget(h_title); title_col.addWidget(h_sub)
        tb_h.addLayout(title_col)
        tb_h.addStretch(1)

        self._minimizeBtn = _caption_btn("—"); self._minimizeBtn.setToolTip("Minimize")
        self._maximizeBtn = _caption_btn("⬜"); self._maximizeBtn.setToolTip("Maximize / Restore")
        self._closeBtn    = _caption_btn("✕", close=True); self._closeBtn.setToolTip("Close")
        tb_h.addWidget(self._minimizeBtn)
        tb_h.addWidget(self._maximizeBtn)
        tb_h.addWidget(self._closeBtn)
        root.addWidget(self.titleBar)

        # ── ACCENT LINE ───────────────────────────────────────────────────────
        accent = QtWidgets.QFrame()
        accent.setFixedHeight(2)
        accent.setStyleSheet(f"background: {_G200}; border: none;")
        root.addWidget(accent)

        # ── MENU BAR (File, View only — Edit and Help removed) ────────────────
        self.menuBarRow = QtWidgets.QFrame()
        self.menuBarRow.setObjectName("menuBarRow")
        self.menuBarRow.setFixedHeight(34)
        self.menuBarRow.setStyleSheet(f"QFrame#menuBarRow {{ background: {_G600}; border: none; }}")

        mb_h = QtWidgets.QHBoxLayout(self.menuBarRow)
        mb_h.setContentsMargins(6, 0, 0, 0)
        mb_h.setSpacing(0)

        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setObjectName("menubar")
        self.menubar.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.menubar.setStyleSheet(f"""
            QMenuBar {{ background: transparent; color: rgba(198,246,213,0.80);
                font: 10pt 'Segoe UI'; padding: 0px; border: none; spacing: 0px; }}
            QMenuBar::item {{ padding: 5px 14px; border-radius: 4px; background: transparent;
                color: rgba(198,246,213,0.75); }}
            QMenuBar::item:selected {{ background: rgba(255,255,255,0.12); color: #fff; }}
            QMenuBar::item:pressed {{ background: rgba(255,255,255,0.20); }}
            QMenu {{ background: {_SURFACE}; color: {_TEXT}; border: 1px solid {_BORDER};
                border-radius: 8px; font: 10pt 'Segoe UI'; padding: 4px 0; }}
            QMenu::item {{ padding: 7px 22px 7px 16px; border-radius: 4px; margin: 1px 4px; }}
            QMenu::item:selected {{ background: {_G400}; color: #fff; }}
            QMenu::separator {{ height: 1px; background: {_BORDER}; margin: 4px 12px; }}
        """)

        self.menuFile = QtWidgets.QMenu("File", self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu("View", self.menubar)
        self.menuView.setObjectName("menuView")
        # ── Edit and Help menus REMOVED ──
        self.menubar.addMenu(self.menuFile)
        self.menubar.addMenu(self.menuView)

        mb_h.addWidget(self.menubar, 0, QtCore.Qt.AlignVCenter)
        mb_h.addStretch(1)
        root.addWidget(self.menuBarRow)

        # ── TOOLBAR ───────────────────────────────────────────────────────────
        self.toolBarRow = QtWidgets.QFrame()
        self.toolBarRow.setObjectName("toolBarRow")
        self.toolBarRow.setFixedHeight(40)
        self.toolBarRow.setStyleSheet(f"""
            QFrame#toolBarRow {{ background: {_G400}; border: none; border-bottom: 1px solid {_G600}; }}
        """)

        tool_h = QtWidgets.QHBoxLayout(self.toolBarRow)
        tool_h.setContentsMargins(10, 0, 10, 0)
        tool_h.setSpacing(4)

        def _tbtn(label, tooltip=""):
            b = QtWidgets.QPushButton(label)
            b.setStyleSheet(_TOOLBAR_BTN_SS)
            b.setFixedHeight(28)
            if tooltip:
                b.setToolTip(tooltip)
            return b

        def _tsep():
            f = QtWidgets.QFrame()
            f.setFrameShape(QtWidgets.QFrame.VLine)
            f.setFixedHeight(18)
            f.setStyleSheet("background: rgba(198,246,213,0.22); border: none; min-width: 1px; max-width: 1px;")
            return f

        self.btnOpen    = _tbtn("📂 Open",   "Open a document file")
        self.btnExport  = _tbtn("Export",    "Export current document")
        self.btnPrint   = _tbtn("Print",     "Print document")

        # Zoom controls
        self.btnZoomOut = _tbtn("−",  "Zoom out  (Ctrl+-)")
        self.btnZoomOut.setFixedWidth(30)
        self.zoomLabel  = QtWidgets.QLabel("100%")
        self.zoomLabel.setStyleSheet(_ZOOM_LABEL_SS)
        self.zoomLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.zoomLabel.setFixedWidth(54)
        self.zoomLabel.setToolTip("Current zoom — click Zoom− / Zoom+ or Ctrl+scroll")
        self.btnZoomIn  = _tbtn("+",  "Zoom in  (Ctrl+=)")
        self.btnZoomIn.setFixedWidth(30)
        self.btnZoom100 = _tbtn("Reset", "Reset zoom to 100%  (Ctrl+0)")
        self.btnZoom100.setFixedWidth(54)

        for w in [
            self.btnOpen, _tsep(),
            self.btnExport, self.btnPrint, _tsep(),
            self.btnZoomOut, self.zoomLabel, self.btnZoomIn, self.btnZoom100,
        ]:
            tool_h.addWidget(w, 0, QtCore.Qt.AlignVCenter)

        tool_h.addStretch(1)
        root.addWidget(self.toolBarRow)

        # ── BODY ──────────────────────────────────────────────────────────────
        body_h = QtWidgets.QHBoxLayout()
        body_h.setContentsMargins(0, 0, 0, 0)
        body_h.setSpacing(0)

        # Sidebar
        sidebar = QtWidgets.QWidget()
        sidebar.setFixedWidth(232)
        sidebar.setStyleSheet(f"background: {_SIDEBAR_BG};")
        sidebar_v = QtWidgets.QVBoxLayout(sidebar)
        sidebar_v.setContentsMargins(0, 0, 0, 0)
        sidebar_v.setSpacing(0)
        self.leftPanelVLayout = sidebar_v

        self.leftSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.leftSplitter.setObjectName("leftSplitter")
        self.leftSplitter.setHandleWidth(1)
        self.leftSplitter.setChildrenCollapsible(False)
        self.leftSplitter.setStyleSheet(_SPLITTER_SS)

        self.filesPanel = QtWidgets.QWidget()
        self.filesPanel.setObjectName("filesPanel")
        self.filesPanel.setMinimumHeight(180)
        self.filesPanel.setStyleSheet(f"background: {_SIDEBAR_BG};")
        files_v = QtWidgets.QVBoxLayout(self.filesPanel)
        files_v.setContentsMargins(0, 0, 0, 0)
        files_v.setSpacing(0)
        self.filesPanelVLayout = files_v
        self.filesPanelHeader = QtWidgets.QLabel("  AVAILABLE FILES")
        self.filesPanelHeader.setObjectName("filesPanelHeader")
        self.filesPanelHeader.setFixedHeight(34)
        self.filesPanelHeader.setStyleSheet(_SIDEBAR_HEADER_SS)
        files_v.addWidget(self.filesPanelHeader)
        self.filesList = QtWidgets.QListWidget()
        self.filesList.setObjectName("filesList")
        self.filesList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.filesList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.filesList.setStyleSheet(_LIST_SS)
        files_v.addWidget(self.filesList)

        self.tocPanel = QtWidgets.QWidget()
        self.tocPanel.setObjectName("tocPanel")
        self.tocPanel.setMinimumHeight(150)
        self.tocPanel.setStyleSheet(f"background: {_SIDEBAR_BG};")
        toc_v = QtWidgets.QVBoxLayout(self.tocPanel)
        toc_v.setContentsMargins(0, 0, 0, 0)
        toc_v.setSpacing(0)
        self.tocPanelVLayout = toc_v
        self.tocPanelHeader = QtWidgets.QLabel("  TABLE OF CONTENTS")
        self.tocPanelHeader.setObjectName("tocPanelHeader")
        self.tocPanelHeader.setFixedHeight(34)
        self.tocPanelHeader.setStyleSheet(_SIDEBAR_HEADER_SS)
        toc_v.addWidget(self.tocPanelHeader)
        self.tocList = QtWidgets.QListWidget()
        self.tocList.setObjectName("tocList")
        self.tocList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tocList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tocList.setStyleSheet(_LIST_SS)
        toc_v.addWidget(self.tocList)

        self.leftSplitter.addWidget(self.filesPanel)
        self.leftSplitter.addWidget(self.tocPanel)
        self.leftSplitter.setSizes([340, 300])
        sidebar_v.addWidget(self.leftSplitter)
        body_h.addWidget(sidebar)

        v_sep = QtWidgets.QFrame()
        v_sep.setFrameShape(QtWidgets.QFrame.VLine)
        v_sep.setFixedWidth(1)
        v_sep.setStyleSheet(f"background: {_G800}; border: none;")
        body_h.addWidget(v_sep)

        # Scroll area
        self.pageScrollArea = QtWidgets.QScrollArea()
        self.pageScrollArea.setObjectName("pageScrollArea")
        self.pageScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.pageScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.pageScrollArea.setWidgetResizable(True)
        self.pageScrollArea.setStyleSheet(_SCROLL_AREA_SS)

        self.scrollAreaContent = QtWidgets.QWidget()
        self.scrollAreaContent.setObjectName("scrollAreaContent")

        outer_h = QtWidgets.QHBoxLayout(self.scrollAreaContent)
        outer_h.setContentsMargins(0, 0, 0, 0)
        outer_h.setSpacing(0)
        outer_h.addStretch(1)

        # Inner container — width controlled by zoom
        self.pageInnerContainer = QtWidgets.QWidget()
        self.pageInnerContainer.setObjectName("pageInnerContainer")
        self.pageInnerContainer.setMaximumWidth(1200)
        self.pageInnerContainer.setStyleSheet("background: transparent;")

        self.scrollContentVLayout = QtWidgets.QVBoxLayout(self.pageInnerContainer)
        self.scrollContentVLayout.setContentsMargins(72, 32, 72, 40)
        self.scrollContentVLayout.setSpacing(32)
        self.scrollContentVLayout.setAlignment(QtCore.Qt.AlignTop)

        outer_h.addWidget(self.pageInnerContainer)
        outer_h.addStretch(1)

        # Page 1
        self.paperPage1 = self._make_page("paperPage1")
        self.paperPage1.setMinimumWidth(900)
        self.paperPage1.setMinimumHeight(900)
        lay1 = QtWidgets.QVBoxLayout(self.paperPage1)
        lay1.setContentsMargins(72, 64, 72, 64)
        lay1.setSpacing(0)
        self.paperLayout1 = lay1

        hdr_block1 = QtWidgets.QWidget()
        hdr_block1.setStyleSheet("background: transparent;")
        hdr_h1 = QtWidgets.QHBoxLayout(hdr_block1)
        hdr_h1.setContentsMargins(0,0,0,0); hdr_h1.setSpacing(14)
        accent_bar = QtWidgets.QFrame()
        accent_bar.setFixedWidth(5)
        accent_bar.setStyleSheet(f"background: {_G400}; border-radius: 3px; border: none;")
        hdr_h1.addWidget(accent_bar)
        hdr_title_col = QtWidgets.QVBoxLayout()
        hdr_title_col.setSpacing(2)
        self.companyName = QtWidgets.QLabel("Raionn Pest Solutions")
        self.companyName.setObjectName("companyName")
        self.companyName.setStyleSheet(f"color: {_TEXT}; font: bold 20pt 'Georgia'; background: transparent;")
        hdr_title_col.addWidget(self.companyName)
        self.companyTagline = QtWidgets.QLabel(
            "Professional Pest Control and Inventory Management  |  raionnpest@gmail.com")
        self.companyTagline.setObjectName("companyTagline")
        self.companyTagline.setStyleSheet(f"color: {_MUTED}; font: 9pt 'Segoe UI'; background: transparent;")
        hdr_title_col.addWidget(self.companyTagline)
        hdr_h1.addLayout(hdr_title_col)
        hdr_h1.addStretch()
        chip = QtWidgets.QLabel("  ACTIVE  ")
        chip.setFixedHeight(24)
        chip.setStyleSheet("QLabel { background: #D1FAE5; color: #065F46; font: bold 8pt 'Segoe UI';"
                           "border-radius: 12px; padding: 0 10px; letter-spacing: 2px; }")
        hdr_h1.addWidget(chip, 0, QtCore.Qt.AlignVCenter)
        lay1.addWidget(hdr_block1)
        lay1.addSpacing(16)
        self.headerDivider = self._make_hline("headerDivider", _G400, 2)
        lay1.addWidget(self.headerDivider)
        lay1.addSpacing(14)

        meta_row = QtWidgets.QHBoxLayout()
        self.docTitleLabel = QtWidgets.QLabel("Inventory Report")
        self.docTitleLabel.setObjectName("docTitleLabel")
        self.docTitleLabel.setStyleSheet(f"color: {_TEXT}; font: bold 14pt 'Segoe UI'; background: transparent;")
        meta_row.addWidget(self.docTitleLabel)
        meta_row.addStretch()
        self.metaLabel = QtWidgets.QLabel("No document loaded")
        self.metaLabel.setObjectName("metaLabel")
        self.metaLabel.setStyleSheet(f"color: {_MUTED}; font: 9pt 'Segoe UI'; background: transparent;")
        self.metaLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        meta_row.addWidget(self.metaLabel)
        lay1.addLayout(meta_row)
        lay1.addSpacing(6)
        self.innerDivider = self._make_hline("innerDivider", _G100, 1)
        lay1.addWidget(self.innerDivider)
        lay1.addSpacing(18)

        self.sectionLabel = self._make_section_lbl(self.paperPage1, "sectionLabel", "Inventory Table")
        lay1.addWidget(self.sectionLabel)
        lay1.addSpacing(10)

        self.inventoryTable1 = self._make_table("inventoryTable1", 10, 7)
        lay1.addWidget(self.inventoryTable1)
        lay1.addSpacing(16)

        self.pageFooter1 = self._make_footer(self.paperPage1, "pageFooter1",
                                             "Raionn Pest Solutions — Confidential", "Page 1 of 2")
        lay1.addWidget(self.pageFooter1)
        self.scrollContentVLayout.addWidget(self.paperPage1)

        # Page 2
        self.paperPage2 = self._make_page("paperPage2")
        self.paperPage2.setMinimumWidth(900)
        self.paperPage2.setMinimumHeight(900)
        lay2 = QtWidgets.QVBoxLayout(self.paperPage2)
        lay2.setContentsMargins(72, 64, 72, 64)
        lay2.setSpacing(0)
        self.paperLayout2 = lay2

        hdr_block2 = QtWidgets.QWidget()
        hdr_block2.setStyleSheet("background: transparent;")
        hdr_h2 = QtWidgets.QHBoxLayout(hdr_block2)
        hdr_h2.setContentsMargins(0,0,0,0); hdr_h2.setSpacing(14)
        accent_bar2 = QtWidgets.QFrame()
        accent_bar2.setFixedWidth(5)
        accent_bar2.setStyleSheet(f"background: {_G400}; border-radius: 3px; border: none;")
        hdr_h2.addWidget(accent_bar2)
        self.companyName2 = QtWidgets.QLabel("Raionn Pest Solutions")
        self.companyName2.setObjectName("companyName2")
        self.companyName2.setStyleSheet(f"color: {_TEXT}; font: bold 14pt 'Georgia'; background: transparent;")
        hdr_h2.addWidget(self.companyName2)
        hdr_h2.addStretch()
        pg2_chip = QtWidgets.QLabel("  Page 2  ")
        pg2_chip.setFixedHeight(22)
        pg2_chip.setStyleSheet(f"QLabel {{ background: {_BG}; color: {_G400}; font: bold 8pt 'Segoe UI';"
                               f"border-radius: 11px; border: 1px solid {_G100}; padding: 0 8px; }}")
        hdr_h2.addWidget(pg2_chip, 0, QtCore.Qt.AlignVCenter)
        lay2.addWidget(hdr_block2)
        lay2.addSpacing(12)
        self.headerDivider2 = self._make_hline("headerDivider2", _G400, 2)
        lay2.addWidget(self.headerDivider2)
        lay2.addSpacing(22)
        self.notesLabel = self._make_section_lbl(self.paperPage2, "notesLabel", "Statement")
        lay2.addWidget(self.notesLabel)
        lay2.addSpacing(10)
        self.notesEdit = QtWidgets.QTextEdit()
        self.notesEdit.setObjectName("notesEdit")
        self.notesEdit.setMinimumHeight(220)
        self.notesEdit.setAcceptRichText(False)
        self.notesEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.notesEdit.setPlaceholderText("Click here to type your notes, observations, or remarks...")
        self.notesEdit.setStyleSheet(_NOTES_SS)
        lay2.addWidget(self.notesEdit)
        lay2.addStretch()
        lay2.addSpacing(12)
        self.pageFooter2 = self._make_footer(self.paperPage2, "pageFooter2",
                                             "Raionn Pest Solutions © 2025 — Confidential", "Page 2 of 2")
        lay2.addWidget(self.pageFooter2)
        self.scrollContentVLayout.addWidget(self.paperPage2)
        self.scrollContentVLayout.addItem(
            QtWidgets.QSpacerItem(20, 32, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed))

        self.pageScrollArea.setWidget(self.scrollAreaContent)
        body_h.addWidget(self.pageScrollArea)

        body_widget = QtWidgets.QWidget()
        body_widget.setObjectName("bodyWidget")
        body_widget.setStyleSheet(f"""
            QWidget#bodyWidget {{ background: {_BG}; border: none;
                border-bottom-left-radius: 10px; border-bottom-right-radius: 10px; }}
        """)
        body_widget.setLayout(body_h)
        root.addWidget(body_widget, 1)

        # ── Actions (File and View only) ──────────────────────────────────────
        for name in ["actionOpen", "actionRefresh", "actionExportPDF",
                     "actionExportDocx", "actionPrint",
                     "actionZoomIn", "actionZoomOut", "actionZoomReset", "actionClose"]:
            a = QtWidgets.QAction(DocxViewer)
            a.setObjectName(name)
            setattr(self, name, a)

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionRefresh)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExportPDF)
        self.menuFile.addAction(self.actionExportDocx)
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuView.addAction(self.actionZoomIn)
        self.menuView.addAction(self.actionZoomOut)
        self.menuView.addAction(self.actionZoomReset)

        # Wire toolbar buttons
        self.btnOpen.clicked.connect(self.actionOpen.trigger)
        self.btnExport.clicked.connect(self.actionExportPDF.trigger)
        self.btnPrint.clicked.connect(self.actionPrint.trigger)
        self.btnZoomIn.clicked.connect(self.actionZoomIn.trigger)
        self.btnZoomOut.clicked.connect(self.actionZoomOut.trigger)
        self.btnZoom100.clicked.connect(self.actionZoomReset.trigger)

        self._apply_rounded_mask(inner_container, 10)
        self._install_drag(DocxViewer)
        self.retranslateUi(DocxViewer)
        QtCore.QMetaObject.connectSlotsByName(DocxViewer)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _apply_rounded_mask(self, widget, radius):
        def apply_mask():
            rect = widget.rect()
            path = QtGui.QPainterPath()
            path.addRoundedRect(QtCore.QRectF(rect), float(radius), float(radius))
            region = QtGui.QRegion(path.toFillPolygon().toPolygon())
            widget.setMask(region)
        apply_mask()
        original_resize = widget.resizeEvent
        def new_resize(event):
            if original_resize: original_resize(event)
            apply_mask()
        widget.resizeEvent = new_resize

    def _make_page(self, obj_name):
        page = QtWidgets.QFrame()
        page.setObjectName(obj_name)
        page.setFrameShape(QtWidgets.QFrame.NoFrame)
        page.setStyleSheet(f"QFrame#{obj_name} {{ background: {_SURFACE}; border-radius: 6px; border: 1px solid {_BORDER}; }}")
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(32); shadow.setOffset(0, 2)
        shadow.setColor(QtGui.QColor(0, 0, 0, 20))
        page.setGraphicsEffect(shadow)
        return page

    def _make_hline(self, obj_name, color, height=1):
        f = QtWidgets.QFrame()
        f.setObjectName(obj_name)
        f.setFrameShape(QtWidgets.QFrame.HLine)
        f.setFrameShadow(QtWidgets.QFrame.Plain)
        f.setFixedHeight(height)
        f.setStyleSheet(f"background: {color}; border: none; max-height: {height}px;")
        return f

    def _make_section_lbl(self, parent, obj_name, text):
        row = QtWidgets.QWidget(parent)
        row.setStyleSheet("background: transparent; border: none;")
        h = QtWidgets.QHBoxLayout(row)
        h.setContentsMargins(0,0,0,0); h.setSpacing(8)
        pip = QtWidgets.QFrame()
        pip.setFixedSize(4, 18)
        pip.setStyleSheet(f"background: {_G200}; border-radius: 2px; border: none;")
        h.addWidget(pip, 0, QtCore.Qt.AlignVCenter)
        lbl = QtWidgets.QLabel(text)
        lbl.setObjectName(obj_name)
        lbl.setStyleSheet(f"color: {_TEXT}; font: bold 11pt 'Segoe UI'; background: transparent; border: none;")
        h.addWidget(lbl)
        h.addStretch()
        return row

    def _make_footer(self, parent, obj_name, left_text, right_text):
        row = QtWidgets.QWidget(parent)
        row.setStyleSheet("background: transparent; border: none;")
        v = QtWidgets.QVBoxLayout(row)
        v.setContentsMargins(0, 8, 0, 0); v.setSpacing(6)
        div = QtWidgets.QFrame()
        div.setFrameShape(QtWidgets.QFrame.HLine)
        div.setFixedHeight(1)
        div.setStyleSheet(f"background: {_G100}; border: none;")
        v.addWidget(div)
        inner = QtWidgets.QHBoxLayout()
        inner.setContentsMargins(0, 0, 0, 0)
        left_lbl = QtWidgets.QLabel(left_text)
        left_lbl.setObjectName(obj_name)
        left_lbl.setStyleSheet(f"color: {_MUTED}; font: 8pt 'Segoe UI'; background: transparent; border: none;")
        inner.addWidget(left_lbl); inner.addStretch()
        right_lbl = QtWidgets.QLabel(right_text)
        right_lbl.setStyleSheet(f"color: {_MUTED}; font: 8pt 'Segoe UI'; background: transparent; border: none;")
        inner.addWidget(right_lbl)
        v.addLayout(inner)
        return row

    def _make_table(self, obj_name, rows, cols):
        tbl = QtWidgets.QTableWidget(rows, cols)
        tbl.setObjectName(obj_name)
        tbl.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        tbl.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        tbl.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        tbl.setMinimumHeight(400)
        tbl.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        tbl.setAlternatingRowColors(True)
        tbl.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        tbl.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        tbl.setShowGrid(True)
        tbl.setWordWrap(True)
        tbl.setStyleSheet(_TABLE_SS)
        for col, txt in enumerate(["Category","Date","Client","Time","Chemicals Used","Actual Chemicals","Remarks"]):
            tbl.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(txt))
        hdr = tbl.horizontalHeader()
        hdr.setDefaultAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        for col in range(cols):
            hdr.setSectionResizeMode(col, QtWidgets.QHeaderView.Interactive)
        hdr.setDefaultSectionSize(160)
        hdr.setMinimumSectionSize(80)
        hdr.setStretchLastSection(True)
        tbl.verticalHeader().setDefaultSectionSize(40)
        tbl.verticalHeader().setVisible(False)
        for r in range(rows):
            for c in range(cols):
                tbl.setItem(r, c, QtWidgets.QTableWidgetItem(""))
        return tbl

    def _install_drag(self, window):
        self._drag_pos = None
        def _press(e):
            if e.button() == QtCore.Qt.LeftButton:
                self._drag_pos = e.globalPos() - window.frameGeometry().topLeft()
        def _move(e):
            if e.buttons() == QtCore.Qt.LeftButton and self._drag_pos is not None:
                window.move(e.globalPos() - self._drag_pos)
        def _release(e): self._drag_pos = None
        self.titleBar.mousePressEvent   = _press
        self.titleBar.mouseMoveEvent    = _move
        self.titleBar.mouseReleaseEvent = _release
        self._closeBtn.clicked.connect(window.close)
        self._minimizeBtn.clicked.connect(window.showMinimized)
        self._maximizeBtn.clicked.connect(
            lambda: window.showNormal() if window.isMaximized() else window.showMaximized())

    def retranslateUi(self, DocxViewer):
        _t = QtCore.QCoreApplication.translate
        DocxViewer.setWindowTitle(_t("DocxViewer", "Raionn Pest Solutions — Document Viewer"))
        self.filesPanelHeader.setText(_t("DocxViewer", "  AVAILABLE FILES"))
        self.tocPanelHeader.setText(_t("DocxViewer", "  TABLE OF CONTENTS"))
        self.companyName.setText(_t("DocxViewer", "Raionn Pest Solutions"))
        self.companyTagline.setText(_t("DocxViewer",
            "Professional Pest Control and Inventory Management  |  raionnpest@gmail.com"))
        self.menuFile.setTitle(_t("DocxViewer", "File"))
        self.menuView.setTitle(_t("DocxViewer", "View"))
        self.actionOpen.setText(_t("DocxViewer", "Open File")); self.actionOpen.setShortcut("Ctrl+O")
        self.actionRefresh.setText(_t("DocxViewer", "Refresh")); self.actionRefresh.setShortcut("F5")
        self.actionExportPDF.setText(_t("DocxViewer", "Export as PDF")); self.actionExportPDF.setShortcut("Ctrl+E")
        self.actionExportDocx.setText(_t("DocxViewer", "Save as DOCX")); self.actionExportDocx.setShortcut("Ctrl+S")
        self.actionPrint.setText(_t("DocxViewer", "Print")); self.actionPrint.setShortcut("Ctrl+P")
        self.actionZoomIn.setText(_t("DocxViewer", "Zoom In")); self.actionZoomIn.setShortcut("Ctrl+=")
        self.actionZoomOut.setText(_t("DocxViewer", "Zoom Out")); self.actionZoomOut.setShortcut("Ctrl+-")
        self.actionZoomReset.setText(_t("DocxViewer", "Reset Zoom")); self.actionZoomReset.setShortcut("Ctrl+0")
        self.actionClose.setText(_t("DocxViewer", "Close")); self.actionClose.setShortcut("Ctrl+W")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    win = QtWidgets.QMainWindow()
    ui = Ui_DocxViewer()
    ui.setupUi(win)
    win.show()
    sys.exit(app.exec_())