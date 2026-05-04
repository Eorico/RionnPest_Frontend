# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

# ── Theme (shared with chem use viewer) ──────────────────────────────────────
_CLR_BG      = "#F0FAF4"
_CLR_PRIMARY = "#2F6B3F"
_CLR_TEXT    = "#1B4332"

_TABLE_SS = """
QTableWidget {
    background-color: #FFFFFF;
    alternate-background-color: #EDF7F1;
    gridline-color: #D6EDE0;
    border: 2px solid #2D6A4F;
    border-radius: 8px;
    font: 11pt 'Segoe UI';
    color: #1B4332;
    selection-background-color: #C6F6D5;
    selection-color: #1B4332;
}
QTableWidget::item {
    padding: 8px 12px;
    border: none;
    color: #1B4332;
}
QTableWidget::item:hover    { background-color: #D6F0E2; }
QTableWidget::item:selected { background-color: #C6F6D5; color: #1B4332; }
QHeaderView::section {
    background-color: #2F6B3F;
    color: #FFFFFF;
    padding: 10px 12px;
    border: none;
    font: bold 10pt 'Segoe UI';
    letter-spacing: 0.4px;
}
QHeaderView::section:vertical {
    background-color: #EDF7F1;
    color: #4A6655;
    border-right: 1px solid #D6EDE0;
    font: 9pt 'Segoe UI';
    padding: 4px;
}
QTableCornerButton::section {
    background-color: #2F6B3F;
    border: none;
}
QScrollBar:vertical {
    background: transparent; width: 12px; margin: 4px 2px;
}
QScrollBar::handle:vertical {
    background: #C6F6D5; border-radius: 6px; min-height: 30px;
}
QScrollBar::handle:vertical:hover   { background: #A8D5BA; }
QScrollBar::handle:vertical:pressed { background: #2F6B3F; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background: transparent; height: 12px; margin: 2px 4px;
}
QScrollBar::handle:horizontal {
    background: #C6F6D5; border-radius: 6px; min-width: 30px;
}
QScrollBar::handle:horizontal:hover   { background: #A8D5BA; }
QScrollBar::handle:horizontal:pressed { background: #2F6B3F; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
"""

_ADD_BTN_SS = """
QPushButton {
    background-color: transparent;
    color: #2F6B3F;
    border: 1.5px dashed #2D6A4F;
    border-radius: 8px;
    padding: 8px 16px;
    font: 11pt 'Segoe UI';
}
QPushButton:hover {
    background-color: #EDF7F1;
    border-color: #1B4332;
    color: #1B4332;
}
QPushButton:pressed { background-color: #C6F6D5; }
"""

_DEL_BTN_SS = """
QPushButton {
    background-color: transparent;
    color: #C0392B;
    border: 1.5px dashed rgba(192, 57, 43, 0.5);
    border-radius: 8px;
    padding: 8px 16px;
    font: 11pt 'Segoe UI';
}
QPushButton:hover {
    background-color: rgba(192, 57, 43, 0.08);
    border-color: #C0392B;
}
QPushButton:pressed { background-color: rgba(192, 57, 43, 0.18); }
"""


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("ActualChemicalView")
        MainWindow.setMinimumSize(860, 620)
        MainWindow.setStyleSheet(f"QMainWindow {{ background-color: {_CLR_BG}; }}")

        # ── Central widget ────────────────────────────────────────────────────
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(f"background-color: {_CLR_BG};")

        root = QtWidgets.QVBoxLayout(self.centralwidget)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ── Header ────────────────────────────────────────────────────────────
        header = QtWidgets.QWidget()
        header.setFixedHeight(68)
        header.setStyleSheet("QWidget { background-color: #2F6B3F; }")

        h_lay = QtWidgets.QHBoxLayout(header)
        h_lay.setContentsMargins(20, 0, 20, 0)
        h_lay.setSpacing(12)

        # icon circle
        icon_circle = QtWidgets.QLabel()
        icon_circle.setFixedSize(40, 40)
        icon_circle.setStyleSheet("""
            QLabel {
                background-color: rgba(255,255,255,0.15);
                border-radius: 20px;
                color: #FFFFFF;
                font: bold 16pt 'Segoe UI';
            }
        """)
        icon_circle.setText("🧪")
        icon_circle.setAlignment(QtCore.Qt.AlignCenter)
        h_lay.addWidget(icon_circle)

        # vertical separator
        vsep = QtWidgets.QFrame()
        vsep.setFrameShape(QtWidgets.QFrame.VLine)
        vsep.setFixedHeight(36)
        vsep.setStyleSheet("color: rgba(255,255,255,0.25);")
        h_lay.addWidget(vsep)

        # title + subtitle
        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(1)

        h_title = QtWidgets.QLabel("Actual Chemicals on Hand")
        h_title.setStyleSheet(
            "font: bold 13pt 'Segoe UI'; color: #FFFFFF; background: transparent;")

        h_sub = QtWidgets.QLabel("View and manage actual chemical stock records")
        h_sub.setStyleSheet(
            "font: 9pt 'Segoe UI'; color: rgba(255,255,255,0.65); background: transparent;")

        title_col.addWidget(h_title)
        title_col.addWidget(h_sub)
        h_lay.addLayout(title_col)
        h_lay.addStretch()

        # row counter badge
       
        root.addWidget(header)

        # ── Body ──────────────────────────────────────────────────────────────
        body = QtWidgets.QWidget()
        body.setStyleSheet(f"background-color: {_CLR_BG};")
        body_lay = QtWidgets.QVBoxLayout(body)
        body_lay.setContentsMargins(16, 16, 16, 12)
        body_lay.setSpacing(10)

        # ── Table ─────────────────────────────────────────────────────────────
        self.actualChemicalOnHand = QtWidgets.QTableWidget()
        self.actualChemicalOnHand.setStyleSheet(_TABLE_SS)
        self.actualChemicalOnHand.setObjectName("actualChemicalOnHand")
        self.actualChemicalOnHand.setColumnCount(3)
        self.actualChemicalOnHand.setRowCount(5)
        self.actualChemicalOnHand.setAlternatingRowColors(True)
        self.actualChemicalOnHand.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection)
        self.actualChemicalOnHand.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.actualChemicalOnHand.setWordWrap(True)
        self.actualChemicalOnHand.setShowGrid(True)

        # headers
        for col, (text, width) in enumerate([
            ("Actual Chemical/s on Hand", 300),
            ("Quantity",                  130),
            ("Remarks",                   0  ),
        ]):
            item = QtWidgets.QTableWidgetItem(text)
            item.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
            self.actualChemicalOnHand.setHorizontalHeaderItem(col, item)
            if width:
                self.actualChemicalOnHand.setColumnWidth(col, width)

        self.actualChemicalOnHand.horizontalHeader().setSectionResizeMode(
            0, QtWidgets.QHeaderView.Stretch)
        self.actualChemicalOnHand.horizontalHeader().setSectionResizeMode(
            1, QtWidgets.QHeaderView.Fixed)
        self.actualChemicalOnHand.horizontalHeader().setSectionResizeMode(
            2, QtWidgets.QHeaderView.Stretch)
        self.actualChemicalOnHand.horizontalHeader().setStretchLastSection(True)

        self.actualChemicalOnHand.verticalHeader().setDefaultSectionSize(48)
        self.actualChemicalOnHand.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed)

        for i in range(5):
            item = QtWidgets.QTableWidgetItem(str(i + 1))
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.actualChemicalOnHand.setVerticalHeaderItem(i, item)

        body_lay.addWidget(self.actualChemicalOnHand)

        # ── Action buttons ────────────────────────────────────────────────────
        btn_row = QtWidgets.QHBoxLayout()
        btn_row.setSpacing(10)

        self.addRowBtn_chem = QtWidgets.QPushButton("＋  Add a Row")
        self.addRowBtn_chem.setFixedHeight(42)
        self.addRowBtn_chem.setStyleSheet(_ADD_BTN_SS)
        self.addRowBtn_chem.setObjectName("addRowBtn_chem")

        self.delRowBtn_chem = QtWidgets.QPushButton("－  Remove Last Row")
        self.delRowBtn_chem.setFixedHeight(42)
        self.delRowBtn_chem.setStyleSheet(_DEL_BTN_SS)
        self.delRowBtn_chem.setObjectName("delRowBtn_chem")

        btn_row.addWidget(self.addRowBtn_chem)
        btn_row.addWidget(self.delRowBtn_chem)
        body_lay.addLayout(btn_row)

        root.addWidget(body)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtCore.QCoreApplication.translate(
                "ActualChemicalView", "Actual Chemicals on Hand"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())