# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os

base_dir   = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "assets")

# ── Shared theme tokens (mirrors dashboard palette) ───────────────────────────
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

# ── Stylesheets ───────────────────────────────────────────────────────────────
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

_RESTORE_BTN_SS = f"""
QPushButton {{
    background: rgba(198,246,213,0.15);
    color: #fff;
    border: 1.5px solid rgba(198,246,213,0.35);
    border-radius: 8px;
    padding: 7px 18px;
    font: 500 10pt 'Segoe UI';
}}
QPushButton:hover   {{
    background: rgba(198,246,213,0.28);
    border-color: rgba(198,246,213,0.70);
}}
QPushButton:pressed {{
    background: rgba(198,246,213,0.10);
}}
"""

_DELETE_BTN_SS = """
QPushButton {
    background: rgba(220,38,38,0.18);
    color: #fff;
    border: 1.5px solid rgba(255,100,100,0.40);
    border-radius: 8px;
    padding: 7px 18px;
    font: 500 10pt 'Segoe UI';
}
QPushButton:hover   {
    background: rgba(220,38,38,0.35);
    border-color: rgba(255,100,100,0.80);
}
QPushButton:pressed {
    background: rgba(220,38,38,0.55);
}
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
    btn.setFixedSize(46, 52)
    btn.setFlat(True)
    btn.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    btn.setStyleSheet(_CAPTION_CLOSE_SS if close else _CAPTION_IDLE_SS)
    return btn


# ── Main UI class ─────────────────────────────────────────────────────────────
class Ui_RecycleBin(object):

    def setupUi(self, RecycleBin):
        RecycleBin.setObjectName("RecycleBin")
        RecycleBin.setMinimumSize(1100, 700)
        RecycleBin.resize(1200, 780)

        # ── Frameless window ──────────────────────────────────────────────────
        RecycleBin.setWindowFlags(
            QtCore.Qt.FramelessWindowHint | QtCore.Qt.Window)
        RecycleBin.setAttribute(QtCore.Qt.WA_TranslucentBackground, False)
        RecycleBin.setStyleSheet(f"QMainWindow {{ background: {_BG}; }}")

        cw = QtWidgets.QWidget(RecycleBin)
        cw.setStyleSheet(f"background: {_BG};")
        RecycleBin.setCentralWidget(cw)

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
        icon_pill = QtWidgets.QLabel()
        icon_pill.setFixedSize(32, 32)
        icon_pill.setAlignment(QtCore.Qt.AlignCenter)
        icon_pill.setStyleSheet(
            "background: rgba(255,255,255,0.12); border-radius: 8px; border: none;")
        rb_px = QtGui.QPixmap(f"{image_path}/Recycle Bin.png")
        if not rb_px.isNull():
            icon_pill.setPixmap(
                rb_px.scaled(20, 20, QtCore.Qt.KeepAspectRatio,
                             QtCore.Qt.SmoothTransformation))
        else:
            icon_pill.setText("🗑")
            icon_pill.setStyleSheet(
                icon_pill.styleSheet() +
                "font: 14pt 'Segoe UI'; color: #fff;")
        tb_h.addWidget(icon_pill)

        # Title + subtitle stack
        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(0)
        title_col.setContentsMargins(0, 0, 0, 0)

        h_title = QtWidgets.QLabel("Recycle Bin")
        h_title.setStyleSheet(
            "color: #fff; font: 700 11pt 'Segoe UI'; "
            "background: transparent; border: none; letter-spacing: 0.3px;")

        h_sub = QtWidgets.QLabel("Restore or permanently delete trashed records")
        h_sub.setStyleSheet(
            "color: rgba(198,246,213,0.55); font: 8pt 'Segoe UI'; "
            "background: transparent; border: none;")

        title_col.addWidget(h_title)
        title_col.addWidget(h_sub)
        tb_h.addLayout(title_col)
        tb_h.addStretch()

        # ── Action buttons inside title bar ───────────────────────────────────
        # Restore button
        self.Restore_btn = QtWidgets.QPushButton()
        self.Restore_btn.setObjectName("Restore_btn")
        self.Restore_btn.setFixedHeight(34)
        self.Restore_btn.setStyleSheet(_RESTORE_BTN_SS)
        self.Restore_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Restore_btn.setToolTip("Restore selected records")

        rst_lay = QtWidgets.QHBoxLayout(self.Restore_btn)
        rst_lay.setContentsMargins(8, 0, 12, 0)
        rst_lay.setSpacing(6)
        rst_icon = QtWidgets.QLabel()
        rst_icon.setFixedSize(16, 16)
        rst_icon.setStyleSheet("background: transparent; border: none;")
        rst_px = QtGui.QPixmap(f"{image_path}/restore.png")
        if not rst_px.isNull():
            rst_icon.setPixmap(
                rst_px.scaled(16, 16, QtCore.Qt.KeepAspectRatio,
                              QtCore.Qt.SmoothTransformation))
        rst_lbl = QtWidgets.QLabel("Restore")
        rst_lbl.setStyleSheet(
            "color: #fff; font: 500 10pt 'Segoe UI'; "
            "background: transparent; border: none;")
        rst_lay.addWidget(rst_icon)
        rst_lay.addWidget(rst_lbl)

        # Delete permanently button
        self.Delete_permanently_btn = QtWidgets.QPushButton()
        self.Delete_permanently_btn.setObjectName("Delete_permanently_btn")
        self.Delete_permanently_btn.setFixedHeight(34)
        self.Delete_permanently_btn.setStyleSheet(_DELETE_BTN_SS)
        self.Delete_permanently_btn.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Delete_permanently_btn.setToolTip("Permanently delete selected records")

        del_lay = QtWidgets.QHBoxLayout(self.Delete_permanently_btn)
        del_lay.setContentsMargins(8, 0, 12, 0)
        del_lay.setSpacing(6)
        del_icon = QtWidgets.QLabel()
        del_icon.setFixedSize(16, 16)
        del_icon.setStyleSheet("background: transparent; border: none;")
        del_px = QtGui.QPixmap(f"{image_path}/hard-delete.png")
        if not del_px.isNull():
            del_icon.setPixmap(
                del_px.scaled(16, 16, QtCore.Qt.KeepAspectRatio,
                              QtCore.Qt.SmoothTransformation))
        del_lbl = QtWidgets.QLabel("Delete Permanently")
        del_lbl.setStyleSheet(
            "color: #fff; font: 500 10pt 'Segoe UI'; "
            "background: transparent; border: none;")
        del_lay.addWidget(del_icon)
        del_lay.addWidget(del_lbl)

        tb_h.addWidget(self.Restore_btn)
        tb_h.addSpacing(8)
        tb_h.addWidget(self.Delete_permanently_btn)
        tb_h.addSpacing(8)

        # Window caption buttons
        self._minimizeBtn = _caption_btn("─")
        self._minimizeBtn.setToolTip("Minimize")
        self._maximizeBtn = _caption_btn("□")
        self._maximizeBtn.setToolTip("Maximize / Restore")
        self._closeBtn    = _caption_btn("✕", close=True)
        self._closeBtn.setToolTip("Close")

        tb_h.addWidget(self._minimizeBtn)
        tb_h.addWidget(self._maximizeBtn)
        tb_h.addWidget(self._closeBtn)

        root.addWidget(self.titleBar)

        # ── Thin accent line ──────────────────────────────────────────────────
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
        sec_lbl = QtWidgets.QLabel("TRASHED RECORDS")
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

        self.recycle_table = QtWidgets.QTableWidget()
        self.recycle_table.setObjectName("recycle_table")
        self.recycle_table.setStyleSheet(_TABLE_SS)
        self.recycle_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.recycle_table.setSelectionMode(
            QtWidgets.QAbstractItemView.NoSelection)
        self.recycle_table.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.recycle_table.setWordWrap(True)
        self.recycle_table.setAlternatingRowColors(True)
        self.recycle_table.setShowGrid(True)

        self.recycle_table.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)
        self.recycle_table.verticalHeader().setDefaultSectionSize(52)
        self.recycle_table.horizontalHeader().setStretchLastSection(True)
        self.recycle_table.horizontalHeader().setDefaultSectionSize(200)

        self.recycle_table.setColumnCount(9)
        for col, (lbl, w) in enumerate([
            ("",                 0  ),
            ("Category",         110),
            ("Admin",            120),
            ("Date",             100),
            ("Client",           160),
            ("Time",             230),
            ("Chemicals Used",   260),
            ("Actual Chemicals", 260),
            ("Remarks",          220),
        ]):
            item = QtWidgets.QTableWidgetItem(lbl)
            item.setFont(QtGui.QFont("Segoe UI", 9, QtGui.QFont.Bold))
            self.recycle_table.setHorizontalHeaderItem(col, item)
            if w:
                self.recycle_table.setColumnWidth(col, w)

        self.recycle_table.setColumnHidden(0, True)

        card_lay.addWidget(self.recycle_table)
        body_lay.addWidget(card, 1)

        root.addWidget(body, 1)

        # ── Drag + window controls ────────────────────────────────────────────
        self._install_drag(RecycleBin)

        self.retranslateUi(RecycleBin)
        QtCore.QMetaObject.connectSlotsByName(RecycleBin)

    # ── Draggable title bar ───────────────────────────────────────────────────
    def _install_drag(self, window):
        self._drag_pos = None

        def _press(e):
            if e.button() == QtCore.Qt.LeftButton:
                self._drag_pos = (
                    e.globalPos() - window.frameGeometry().topLeft())

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

    def retranslateUi(self, RecycleBin):
        RecycleBin.setWindowTitle(
            QtCore.QCoreApplication.translate("RecycleBin", "Recycle Bin"))


# ── Standalone preview ────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    win = QtWidgets.QMainWindow()
    ui = Ui_RecycleBin()
    ui.setupUi(win)
    win.show()
    sys.exit(app.exec_())