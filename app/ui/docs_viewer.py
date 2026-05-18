# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEvent, QPoint, QTimer
from PyQt5.QtGui import QFontMetrics, QFont as QGuiFont, QColor, QPainter, QPainterPath, QPen

# ── Theme tokens ──────────────────────────────────────────────────────────────
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

# ── Custom tooltip (same as recycle bin / edit dialog) ────────────────────────
class _CustomTooltip(QtWidgets.QWidget):
    _instance = None

    def __init__(self):
        super().__init__(None, QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating, True)
        self.setWindowFlags(
            QtCore.Qt.ToolTip | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.BypassGraphicsProxyWidget)
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
        fm = QFontMetrics(QGuiFont("Segoe UI", 9))
        tr = fm.boundingRect(text)
        px, py = 14, 8
        self.setFixedSize(tr.width() + px * 2, tr.height() + py * 2)
        screen = QtWidgets.QApplication.screenAt(global_pos)
        if screen:
            sr = screen.availableGeometry()
            x = min(global_pos.x() + 12, sr.right()  - self.width()  - 4)
            y = min(global_pos.y() + 20, sr.bottom() - self.height() - 4)
        else:
            x, y = global_pos.x() + 12, global_pos.y() + 20
        self.move(x, y)
        self.show()
        self.raise_()
        self._hide_timer.start(duration)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(0.5, 0.5, self.width() - 1, self.height() - 1, 6, 6)
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


# ── Stylesheets ───────────────────────────────────────────────────────────────
_SIDEBAR_HEADER_SS = f"""
QLabel {{
    background: #0F2419;
    color: rgba(198,246,213,0.40);
    font: 600 7pt 'Segoe UI';
    letter-spacing: 2px;
    padding: 8px 14px;
    border: none;
}}
"""

_LIST_SS = f"""
QListWidget {{
    background: transparent;
    color: {_G100};
    border: none;
    font: 10pt 'Segoe UI';
    outline: none;
    padding: 4px 0;
}}
QListWidget::item {{
    padding: 8px 14px;
    border-radius: 6px;
    margin: 1px 6px;
    color: rgba(198,246,213,0.70);
}}
QListWidget::item:hover {{
    background: rgba(255,255,255,0.07);
    color: {_G100};
}}
QListWidget::item:selected {{
    background: rgba(198,246,213,0.14);
    color: #fff;
    border-left: 3px solid {_G200};
    padding-left: 11px;
}}
QScrollBar:vertical {{
    background: transparent; width: 5px; border-radius: 2px;
}}
QScrollBar::handle:vertical {{
    background: rgba(198,246,213,0.25); border-radius: 2px; min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{ background: rgba(198,246,213,0.45); }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
"""

_SPLITTER_SS = f"""
QSplitter#leftSplitter::handle {{
    background: rgba(255,255,255,0.06);
    height: 1px;
}}
QSplitter#leftSplitter::handle:hover {{
    background: rgba(198,246,213,0.20);
}}
"""

_SCROLL_AREA_SS = f"""
QScrollArea#pageScrollArea {{
    background: {_BG};
    border: none;
}}
QWidget#scrollAreaContent {{
    background: {_BG};
}}
QScrollBar:vertical {{
    background: {_BG}; width: 8px; border-radius: 4px; margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: {_G200}; border-radius: 4px; min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{ background: {_G400}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: {_BG}; height: 8px; border-radius: 4px; margin: 2px;
}}
QScrollBar::handle:horizontal {{
    background: {_G200}; border-radius: 4px; min-width: 24px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
"""

_TABLE_SS = f"""
QTableWidget#inventoryTable1,
QTableWidget#inventoryTable2 {{
    background: {_SURFACE};
    alternate-background-color: {_BG};
    gridline-color: {_BORDER};
    color: {_TEXT};
    font: 10pt 'Segoe UI';
    border: none;
    selection-background-color: {_G100};
    selection-color: {_TEXT};
}}
QTableWidget#inventoryTable1::item,
QTableWidget#inventoryTable2::item {{
    padding: 8px 12px;
    border: none;
}}
QTableWidget#inventoryTable1::item:hover,
QTableWidget#inventoryTable2::item:hover {{ background: #E8F5EE; }}
QTableWidget#inventoryTable1 QHeaderView::section,
QTableWidget#inventoryTable2 QHeaderView::section {{
    background: {_G400};
    color: #fff;
    font: 600 9pt 'Segoe UI';
    padding: 9px 12px;
    border: none;
    border-right: 1px solid {_G600};
}}
QTableCornerButton::section {{ background: {_G400}; border: none; }}
QScrollBar:vertical {{
    background: {_BG}; width: 6px; border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {_G200}; border-radius: 3px; min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{ background: {_G400}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
"""

# FIX: Borderless statement editor — no border, no outline, blends into page
_NOTES_SS = f"""
QTextEdit#notesEdit {{
    background: {_SURFACE};
    color: {_TEXT};
    font: 10pt 'Segoe UI';
    border: none;
    padding: 8px 4px;
    selection-background-color: {_G100};
}}
QTextEdit#notesEdit:focus {{
    border: none;
    background: {_SURFACE};
}}
"""

_TITLE_BAR_H = 48

_CAPTION_IDLE_SS = f"""
QPushButton {{
    background: transparent;
    color: rgba(255,255,255,0.75);
    border: none;
    border-radius: 0px;
    font: 10pt 'Segoe MDL2 Assets', 'Segoe UI Symbol', 'Segoe UI', sans-serif;
    min-width: 46px;
    min-height: {_TITLE_BAR_H}px;
    max-height: {_TITLE_BAR_H}px;
}}
QPushButton:hover   {{ background: rgba(255,255,255,0.13); color: #fff; }}
QPushButton:pressed {{ background: rgba(255,255,255,0.22); color: #fff; }}
"""

_CAPTION_CLOSE_SS = f"""
QPushButton {{
    background: transparent;
    color: rgba(255,255,255,0.85);
    border: none;
    border-radius: 0px;
    font: 10pt 'Segoe MDL2 Assets', 'Segoe UI Symbol', 'Segoe UI', sans-serif;
    min-width: 46px;
    min-height: {_TITLE_BAR_H}px;
    max-height: {_TITLE_BAR_H}px;
}}
QPushButton:hover   {{ background: #C42B1C; color: #fff; }}
QPushButton:pressed {{ background: #A31C12; color: #fff; }}
"""

_TOOLBAR_BTN_SS = f"""
QPushButton {{
    background: transparent;
    color: rgba(198,246,213,0.80);
    border: 1px solid transparent;
    border-radius: 5px;
    padding: 3px 10px;
    font: 10pt 'Segoe UI';
    min-width: 48px;
}}
QPushButton:hover {{
    background: rgba(255,255,255,0.12);
    border-color: rgba(198,246,213,0.28);
    color: #fff;
}}
QPushButton:pressed {{
    background: rgba(255,255,255,0.20);
}}
"""


# ── Caption button helper ─────────────────────────────────────────────────────
def _caption_btn(symbol: str, close: bool = False) -> QtWidgets.QPushButton:
    btn = QtWidgets.QPushButton(symbol)
    btn.setFixedSize(46, _TITLE_BAR_H)
    btn.setFlat(True)
    btn.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    btn.setStyleSheet(_CAPTION_CLOSE_SS if close else _CAPTION_IDLE_SS)
    return btn


# ── Main UI class ─────────────────────────────────────────────────────────────
class Ui_DocxViewer(object):

    def setupUi(self, DocxViewer):
        DocxViewer.setObjectName("DocxViewer")
        DocxViewer.setMinimumSize(1280, 860)
        DocxViewer.resize(1416, 988)

        DocxViewer.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        DocxViewer.setAttribute(QtCore.Qt.WA_TranslucentBackground, False)
        DocxViewer.setStyleSheet(
            f"QMainWindow {{ background: {_BG}; }}"
            + _SPLITTER_SS + _SCROLL_AREA_SS + _TABLE_SS + _NOTES_SS
        )

        # Install custom white tooltips
        install_custom_tooltips(DocxViewer)

        cw = QtWidgets.QWidget(DocxViewer)
        cw.setObjectName("centralwidget")
        cw.setStyleSheet(f"background: {_BG};")
        DocxViewer.setCentralWidget(cw)

        root = QtWidgets.QVBoxLayout(cw)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ══════════════════════════════════════════════════════════════════════
        # ROW 1 ── TITLE BAR
        # ══════════════════════════════════════════════════════════════════════
        self.titleBar = QtWidgets.QFrame()
        self.titleBar.setObjectName("titleBar")
        self.titleBar.setFixedHeight(_TITLE_BAR_H)
        self.titleBar.setStyleSheet(
            f"QFrame#titleBar {{ background: {_HEADER_BG}; border: none; }}")

        tb_h = QtWidgets.QHBoxLayout(self.titleBar)
        tb_h.setContentsMargins(14, 0, 0, 0)
        tb_h.setSpacing(10)

        icon_pill = QtWidgets.QLabel("📄")
        icon_pill.setFixedSize(30, 30)
        icon_pill.setAlignment(QtCore.Qt.AlignCenter)
        icon_pill.setStyleSheet(
            "background: rgba(255,255,255,0.12); border-radius: 7px; "
            "font: 14pt 'Segoe UI'; color: #fff; border: none;")
        tb_h.addWidget(icon_pill)

        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(0)
        title_col.setContentsMargins(0, 0, 0, 0)
        h_title = QtWidgets.QLabel("Document Viewer")
        h_title.setStyleSheet(
            "color: #fff; font: 700 10pt 'Segoe UI'; "
            "background: transparent; border: none;")
        h_sub = QtWidgets.QLabel("Raionn Pest Solutions — Report Archive")
        h_sub.setStyleSheet(
            "color: rgba(198,246,213,0.55); font: 8pt 'Segoe UI'; "
            "background: transparent; border: none;")
        title_col.addWidget(h_title)
        title_col.addWidget(h_sub)
        tb_h.addLayout(title_col)

        tb_h.addStretch(1)

        # Full-height Windows caption buttons
        self._minimizeBtn = _caption_btn("—")
        self._minimizeBtn.setToolTip("Minimize")
        self._maximizeBtn = _caption_btn("⬜")
        self._maximizeBtn.setToolTip("Maximize / Restore")
        self._closeBtn    = _caption_btn("✕", close=True)
        self._closeBtn.setToolTip("Close")
        tb_h.addWidget(self._minimizeBtn)
        tb_h.addWidget(self._maximizeBtn)
        tb_h.addWidget(self._closeBtn)

        root.addWidget(self.titleBar)

        # ══════════════════════════════════════════════════════════════════════
        # ROW 2 ── ACCENT LINE
        # ══════════════════════════════════════════════════════════════════════
        accent = QtWidgets.QFrame()
        accent.setFixedHeight(2)
        accent.setStyleSheet(f"background: {_G200}; border: none;")
        root.addWidget(accent)

        # ══════════════════════════════════════════════════════════════════════
        # ROW 3 ── CUSTOM MENU BAR
        # ══════════════════════════════════════════════════════════════════════
        self.menuBarRow = QtWidgets.QFrame()
        self.menuBarRow.setObjectName("menuBarRow")
        self.menuBarRow.setFixedHeight(34)
        self.menuBarRow.setStyleSheet(
            f"QFrame#menuBarRow {{ background: {_G600}; border: none; }}")

        mb_h = QtWidgets.QHBoxLayout(self.menuBarRow)
        mb_h.setContentsMargins(6, 0, 0, 0)
        mb_h.setSpacing(0)

        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setObjectName("menubar")
        self.menubar.setSizePolicy(
            QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Preferred)
        self.menubar.setStyleSheet(f"""
            QMenuBar {{
                background: transparent;
                color: rgba(198,246,213,0.80);
                font: 10pt 'Segoe UI';
                padding: 0px;
                border: none;
                spacing: 0px;
            }}
            QMenuBar::item {{
                padding: 5px 14px;
                border-radius: 4px;
                background: transparent;
                color: rgba(198,246,213,0.75);
            }}
            QMenuBar::item:selected {{
                background: rgba(255,255,255,0.12);
                color: #fff;
            }}
            QMenuBar::item:pressed {{
                background: rgba(255,255,255,0.20);
            }}
            QMenu {{
                background: {_SURFACE};
                color: {_TEXT};
                border: 1px solid {_BORDER};
                border-radius: 8px;
                font: 10pt 'Segoe UI';
                padding: 4px 0;
            }}
            QMenu::item {{
                padding: 7px 22px 7px 16px;
                border-radius: 4px;
                margin: 1px 4px;
            }}
            QMenu::item:selected {{
                background: {_G400};
                color: #fff;
            }}
            QMenu::separator {{
                height: 1px;
                background: {_BORDER};
                margin: 4px 12px;
            }}
        """)

        self.menuFile = QtWidgets.QMenu("File", self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu("View", self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuEdit = QtWidgets.QMenu("Edit", self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu("Help", self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.menubar.addMenu(self.menuFile)
        self.menubar.addMenu(self.menuView)
        self.menubar.addMenu(self.menuEdit)
        self.menubar.addMenu(self.menuHelp)

        mb_h.addWidget(self.menubar, 0, QtCore.Qt.AlignVCenter)
        mb_h.addStretch(1)

        root.addWidget(self.menuBarRow)

        # ══════════════════════════════════════════════════════════════════════
        # ROW 4 ── TOOLBAR   Export Print | Zoom… (Open, Refresh, Find removed)
        # ══════════════════════════════════════════════════════════════════════
        self.toolBarRow = QtWidgets.QFrame()
        self.toolBarRow.setObjectName("toolBarRow")
        self.toolBarRow.setFixedHeight(38)
        self.toolBarRow.setStyleSheet(f"""
            QFrame#toolBarRow {{
                background: {_G400};
                border: none;
                border-bottom: 1px solid {_G600};
            }}
        """)

        tool_h = QtWidgets.QHBoxLayout(self.toolBarRow)
        tool_h.setContentsMargins(10, 0, 10, 0)
        tool_h.setSpacing(2)

        def _tbtn(label: str) -> QtWidgets.QPushButton:
            b = QtWidgets.QPushButton(label)
            b.setStyleSheet(_TOOLBAR_BTN_SS)
            b.setFixedHeight(28)
            return b

        def _tsep() -> QtWidgets.QFrame:
            f = QtWidgets.QFrame()
            f.setFrameShape(QtWidgets.QFrame.VLine)
            f.setFixedHeight(18)
            f.setStyleSheet(
                "background: rgba(198,246,213,0.22); "
                "border: none; min-width: 1px; max-width: 1px;")
            return f

        # Kept buttons only: Export, Print, Zoom+, Zoom−, 100%
        self.btnExport  = _tbtn("Export")
        self.btnPrint   = _tbtn("Print")
        self.btnZoomIn  = _tbtn("Zoom +")
        self.btnZoomOut = _tbtn("Zoom −")
        self.btnZoom100 = _tbtn("100%")

        for w in [
            self.btnExport, self.btnPrint, _tsep(),
            self.btnZoomIn, self.btnZoomOut, self.btnZoom100,
        ]:
            tool_h.addWidget(w, 0, QtCore.Qt.AlignVCenter)

        tool_h.addStretch(1)
        root.addWidget(self.toolBarRow)

        # ══════════════════════════════════════════════════════════════════════
        # ROW 5 ── BODY   sidebar | vsep | document scroll area
        # ══════════════════════════════════════════════════════════════════════
        body_h = QtWidgets.QHBoxLayout()
        body_h.setContentsMargins(0, 0, 0, 0)
        body_h.setSpacing(0)

        # ── Left sidebar ──────────────────────────────────────────────────────
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

        # Files panel
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

        # ToC panel
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

        # ── Document scroll area ──────────────────────────────────────────────
        self.pageScrollArea = QtWidgets.QScrollArea()
        self.pageScrollArea.setObjectName("pageScrollArea")
        self.pageScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.pageScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.pageScrollArea.setWidgetResizable(True)

        self.scrollAreaContent = QtWidgets.QWidget()
        self.scrollAreaContent.setObjectName("scrollAreaContent")

        self.scrollContentVLayout = QtWidgets.QVBoxLayout(self.scrollAreaContent)
        self.scrollContentVLayout.setContentsMargins(0, 32, 0, 40)
        self.scrollContentVLayout.setSpacing(32)
        self.scrollContentVLayout.setAlignment(QtCore.Qt.AlignHCenter)

        # ── Page 1 ────────────────────────────────────────────────────────────
        self.paperPage1 = self._make_page("paperPage1")
        self.paperPage1.setFixedSize(794, 1123)
        lay1 = QtWidgets.QVBoxLayout(self.paperPage1)
        lay1.setContentsMargins(72, 64, 72, 64)
        lay1.setSpacing(0)
        self.paperLayout1 = lay1

        hdr_block1 = QtWidgets.QWidget()
        hdr_block1.setStyleSheet("background: transparent;")
        hdr_h1 = QtWidgets.QHBoxLayout(hdr_block1)
        hdr_h1.setContentsMargins(0, 0, 0, 0)
        hdr_h1.setSpacing(14)

        accent_bar = QtWidgets.QFrame()
        accent_bar.setFixedWidth(5)
        accent_bar.setStyleSheet(
            f"background: {_G400}; border-radius: 3px; border: none;")
        hdr_h1.addWidget(accent_bar)

        hdr_title_col = QtWidgets.QVBoxLayout()
        hdr_title_col.setSpacing(2)

        self.companyName = QtWidgets.QLabel("Raionn Pest Solutions")
        self.companyName.setObjectName("companyName")
        self.companyName.setStyleSheet(
            f"color: {_TEXT}; font: bold 20pt 'Georgia'; background: transparent;")
        hdr_title_col.addWidget(self.companyName)

        self.companyTagline = QtWidgets.QLabel(
            "Professional Pest Control and Inventory Management"
            "  |  raionnpest@gmail.com")
        self.companyTagline.setObjectName("companyTagline")
        self.companyTagline.setStyleSheet(
            f"color: {_MUTED}; font: 9pt 'Segoe UI'; background: transparent;")
        hdr_title_col.addWidget(self.companyTagline)

        hdr_h1.addLayout(hdr_title_col)
        hdr_h1.addStretch()
 
        lay1.addWidget(hdr_block1)

        lay1.addSpacing(16)
        self.headerDivider = self._make_hline("headerDivider", _G400, 2)
        lay1.addWidget(self.headerDivider)
        lay1.addSpacing(14)

        meta_row = QtWidgets.QHBoxLayout()
        self.docTitleLabel = QtWidgets.QLabel("Inventory Report — Q1 2025")
        self.docTitleLabel.setObjectName("docTitleLabel")
        self.docTitleLabel.setStyleSheet(
            f"color: {_TEXT}; font: bold 14pt 'Segoe UI'; background: transparent;")
        meta_row.addWidget(self.docTitleLabel)
        meta_row.addStretch()

       
     
        lay1.addLayout(meta_row)

        lay1.addSpacing(6)
        self.innerDivider = self._make_hline("innerDivider", _G100, 1)
        lay1.addWidget(self.innerDivider)
        lay1.addSpacing(18)

        self.sectionLabel = self._make_section_lbl(
            self.paperPage1, "sectionLabel", "Inventory Table")
        lay1.addWidget(self.sectionLabel)
        lay1.addSpacing(10)

        self.inventoryTable1 = self._make_table("inventoryTable1", 10, 6)
        lay1.addWidget(self.inventoryTable1)
        lay1.addSpacing(16)

        self.pageFooter1 = self._make_footer(
            self.paperPage1, "pageFooter1",
            "Raionn Pest Solutions — Confidential", "Page 1 of 2")
        lay1.addWidget(self.pageFooter1)

        self.scrollContentVLayout.addWidget(self.paperPage1)

        # ── Page 2 ────────────────────────────────────────────────────────────
        self.paperPage2 = self._make_page("paperPage2")
        self.paperPage2.setFixedSize(794, 1123)
        lay2 = QtWidgets.QVBoxLayout(self.paperPage2)
        lay2.setContentsMargins(72, 64, 72, 64)
        lay2.setSpacing(0)
        self.paperLayout2 = lay2

        hdr_block2 = QtWidgets.QWidget()
        hdr_block2.setStyleSheet("background: transparent;")
        hdr_h2 = QtWidgets.QHBoxLayout(hdr_block2)
        hdr_h2.setContentsMargins(0, 0, 0, 0)
        hdr_h2.setSpacing(14)

        accent_bar2 = QtWidgets.QFrame()
        accent_bar2.setFixedWidth(5)
        accent_bar2.setStyleSheet(
            f"background: {_G400}; border-radius: 3px; border: none;")
        hdr_h2.addWidget(accent_bar2)

        self.companyName2 = QtWidgets.QLabel("Raionn Pest Solutions")
        self.companyName2.setObjectName("companyName2")
        self.companyName2.setStyleSheet(
            f"color: {_TEXT}; font: bold 14pt 'Georgia'; background: transparent;")
        hdr_h2.addWidget(self.companyName2)
        hdr_h2.addStretch()

        pg2_chip = QtWidgets.QLabel("  Page 2  ")
        pg2_chip.setFixedHeight(22)
        pg2_chip.setStyleSheet(f"""
            QLabel {{
                background: {_BG}; color: {_G400};
                font: bold 8pt 'Segoe UI'; border-radius: 11px;
                border: 1px solid {_G100}; padding: 0 8px;
            }}
        """)
        hdr_h2.addWidget(pg2_chip, 0, QtCore.Qt.AlignVCenter)
        lay2.addWidget(hdr_block2)

        lay2.addSpacing(12)
        self.headerDivider2 = self._make_hline("headerDivider2", _G400, 2)
        lay2.addWidget(self.headerDivider2)
        lay2.addSpacing(22)

        self.notesLabel = self._make_section_lbl(
            self.paperPage2, "notesLabel", "Statement")
        lay2.addWidget(self.notesLabel)
        lay2.addSpacing(10)

        # FIX: Borderless text editor — blends into the page like MS Word
        self.notesEdit = QtWidgets.QTextEdit()
        self.notesEdit.setObjectName("notesEdit")
        self.notesEdit.setMinimumHeight(220)
        self.notesEdit.setAcceptRichText(False)
        self.notesEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.notesEdit.setPlaceholderText(
            "Click here to type your notes, observations, "
            "or remarks for this report...")
        self.notesEdit.setStyleSheet(_NOTES_SS)
        lay2.addWidget(self.notesEdit)
        lay2.addStretch()
        lay2.addSpacing(12)

        self.pageFooter2 = self._make_footer(
            self.paperPage2, "pageFooter2",
            "Raionn Pest Solutions © 2025 — Confidential", "Page 2 of 2")
        lay2.addWidget(self.pageFooter2)

        self.scrollContentVLayout.addWidget(self.paperPage2)
        self.scrollContentVLayout.addItem(
            QtWidgets.QSpacerItem(
                20, 32,
                QtWidgets.QSizePolicy.Minimum,
                QtWidgets.QSizePolicy.Fixed))

        self.pageScrollArea.setWidget(self.scrollAreaContent)
        body_h.addWidget(self.pageScrollArea)

        body_widget = QtWidgets.QWidget()
        body_widget.setStyleSheet(f"background: {_BG};")
        body_widget.setLayout(body_h)
        root.addWidget(body_widget, 1)

        # ══════════════════════════════════════════════════════════════════════
        # ROW 6 ── STATUS BAR
        # ══════════════════════════════════════════════════════════════════════
        self.statusbar = QtWidgets.QStatusBar(DocxViewer)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setStyleSheet(f"""
            QStatusBar {{
                background: {_G600};
                color: rgba(198,246,213,0.55);
                font: 8pt 'Segoe UI';
                border-top: 1px solid {_G800};
                padding: 2px 10px;
            }}
            QStatusBar::item {{ border: none; }}
        """)
        DocxViewer.setStatusBar(self.statusbar)

        # ── Actions ───────────────────────────────────────────────────────────
        for name in [
            "actionOpen", "actionRefresh", "actionExport", "actionPrint",
            "actionZoomIn", "actionZoomOut", "actionZoomReset",
            "actionFind", "actionClose", "actionAbout",
        ]:
            a = QtWidgets.QAction(DocxViewer)
            a.setObjectName(name)
            setattr(self, name, a)

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionRefresh)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addAction(self.actionPrint)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuView.addAction(self.actionZoomIn)
        self.menuView.addAction(self.actionZoomOut)
        self.menuView.addAction(self.actionZoomReset)
        self.menuEdit.addAction(self.actionFind)
        self.menuHelp.addAction(self.actionAbout)

        # Wire toolbar buttons → actions (only the ones still in the toolbar)
        self.btnExport.clicked.connect(self.actionExport.trigger)
        self.btnPrint.clicked.connect(self.actionPrint.trigger)
        self.btnZoomIn.clicked.connect(self.actionZoomIn.trigger)
        self.btnZoomOut.clicked.connect(self.actionZoomOut.trigger)
        self.btnZoom100.clicked.connect(self.actionZoomReset.trigger)

        self._install_drag(DocxViewer)
        self.retranslateUi(DocxViewer)
        QtCore.QMetaObject.connectSlotsByName(DocxViewer)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _make_page(self, obj_name: str) -> QtWidgets.QFrame:
        page = QtWidgets.QFrame()
        page.setObjectName(obj_name)
        page.setFrameShape(QtWidgets.QFrame.NoFrame)
        page.setStyleSheet(f"""
            QFrame#{obj_name} {{
                background: {_SURFACE};
                border-radius: 6px;
                border: 1px solid {_BORDER};
            }}
        """)
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 4)
        shadow.setColor(QtGui.QColor(0, 0, 0, 35))
        page.setGraphicsEffect(shadow)
        return page

    def _make_hline(self, obj_name: str, color: str,
                    height: int = 1) -> QtWidgets.QFrame:
        f = QtWidgets.QFrame()
        f.setObjectName(obj_name)
        f.setFrameShape(QtWidgets.QFrame.HLine)
        f.setFrameShadow(QtWidgets.QFrame.Plain)
        f.setFixedHeight(height)
        f.setStyleSheet(
            f"background: {color}; border: none; max-height: {height}px;")
        return f

    def _make_section_lbl(self, parent, obj_name: str,
                          text: str) -> QtWidgets.QWidget:
        row = QtWidgets.QWidget(parent)
        row.setStyleSheet("background: transparent; border: none;")
        h = QtWidgets.QHBoxLayout(row)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(8)

        pip = QtWidgets.QFrame()
        pip.setFixedSize(4, 18)
        pip.setStyleSheet(
            f"background: {_G200}; border-radius: 2px; border: none;")
        h.addWidget(pip, 0, QtCore.Qt.AlignVCenter)

        lbl = QtWidgets.QLabel(text)
        lbl.setObjectName(obj_name)
        lbl.setStyleSheet(
            f"color: {_TEXT}; font: bold 11pt 'Segoe UI'; "
            "background: transparent; border: none;")
        h.addWidget(lbl)
        h.addStretch()
        return row

    def _make_footer(self, parent, obj_name: str,
                     left_text: str, right_text: str) -> QtWidgets.QWidget:
        row = QtWidgets.QWidget(parent)
        row.setStyleSheet("background: transparent; border: none;")
        v = QtWidgets.QVBoxLayout(row)
        v.setContentsMargins(0, 8, 0, 0)
        v.setSpacing(6)

        div = QtWidgets.QFrame()
        div.setFrameShape(QtWidgets.QFrame.HLine)
        div.setFixedHeight(1)
        div.setStyleSheet(f"background: {_G100}; border: none;")
        v.addWidget(div)

        inner = QtWidgets.QHBoxLayout()
        inner.setContentsMargins(0, 0, 0, 0)

        left_lbl = QtWidgets.QLabel(left_text)
        left_lbl.setObjectName(obj_name)
        left_lbl.setStyleSheet(
            f"color: {_MUTED}; font: 8pt 'Segoe UI'; "
            "background: transparent; border: none;")
        inner.addWidget(left_lbl)
        inner.addStretch()

        right_lbl = QtWidgets.QLabel(right_text)
        right_lbl.setStyleSheet(
            f"color: {_MUTED}; font: 8pt 'Segoe UI'; "
            "background: transparent; border: none;")
        inner.addWidget(right_lbl)
        v.addLayout(inner)
        return row

    def _make_table(self, obj_name: str, rows: int,
                    cols: int) -> QtWidgets.QTableWidget:
        tbl = QtWidgets.QTableWidget(rows, cols)
        tbl.setObjectName(obj_name)
        tbl.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        tbl.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        tbl.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding)
        tbl.setMinimumHeight(400)
        tbl.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        tbl.setAlternatingRowColors(True)
        tbl.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        tbl.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        tbl.setShowGrid(True)
        tbl.setGridStyle(QtCore.Qt.SolidLine)
        tbl.setStyleSheet(_TABLE_SS)

        for col, txt in enumerate([
            "Date of Treatment", "Name of Client", "Time of Treatment",
            "Chemical/s Used", "Actual Chemical/s Used", "Remarks",
        ]):
            tbl.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(txt))

        hdr = tbl.horizontalHeader()
        for col in range(6):
            hdr.setSectionResizeMode(col, QtWidgets.QHeaderView.Stretch)

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
                self._drag_pos = (
                    e.globalPos() - window.frameGeometry().topLeft())

        def _move(e):
            if (e.buttons() == QtCore.Qt.LeftButton
                    and self._drag_pos is not None):
                window.move(e.globalPos() - self._drag_pos)

        def _release(e):
            self._drag_pos = None

        self.titleBar.mousePressEvent   = _press
        self.titleBar.mouseMoveEvent    = _move
        self.titleBar.mouseReleaseEvent = _release

        self._closeBtn.clicked.connect(window.close)
        self._minimizeBtn.clicked.connect(window.showMinimized)
        self._maximizeBtn.clicked.connect(
            lambda: window.showNormal()
            if window.isMaximized() else window.showMaximized())

    def retranslateUi(self, DocxViewer):
        _t = QtCore.QCoreApplication.translate

        DocxViewer.setWindowTitle(
            _t("DocxViewer", "Raionn Pest Solutions — Document Viewer"))

        self.filesPanelHeader.setText(_t("DocxViewer", "  AVAILABLE FILES"))
        self.tocPanelHeader.setText(_t("DocxViewer", "  TABLE OF CONTENTS"))

        self.companyName.setText(_t("DocxViewer", "Raionn Pest Solutions"))
        self.companyTagline.setText(
            _t("DocxViewer",
               "Professional Pest Control and Inventory Management"
               "  |  raionnpest@gmail.com"))
        self.docTitleLabel.setText(
            _t("DocxViewer", "Inventory Report — Q1 2025"))
     

        for col, txt in enumerate([
            "Date of Treatment", "Name of Client", "Time of Treatment",
            "Chemical/s Used", "Actual Chemical/s Used", "Remarks",
        ]):
            h_item = self.inventoryTable1.horizontalHeaderItem(col)
            if h_item:
                h_item.setText(_t("DocxViewer", txt))
        self.inventoryTable1.setSortingEnabled(True)

        self.companyName2.setText(_t("DocxViewer", "Raionn Pest Solutions"))
        self.notesEdit.setPlaceholderText(
            _t("DocxViewer",
               "Click here to type your notes, observations, "
               "or remarks for this report..."))

        self.menuFile.setTitle(_t("DocxViewer", "File"))
        self.menuView.setTitle(_t("DocxViewer", "View"))
        self.menuEdit.setTitle(_t("DocxViewer", "Edit"))
        self.menuHelp.setTitle(_t("DocxViewer", "Help"))

        self.actionOpen.setText(_t("DocxViewer", "Open"))
        self.actionOpen.setShortcut(_t("DocxViewer", "Ctrl+O"))
        self.actionRefresh.setText(_t("DocxViewer", "Refresh"))
        self.actionRefresh.setShortcut(_t("DocxViewer", "F5"))
        self.actionExport.setText(_t("DocxViewer", "Export"))
        self.actionExport.setShortcut(_t("DocxViewer", "Ctrl+E"))
        self.actionPrint.setText(_t("DocxViewer", "Print"))
        self.actionPrint.setShortcut(_t("DocxViewer", "Ctrl+P"))
        self.actionZoomIn.setText(_t("DocxViewer", "Zoom In"))
        self.actionZoomIn.setShortcut(_t("DocxViewer", "Ctrl+="))
        self.actionZoomOut.setText(_t("DocxViewer", "Zoom Out"))
        self.actionZoomOut.setShortcut(_t("DocxViewer", "Ctrl+-"))
        self.actionZoomReset.setText(_t("DocxViewer", "Reset Zoom"))
        self.actionZoomReset.setShortcut(_t("DocxViewer", "Ctrl+0"))
        self.actionFind.setText(_t("DocxViewer", "Find"))
        self.actionFind.setShortcut(_t("DocxViewer", "Ctrl+F"))
        self.actionClose.setText(_t("DocxViewer", "Close"))
        self.actionClose.setShortcut(_t("DocxViewer", "Ctrl+W"))
        self.actionAbout.setText(_t("DocxViewer", "About"))

        self.btnExport.setText(_t("DocxViewer", "Export"))
        self.btnPrint.setText(_t("DocxViewer", "Print"))
        self.btnZoomIn.setText(_t("DocxViewer", "Zoom +"))
        self.btnZoomOut.setText(_t("DocxViewer", "Zoom −"))
        self.btnZoom100.setText(_t("DocxViewer", "100%"))


# ── Standalone preview ────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    win = QtWidgets.QMainWindow()
    ui = Ui_DocxViewer()
    ui.setupUi(win)
    win.show()
    sys.exit(app.exec_())