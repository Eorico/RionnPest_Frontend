# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

# ── Shared theme tokens (mirrors dashboard palette) ───────────────────────────
_G50   = "#F0FAF4"
_G100  = "#C6F6D5"
_G200  = "#74C69D"
_G400  = "#2D6A4F"
_G600  = "#1B4332"
_G800  = "#081C15"

_SURFACE    = "#FFFFFF"
_BG         = "#F4FAF7"
_TEXT       = _G600
_MUTED      = "#6B8F78"
_BORDER     = "#E0EDE6"
_HEADER_BG  = _G400

# ── Stylesheet blocks (identical to actual chemical viewer) ───────────────────
_TABLE_SS = f"""
QTableWidget {{
    background: {_SURFACE};
    alternate-background-color: {_BG};
    gridline-color: {_BORDER};
    border: none;
    font: 10pt 'Segoe UI';
    color: {_TEXT};
    selection-background-color: {_G100};
    selection-color: {_TEXT};
}}
QTableWidget::item {{
    padding: 10px 14px;
    border: none;
    color: {_TEXT};
}}
QTableWidget::item:hover    {{ background: #E8F5EE; }}
QTableWidget::item:selected {{ background: {_G100}; color: {_TEXT}; }}
QHeaderView::section {{
    background: {_G400};
    color: #fff;
    border: none;
    border-right: 1px solid {_G600};
    padding: 10px 14px;
    font: 600 10pt 'Segoe UI';
    letter-spacing: 0.3px;
}}
QHeaderView::section:vertical {{
    background: {_BG};
    color: {_MUTED};
    border-right: 1px solid {_BORDER};
    font: 9pt 'Segoe UI';
    padding: 4px;
}}
QHeaderView {{ background: transparent; border: none; }}
QTableCornerButton::section {{ background: {_G400}; border: none; }}
QScrollBar:vertical {{
    background: {_BG}; width: 6px; border-radius: 3px; margin: 2px;
}}
QScrollBar::handle:vertical {{
    background: {_G200}; border-radius: 3px; min-height: 20px;
}}
QScrollBar::handle:vertical:hover  {{ background: {_G400}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{
    background: {_BG}; height: 6px; border-radius: 3px; margin: 2px;
}}
QScrollBar::handle:horizontal {{
    background: {_G200}; border-radius: 3px; min-width: 20px;
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
"""

_ADD_BTN_SS = f"""
QPushButton {{
    background: transparent;
    color: {_G400};
    border: 1.5px dashed {_G400};
    border-radius: 8px;
    padding: 8px 18px;
    font: 500 10pt 'Segoe UI';
}}
QPushButton:hover   {{ background: {_G100}; border-color: {_G600}; color: {_G600}; }}
QPushButton:pressed {{ background: {_G100}; }}
"""

_DEL_BTN_SS = """
QPushButton {
    background: transparent;
    color: #DC2626;
    border: 1.5px dashed rgba(220,38,38,0.45);
    border-radius: 8px;
    padding: 8px 18px;
    font: 500 10pt 'Segoe UI';
}
QPushButton:hover   { background: rgba(220,38,38,0.06); border-color: #DC2626; }
QPushButton:pressed { background: rgba(220,38,38,0.12); }
"""

_UNDO_BTN_SS = f"""
QPushButton {{
    background: transparent;
    color: {_MUTED};
    border: 1.5px solid {_BORDER};
    border-radius: 8px;
    padding: 8px 18px;
    font: 500 10pt 'Segoe UI';
}}
QPushButton:hover   {{ background: {_BG}; border-color: {_G200}; color: {_TEXT}; }}
QPushButton:pressed {{ background: {_G100}; border-color: {_G400}; color: {_G400}; }}
QPushButton:disabled {{ color: rgba(107,143,120,0.35); border-color: {_BORDER}; }}
"""

_DONE_BTN_SS = f"""
QPushButton {{
    background: {_G400};
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 8px 24px;
    font: 600 10pt 'Segoe UI';
}}
QPushButton:hover   {{ background: {_G600}; }}
QPushButton:pressed {{ background: {_G800}; }}
"""

_CAPTION_IDLE_SS = """
QPushButton {
    background: transparent;
    color: rgba(255,255,255,0.70);
    border: none;
    border-radius: 0px;
    font: 11pt 'Segoe MDL2 Assets', 'Segoe UI Symbol', 'Arial';
}
QPushButton:hover   { background: rgba(255,255,255,0.12); color: #fff; }
QPushButton:pressed { background: rgba(255,255,255,0.20); }
"""

_CAPTION_CLOSE_SS = """
QPushButton {
    background: transparent;
    color: rgba(255,255,255,0.80);
    border: none;
    border-radius: 0px;
    font: 11pt 'Segoe MDL2 Assets', 'Segoe UI Symbol', 'Arial';
}
QPushButton:hover   { background: #C42B1C; color: #fff; }
QPushButton:pressed { background: #B01F13; }
"""

_LABEL_MUTED_SS = (
    f"color: {_MUTED}; font: 600 8pt 'Segoe UI'; "
    f"letter-spacing: 1.4px; background: transparent; border: none;"
)


# ── Caption button helper ─────────────────────────────────────────────────────
def _caption_btn(symbol: str, close: bool = False) -> QtWidgets.QPushButton:
    btn = QtWidgets.QPushButton(symbol)
    btn.setFixedSize(46, 36)
    btn.setFlat(True)
    btn.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    btn.setStyleSheet(_CAPTION_CLOSE_SS if close else _CAPTION_IDLE_SS)
    return btn


# ── Main UI class ─────────────────────────────────────────────────────────────
class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("ChemicalUsedView")
        MainWindow.setMinimumSize(780, 560)
        MainWindow.resize(860, 620)

        # ── Frameless window ──────────────────────────────────────────────────
        MainWindow.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground, False)
        MainWindow.setStyleSheet(f"QMainWindow {{ background: {_BG}; }}")

        cw = QtWidgets.QWidget(MainWindow)
        cw.setStyleSheet(f"background: {_BG};")
        MainWindow.setCentralWidget(cw)

        root = QtWidgets.QVBoxLayout(cw)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Title bar ─────────────────────────────────────────────────────────
        self.titleBar = QtWidgets.QFrame()
        self.titleBar.setObjectName("titleBar")
        self.titleBar.setFixedHeight(52)
        self.titleBar.setStyleSheet(
            f"QFrame#titleBar {{ background: {_HEADER_BG}; }}")

        tb_h = QtWidgets.QHBoxLayout(self.titleBar)
        tb_h.setContentsMargins(16, 0, 0, 0)
        tb_h.setSpacing(10)

        # Icon pill
        icon_pill = QtWidgets.QLabel("⚗")
        icon_pill.setFixedSize(32, 32)
        icon_pill.setAlignment(QtCore.Qt.AlignCenter)
        icon_pill.setStyleSheet(
            "background: rgba(255,255,255,0.12); border-radius: 8px; "
            "font: 15pt 'Segoe UI'; color: #fff; border: none;")
        tb_h.addWidget(icon_pill)

        # Title + subtitle stack
        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(0)
        title_col.setContentsMargins(0, 0, 0, 0)

        h_title = QtWidgets.QLabel("Chemicals Used")
        h_title.setStyleSheet(
            "color: #fff; font: 700 11pt 'Segoe UI'; "
            "background: transparent; border: none; letter-spacing: 0.3px;")

        h_sub = QtWidgets.QLabel("View and manage chemical usage records")
        h_sub.setStyleSheet(
            "color: rgba(198,246,213,0.55); font: 8pt 'Segoe UI'; "
            "background: transparent; border: none;")

        title_col.addWidget(h_title)
        title_col.addWidget(h_sub)
        tb_h.addLayout(title_col)
        tb_h.addStretch()

        # Window caption buttons
        self._minimizeBtn = _caption_btn("─")
        self._minimizeBtn.setToolTip("Minimize")
        self._maximizeBtn = _caption_btn("□")
        self._maximizeBtn.setToolTip("Maximize / Restore")
        self._closeBtn    = _caption_btn("✕", close=True)
        self._closeBtn.setToolTip("Close")
        self._minimizeBtn.setFixedSize(46, 52)
        self._maximizeBtn.setFixedSize(46, 52)
        self._closeBtn.setFixedSize(46, 52)

        tb_h.addWidget(self._minimizeBtn)
        tb_h.addWidget(self._maximizeBtn)
        tb_h.addWidget(self._closeBtn)

        root.addWidget(self.titleBar)

        # ── Thin accent line under header ─────────────────────────────────────
        accent = QtWidgets.QFrame()
        accent.setFixedHeight(2)
        accent.setStyleSheet(f"background: {_G200}; border: none;")
        root.addWidget(accent)

        # ── Body ──────────────────────────────────────────────────────────────
        body = QtWidgets.QWidget()
        body.setStyleSheet(f"background: {_BG};")
        body_lay = QtWidgets.QVBoxLayout(body)
        body_lay.setContentsMargins(18, 16, 18, 14)
        body_lay.setSpacing(12)

        # Section label
        sec_lbl = QtWidgets.QLabel("CHEMICAL USAGE RECORDS")
        sec_lbl.setStyleSheet(_LABEL_MUTED_SS)
        body_lay.addWidget(sec_lbl)

        # ── Table card ────────────────────────────────────────────────────────
        card = QtWidgets.QFrame()
        card.setStyleSheet(
            f"QFrame {{ background: {_SURFACE}; "
            f"border: 1px solid {_BORDER}; border-radius: 10px; }}")
        card_lay = QtWidgets.QVBoxLayout(card)
        card_lay.setContentsMargins(0, 0, 0, 0)
        card_lay.setSpacing(0)

        self.chemicalUsed = QtWidgets.QTableWidget()
        self.chemicalUsed.setObjectName("chemicalUsed")
        self.chemicalUsed.setStyleSheet(_TABLE_SS)
        self.chemicalUsed.setColumnCount(3)
        self.chemicalUsed.setRowCount(5)
        self.chemicalUsed.setAlternatingRowColors(True)
        self.chemicalUsed.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.chemicalUsed.setEditTriggers(
            QtWidgets.QAbstractItemView.DoubleClicked |
            QtWidgets.QAbstractItemView.EditKeyPressed)
        self.chemicalUsed.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.chemicalUsed.setWordWrap(True)
        self.chemicalUsed.setShowGrid(True)

        for col, (text, mode) in enumerate([
            ("Chemical/s Used", QtWidgets.QHeaderView.Stretch),
            ("Quantity",        QtWidgets.QHeaderView.Fixed),
            ("Remarks",         QtWidgets.QHeaderView.Stretch),
        ]):
            item = QtWidgets.QTableWidgetItem(text)
            item.setFont(QtGui.QFont("Segoe UI", 9, QtGui.QFont.Bold))
            self.chemicalUsed.setHorizontalHeaderItem(col, item)
            self.chemicalUsed.horizontalHeader().setSectionResizeMode(col, mode)

        self.chemicalUsed.setColumnWidth(1, 120)
        self.chemicalUsed.horizontalHeader().setStretchLastSection(True)
        self.chemicalUsed.verticalHeader().setDefaultSectionSize(44)
        self.chemicalUsed.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed)

        for i in range(5):
            vitem = QtWidgets.QTableWidgetItem(str(i + 1))
            vitem.setTextAlignment(QtCore.Qt.AlignCenter)
            self.chemicalUsed.setVerticalHeaderItem(i, vitem)

        card_lay.addWidget(self.chemicalUsed)
        body_lay.addWidget(card, 1)

        # ── Action row ────────────────────────────────────────────────────────
        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(10)

        self.addRowBtn_chem = QtWidgets.QPushButton("＋  Add Row")
        self.addRowBtn_chem.setFixedHeight(38)
        self.addRowBtn_chem.setObjectName("addRowBtn_chem")
        self.addRowBtn_chem.setStyleSheet(_ADD_BTN_SS)
        self.addRowBtn_chem.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.delRowBtn_chem = QtWidgets.QPushButton("－  Remove Last Row")
        self.delRowBtn_chem.setFixedHeight(38)
        self.delRowBtn_chem.setObjectName("delRowBtn_chem")
        self.delRowBtn_chem.setStyleSheet(_DEL_BTN_SS)
        self.delRowBtn_chem.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.undoBtn = QtWidgets.QPushButton("↩  Undo")
        self.undoBtn.setFixedHeight(38)
        self.undoBtn.setObjectName("undoBtn")
        self.undoBtn.setStyleSheet(_UNDO_BTN_SS)
        self.undoBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.undoBtn.setToolTip("Undo last change  (Ctrl+Z)")
        self.undoBtn.setEnabled(False)

        btn_row.addWidget(self.addRowBtn_chem)
        btn_row.addWidget(self.delRowBtn_chem)
        btn_row.addWidget(self.undoBtn)
        btn_row.addStretch()

        self.doneBtn = QtWidgets.QPushButton("  Done")
        self.doneBtn.setFixedHeight(38)
        self.doneBtn.setObjectName("doneBtn")
        self.doneBtn.setStyleSheet(_DONE_BTN_SS)
        self.doneBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn_row.addWidget(self.doneBtn)

        body_lay.addLayout(btn_row)
        root.addWidget(body, 1)

        # ── Drag support ──────────────────────────────────────────────────────
        self._install_drag(MainWindow)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # ── Draggable title bar ───────────────────────────────────────────────────
    def _install_drag(self, window):
        self._drag_pos = None

        def _press(e):
            if e.button() == QtCore.Qt.LeftButton:
                self._drag_pos = e.globalPos() - window.frameGeometry().topLeft()

        def _move(e):
            if e.buttons() == QtCore.Qt.LeftButton and self._drag_pos is not None:
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

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtCore.QCoreApplication.translate(
                "ChemicalUsedView", "Chemicals Used"))


# ── Standalone preview ────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    win = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(win)
    win.show()
    sys.exit(app.exec_())