# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os

base_dir   = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "assets")

# ── Theme constants ───────────────────────────────────────────────────────────
_CLR_BG         = "#F0FAF4"
_CLR_PRIMARY    = "#2F6B3F"
_CLR_PRIMARY_DK = "#1B4332"
_CLR_ACCENT     = "#C6F6D5"
_CLR_TEXT       = "#1B4332"

_TABLE_SS = """
QTableWidget {
    background-color: #FFFFFF;
    border: 2px solid #2D6A4F;
    border-radius: 8px;
    gridline-color: #D6EDE0;
    font: 11pt 'Segoe UI';
    color: #1B4332;
    alternate-background-color: #EDF7F1;
}
QTableWidget::item {
    padding: 8px 10px;
    border: none;
    color: #1B4332;
}
QTableWidget::item:hover { background-color: #D6F0E2; }
QHeaderView::section {
    background-color: #2F6B3F;
    color: #FFFFFF;
    padding: 10px;
    border: none;
    font: bold 10pt 'Segoe UI';
}
QTableCornerButton::section {
    background-color: #2F6B3F;
    border: none;
}
QScrollBar:vertical {
    background: transparent; width: 14px; margin: 4px 2px;
}
QScrollBar::handle:vertical {
    background: #C6F6D5; border-radius: 7px; min-height: 36px;
}
QScrollBar::handle:vertical:hover   { background: #A8D5BA; }
QScrollBar::handle:vertical:pressed { background: #2F6B3F; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background: transparent; height: 14px; margin: 2px 4px;
}
QScrollBar::handle:horizontal {
    background: #C6F6D5; border-radius: 7px; min-width: 36px;
}
QScrollBar::handle:horizontal:hover   { background: #A8D5BA; }
QScrollBar::handle:horizontal:pressed { background: #2F6B3F; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
"""

_HEADER_SS = """
QWidget {
    background-color: #2F6B3F;
    border-radius: 10px;
}
QLabel {
    color: #FFFFFF;
    background: transparent;
    font: 11pt 'Segoe UI';
}
"""

_BTN_SS = """
QPushButton {
    background-color: rgba(255, 255, 255, 0.15);
    border: 1.5px solid rgba(255, 255, 255, 0.40);
    border-radius: 8px;
    padding: 4px;
}
QPushButton:hover {
    background-color: rgba(255, 255, 255, 0.28);
    border-color: rgba(255, 255, 255, 0.70);
}
QPushButton:pressed {
    background-color: rgba(255, 255, 255, 0.10);
    border-color: rgba(255, 255, 255, 0.90);
}
"""

_BTN_DELETE_SS = """
QPushButton {
    background-color: rgba(220, 53, 53, 0.18);
    border: 1.5px solid rgba(255, 120, 120, 0.50);
    border-radius: 8px;
    padding: 4px;
}
QPushButton:hover {
    background-color: rgba(220, 53, 53, 0.35);
    border-color: rgba(255, 120, 120, 0.85);
}
QPushButton:pressed {
    background-color: rgba(220, 53, 53, 0.55);
    border-color: #FF6666;
}
"""


class Ui_RecycleBin(object):
    def setupUi(self, RecycleBin):
        RecycleBin.setObjectName("RecycleBin")
        RecycleBin.setMinimumSize(1100, 750)
        RecycleBin.setStyleSheet(f"QMainWindow {{ background-color: {_CLR_BG}; }}")

        # ── Central widget ────────────────────────────────────────────────────
        self.centralwidget = QtWidgets.QWidget(RecycleBin)
        self.centralwidget.setStyleSheet(f"background-color: {_CLR_BG};")

        root_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        root_layout.setContentsMargins(14, 14, 14, 14)
        root_layout.setSpacing(10)

        # ── Header bar ────────────────────────────────────────────────────────
        self.widget = QtWidgets.QWidget()
        self.widget.setFixedHeight(84)
        self.widget.setStyleSheet(_HEADER_SS)
        self.widget.setObjectName("widget")

        h_layout = QtWidgets.QHBoxLayout(self.widget)
        h_layout.setContentsMargins(20, 10, 20, 10)
        h_layout.setSpacing(0)

        # logo
        self.label_14 = QtWidgets.QLabel()
        self.label_14.setFixedSize(52, 52)
        self.label_14.setPixmap(
            QtGui.QPixmap(f"{image_path}/Recycle Bin.png").scaled(
                52, 52, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.label_14.setScaledContents(True)
        self.label_14.setStyleSheet("background: transparent;")
        h_layout.addWidget(self.label_14)

        h_layout.addSpacing(12)

        # vertical separator
        vline = QtWidgets.QFrame()
        vline.setFrameShape(QtWidgets.QFrame.VLine)
        vline.setFixedHeight(40)
        vline.setStyleSheet("color: rgba(255,255,255,0.25);")
        h_layout.addWidget(vline)

        h_layout.addSpacing(12)

        # title
        title = QtWidgets.QLabel("Recycle Bin")
        title.setStyleSheet(
            "font: bold 15pt 'Segoe UI'; color: #FFFFFF; "
            "background: transparent; letter-spacing: 1px;")
        h_layout.addWidget(title)

        h_layout.addStretch()

        # ── Restore action group ──────────────────────────────────────────────
        action_group = QtWidgets.QWidget()
        action_group.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 0.10);
                border-radius: 10px;
                border: 1px solid rgba(255, 255, 255, 0.18);
            }
        """)
        ag_layout = QtWidgets.QHBoxLayout(action_group)
        ag_layout.setContentsMargins(14, 8, 14, 8)
        ag_layout.setSpacing(20)

        # Restore icon label (32×32, sits behind button)
        self.label_16 = QtWidgets.QLabel()
        self.label_16.setFixedSize(32, 32)
        self.label_16.setPixmap(
            QtGui.QPixmap(f"{image_path}/restore.png").scaled(
                32, 32, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.label_16.setScaledContents(True)
        self.label_16.setStyleSheet("background: transparent;")

        self.Restore_btn = QtWidgets.QPushButton()
        self.Restore_btn.setFixedSize(44, 44)
        self.Restore_btn.setStyleSheet(_BTN_SS)
        self.Restore_btn.setObjectName("Restore_btn")

        # Restore All icon label (32×32, sits behind button)
        self.label_17 = QtWidgets.QLabel()
        self.label_17.setFixedSize(32, 32)
        self.label_17.setPixmap(
            QtGui.QPixmap(f"{image_path}/restore-all.png").scaled(
                32, 32, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.label_17.setScaledContents(True)
        self.label_17.setStyleSheet("background: transparent;")

        self.Restore_all_btn = QtWidgets.QPushButton()
        self.Restore_all_btn.setFixedSize(44, 44)
        self.Restore_all_btn.setStyleSheet(_BTN_SS)
        self.Restore_all_btn.setObjectName("Restore_all_btn")

        # thin divider between the two restore buttons
        sep = QtWidgets.QFrame()
        sep.setFrameShape(QtWidgets.QFrame.VLine)
        sep.setFixedHeight(30)
        sep.setStyleSheet("color: rgba(255,255,255,0.20);")

        ag_layout.addWidget(self._icon_btn_wrap(self.Restore_btn,     self.label_16, "Restore"))
        ag_layout.addWidget(sep)
        ag_layout.addWidget(self._icon_btn_wrap(self.Restore_all_btn, self.label_17, "Restore All"))
        h_layout.addWidget(action_group)

        h_layout.addSpacing(16)

        # ── Danger group (single, no duplicate) ───────────────────────────────
        danger_group = QtWidgets.QWidget()
        danger_group.setStyleSheet("""
            QWidget {
                background-color: rgba(180, 40, 40, 0.18);
                border-radius: 10px;
                border: 1px solid rgba(255, 100, 100, 0.30);
            }
        """)
        dg_layout = QtWidgets.QHBoxLayout(danger_group)
        dg_layout.setContentsMargins(14, 8, 14, 8)
        dg_layout.setSpacing(0)

        # Delete Permanently icon label (32×32, sits behind button)
        self.label_18 = QtWidgets.QLabel()
        self.label_18.setFixedSize(32, 32)
        self.label_18.setPixmap(
            QtGui.QPixmap(f"{image_path}/hard-delete.png").scaled(
                32, 32, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.label_18.setScaledContents(True)
        self.label_18.setStyleSheet("background: transparent;")

        self.Delete_permanently_btn = QtWidgets.QPushButton()
        self.Delete_permanently_btn.setFixedSize(44, 44)
        self.Delete_permanently_btn.setStyleSheet(_BTN_DELETE_SS)
        self.Delete_permanently_btn.setObjectName("Delete_permanently_btn")

        dg_layout.addWidget(
            self._icon_btn_wrap(self.Delete_permanently_btn, self.label_18, "Delete Permanently"))
        h_layout.addWidget(danger_group)

        root_layout.addWidget(self.widget)

        # ── Divider ───────────────────────────────────────────────────────────
        divider = QtWidgets.QFrame()
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setStyleSheet(f"color: {_CLR_ACCENT};")
        root_layout.addWidget(divider)

        # ── Table ─────────────────────────────────────────────────────────────
        self.recycle_table = QtWidgets.QTableWidget()
        self.recycle_table.setStyleSheet(_TABLE_SS)
        self.recycle_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.recycle_table.setSelectionMode(
            QtWidgets.QAbstractItemView.NoSelection)
        self.recycle_table.setWordWrap(True)
        self.recycle_table.setAlternatingRowColors(True)
        self.recycle_table.setShowGrid(True)
        self.recycle_table.setObjectName("recycle_table")

        self.recycle_table.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents)
        self.recycle_table.verticalHeader().setDefaultSectionSize(60)
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
            item.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
            self.recycle_table.setHorizontalHeaderItem(col, item)
            if w:
                self.recycle_table.setColumnWidth(col, w)

        self.recycle_table.setColumnHidden(0, True)
        root_layout.addWidget(self.recycle_table)

        RecycleBin.setCentralWidget(self.centralwidget)
        self.retranslateUi(RecycleBin)
        QtCore.QMetaObject.connectSlotsByName(RecycleBin)

    def _icon_btn_wrap(self, btn, icon_lbl, caption: str) -> QtWidgets.QWidget:
        """
        Returns a QWidget with:
          - a 44×44 stack where the QPushButton fills the back
            and the 32×32 icon label floats centered on top
          - a caption label underneath
        """
        outer = QtWidgets.QWidget()
        outer.setStyleSheet("background: transparent; border: none;")
        v = QtWidgets.QVBoxLayout(outer)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(5)
        v.setAlignment(QtCore.Qt.AlignCenter)

        # Stack container — button fills it, icon sits on top
        stack = QtWidgets.QWidget()
        stack.setStyleSheet("background: transparent; border: none;")
        stack.setFixedSize(44, 44)

        btn.setParent(stack)
        btn.setGeometry(0, 0, 44, 44)         # button fills the entire 44×44

        icon_lbl.setParent(stack)
        icon_size   = icon_lbl.width()        # 32
        btn_size    = 44
        offset      = (btn_size - icon_size) // 2   # = 6  → centers 32px inside 44px
        icon_lbl.setGeometry(offset, offset, icon_size, icon_size)
        icon_lbl.raise_()                     # float the icon above the button

        cap = QtWidgets.QLabel(caption)
        cap.setAlignment(QtCore.Qt.AlignCenter)
        cap.setStyleSheet(
            "font: 8pt 'Segoe UI';"
            "color: rgba(255, 255, 255, 0.80);"
            "background: transparent;"
            "border: none;"
            "letter-spacing: 0.2px;"
        )

        v.addWidget(stack, 0, QtCore.Qt.AlignCenter)
        v.addWidget(cap,   0, QtCore.Qt.AlignCenter)
        return outer

    def retranslateUi(self, RecycleBin):
        RecycleBin.setWindowTitle(
            QtCore.QCoreApplication.translate("RecycleBin", "Recycle Bin"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    RecycleBin = QtWidgets.QMainWindow()
    ui = Ui_RecycleBin()
    ui.setupUi(RecycleBin)
    RecycleBin.show()
    sys.exit(app.exec_())