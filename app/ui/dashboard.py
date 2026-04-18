# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import os

base_dir = os.path.dirname(__file__)
image_path = os.path.join(base_dir, "assets")

# ── Shared stylesheet constants ───────────────────────────────────────────────
_COMBO_SS = """
QComboBox {
    background-color: #FFFFFF;
    border-radius: 8px;
    padding: 5px 10px;
    color: #1A3C2A;
    font: 11pt "Segoe UI";
    min-height: 28px;
    border-style: solid;
    border-width: 2px;
    border-top-color: #C6F6D5;
    border-left-color: #C6F6D5;
    border-bottom-color: #2D6A4F;
    border-right-color: #2D6A4F;
}
QComboBox:hover {
    background-color: #D6EBDD;
    border-top-color: #C6E6D3;
    border-left-color: #C6E6D3;
    border-bottom-color: #0E3B21;
    border-right-color: #0E3B21;
    color: #0B2F1B;
}
QComboBox:focus {
    background-color: #EAF7EE;
    border-top-color: #E9F5EC;
    border-left-color: #E9F5EC;
    border-bottom-color: #1B4332;
    border-right-color: #1B4332;
}
QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #C6F6D5;
    border-radius: 6px;
    selection-background-color: #2D6A4F;
    selection-color: #ffffff;
    font: 10pt "Segoe UI";
}
"""

_TABLE_SS = """
QTableWidget {
    background-color: #FFFFFF;
    alternate-background-color: #F5F5F5;
    gridline-color: #D8EDE0;
    border: none;
    font: 11pt "Segoe UI";
    color: #1B4332;
    selection-background-color: #C6F6D5;
    selection-color: #1B4332;
    border-style: solid;
    border-width: 2px;
    border-top-color: #E9F5EC;
    border-left-color: #E9F5EC;
    border-bottom-color: #2D6A4F;
    border-right-color: #2D6A4F;
}
QTableWidget::item { padding: 4px 8px; border: none; background-color: transparent; }
QTableWidget::item:selected { background-color: #C6F6D5; color: #1B4332; }
QHeaderView::section {
    background-color: #2F6B3F;
    color: #ffffff;
    border: none;
    border-right: 1px solid #1B4332;
    padding: 6px 8px;
    font: bold 11pt "Segoe UI";
    text-transform: uppercase;
}
QHeaderView::section:vertical {
    background-color: #F0F0F0;
    color: #1B4332;
    border-right: 1px solid #D1D9CC;
}
QHeaderView { background-color: transparent; border: none; }
QScrollBar:vertical { background: #E8F0EC; width: 11px; border-radius: 5px; }
QScrollBar::handle:vertical { background: #1B4332; border-radius: 5px; min-height: 25px; }
QScrollBar::handle:vertical:hover { background: #0F2A20; }
QScrollBar::handle:vertical:pressed { background: #081A13; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
QScrollBar:horizontal { background: #E8F0EC; height: 11px; border-radius: 5px; }
QScrollBar::handle:horizontal { background: #1B4332; border-radius: 5px; min-width: 25px; }
QScrollBar::handle:horizontal:hover { background: #0F2A20; }
QScrollBar::handle:horizontal:pressed { background: #081A13; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: transparent; }
QTableCornerButton::section { background-color: #2D6A4F; border: none; }
"""

# Left panel width is ~395 px (inputs span x=18 to x=379).
# All section-header labels use x=10, w=375 so they're always fully visible.
_LBL_X  = 10    # consistent left margin for section headers
_LBL_W  = 375   # full left-panel width
_LBL_H  = 24    # consistent height


class Ui_Dashboard(object):
    def setupUi(self, Dashboard):
        Dashboard.setObjectName("Dashboard")
        Dashboard.resize(1455, 982)
        Dashboard.setStyleSheet("QMainWindow { background-color: #EBEBEB; }")

        self.centralwidget = QtWidgets.QWidget(Dashboard)
        self.centralwidget.setObjectName("centralwidget")

        # ── Decorative lines (on centralwidget) ──────────────────────────────
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(864, -10, 241, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.line_8 = QtWidgets.QFrame(self.centralwidget)
        self.line_8.setGeometry(QtCore.QRect(682, -10, 181, 20))
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")

        # ── Scroll area ───────────────────────────────────────────────────────
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(0, 69, 1381, 911))
        self.scrollArea.setStyleSheet(
            "QScrollArea { background-color: #D9E9CF; border: none; "
            "border-right: 1px solid #DCE3DC; border-radius: 15px; } "
            "QWidget { background-color: #D9E9CF; }")
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")

        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1379, 909))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")

        sa = self.scrollAreaWidgetContents_2  # shorthand

        # ── Section header ────────────────────────────────────────────────────
        self.sectionHeader = QtWidgets.QLabel("NEW TREATMENT ENTRY", sa)
        self.sectionHeader.setGeometry(QtCore.QRect(10, 0, 375, 23))
        self.sectionHeader.setStyleSheet(
            "QLabel { color: #1B4332; font: bold 16pt 'Segoe UI'; background: transparent; }")
        self.sectionHeader.setObjectName("sectionHeader")

        # ── Separator ─────────────────────────────────────────────────────────
        self.line_3 = QtWidgets.QFrame(sa)
        self.line_3.setGeometry(QtCore.QRect(-5, -9, 1131, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")

        # ══════════════════════════════════════════════════════════════════════
        #  CLIENT NAME
        # ══════════════════════════════════════════════════════════════════════
        self.label_2 = QtWidgets.QLabel("NAME OF CLIENT - TREATMENT", sa)
        self.label_2.setGeometry(QtCore.QRect(_LBL_X, 40, _LBL_W, _LBL_H))
        self.label_2.setFont(self._font(12))
        self.label_2.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")

        self.nameofClientinput = QtWidgets.QLineEdit(sa)
        self.nameofClientinput.setGeometry(QtCore.QRect(18, 70, 361, 41))
        self.nameofClientinput.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF; border-radius: 10px;
                padding: 8px 16px 8px 36px; font: 11pt "Segoe UI"; color: #374151;
                border-style: solid; border-width: 2px;
                border-top-color: #C6F6D5; border-left-color: #C6F6D5;
                border-bottom-color: #2D6A4F; border-right-color: #2D6A4F;
            }
            QLineEdit:hover {
                background-color: #F0FAF4;
                border-top-color: #D7F2DE; border-left-color: #D7F2DE;
                border-bottom-color: #1B4332; border-right-color: #1B4332;
                color: #2F3A34;
            }
            QLineEdit:focus {
                background-color: #E3F3EA;
                border-top-color: #BFE8CC; border-left-color: #BFE8CC;
                border-bottom-color: #0F3D24; border-right-color: #0F3D24;
                color: #10261C;
            }""")
        self.nameofClientinput.setPlaceholderText("Ex: Eorico")
        self.nameofClientinput.setObjectName("nameofClientinput")

        # ══════════════════════════════════════════════════════════════════════
        #  DATE OF TREATMENT  (label_3)
        # ══════════════════════════════════════════════════════════════════════
        self.label_3 = QtWidgets.QLabel("📅 DATE OF TREATMENT", sa)
        self.label_3.setGeometry(QtCore.QRect(_LBL_X, 110, _LBL_W, _LBL_H))
        self.label_3.setFont(self._font(12))
        self.label_3.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")

        # sub-labels for combos
        self.label_20 = QtWidgets.QLabel("MONTH", sa)
        self.label_20.setGeometry(QtCore.QRect(90, 140, 81, 19))
        self.label_20.setFont(self._font(11))
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")

        self.label_21 = QtWidgets.QLabel("DATE", sa)
        self.label_21.setGeometry(QtCore.QRect(190, 140, 81, 19))
        self.label_21.setFont(self._font(11))
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")

        self.label_22 = QtWidgets.QLabel("YEAR", sa)
        self.label_22.setGeometry(QtCore.QRect(290, 140, 91, 19))
        self.label_22.setFont(self._font(11))
        self.label_22.setAlignment(QtCore.Qt.AlignCenter)
        self.label_22.setObjectName("label_22")

        self.month = self._combo(sa, 95,  160, 81, 42, [str(i) for i in range(1, 13)])
        self.month.setObjectName("month")
        self.date  = self._combo(sa, 197, 160, 71, 42, [str(i) for i in range(1, 32)])
        self.date.setObjectName("date")
        self.year  = self._combo(sa, 290, 160, 91, 42, [str(y) for y in range(2015, 2031)])
        self.year.setObjectName("year")

        # ══════════════════════════════════════════════════════════════════════
        #  TIME OF TREATMENT  (label_4)
        # ══════════════════════════════════════════════════════════════════════
        self.label_4 = QtWidgets.QLabel("🕒 TIME OF TREATMENT", sa)
        self.label_4.setGeometry(QtCore.QRect(_LBL_X, 210, _LBL_W, _LBL_H))
        self.label_4.setFont(self._font(12))
        self.label_4.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")

        self.label_18 = QtWidgets.QLabel("START", sa)
        self.label_18.setGeometry(QtCore.QRect(30, 260, 61, 19))
        self.label_18.setFont(self._font(12))
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")

        self.label_19 = QtWidgets.QLabel("END", sa)
        self.label_19.setGeometry(QtCore.QRect(40, 310, 33, 19))
        self.label_19.setFont(self._font(12))
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName("label_19")

        mins = ["00"] + [str(i) for i in range(1, 60)]
        self.hours    = self._combo(sa, 100, 248, 71, 42, [f"{i:02d}" for i in range(1, 13)])
        self.hours.setObjectName("hours")
        self.time     = self._combo(sa, 200, 248, 71, 42, mins)
        self.time.setObjectName("time")
        self.PM_or_AM = self._combo(sa, 300, 248, 81, 42, ["PM", "AM"])
        self.PM_or_AM.setObjectName("PM_or_AM")

        self.hours_2    = self._combo(sa, 100, 298, 71, 42, [f"{i:02d}" for i in range(1, 13)])
        self.hours_2.setObjectName("hours_2")
        self.time_2     = self._combo(sa, 200, 298, 71, 42, ["00"] + [str(i) for i in range(1, 61)])
        self.time_2.setObjectName("time_2")
        self.PM_or_AM_2 = self._combo(sa, 300, 298, 81, 42, ["PM", "AM"])
        self.PM_or_AM_2.setObjectName("PM_or_AM_2")

        # ══════════════════════════════════════════════════════════════════════
        #  CHEMICALS USED  (label_5)
        # ══════════════════════════════════════════════════════════════════════
        self.label_5 = QtWidgets.QLabel("⚗️ CHEMICALS USED — TREATMENT", sa)
        self.label_5.setGeometry(QtCore.QRect(_LBL_X, 357, _LBL_W, _LBL_H))
        self.label_5.setFont(self._font(12))
        self.label_5.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")

        self.chemicalUsed = self._table(sa, 12, 380, 381, 171,
                                        ["Chemical/s Used", "Quantity", "Remarks"])
        self.chemicalUsed.setObjectName("chemicalUsed")

        self.addChemRow = self._add_row_btn(sa, 20, 560, 361, 36)
        self.addChemRow.setObjectName("addChemRow")

        # ══════════════════════════════════════════════════════════════════════
        #  ACTUAL CHEMICALS ON HAND  (label_6)
        # ══════════════════════════════════════════════════════════════════════
        self.label_6 = QtWidgets.QLabel("⚗️ ACTUAL CHEMICALS ON HAND - TREATMENT", sa)
        self.label_6.setGeometry(QtCore.QRect(_LBL_X, 607, _LBL_W, _LBL_H))
        self.label_6.setFont(self._font(12))
        self.label_6.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")

        self.actualchemicalUsed = self._table(sa, 10, 630, 381, 171,
                                              ["Actual Chemical/s on Hand", "Quantity", "Remarks"])
        self.actualchemicalUsed.setObjectName("actualchemicalUsed")

        self.addActualRow = self._add_row_btn(sa, 26, 810, 351, 36)
        self.addActualRow.setObjectName("addActualRow")

        # ── Save button ───────────────────────────────────────────────────────
        self.confirmButton = QtWidgets.QPushButton("SAVE RECORD", sa)
        self.confirmButton.setGeometry(QtCore.QRect(90, 855, 211, 41))
        self.confirmButton.setStyleSheet("""
            QPushButton {
                background-color: #2F6B3F; color: #ffffff;
                border-style: solid; border-width: 2px;
                border-top-color: #ffffff; border-left-color: #ffffff;
                border-bottom-color: #cccccc; border-right-color: #cccccc;
                border-radius: 15px; padding: 12px 20px;
                font: bold 13pt "Segoe UI"; letter-spacing: 1px;
            }
            QPushButton:hover {
                background-color: #285C36;
                border-top-color: #E6E6E6; border-left-color: #E6E6E6;
                border-bottom-color: #B3B3B3; border-right-color: #B3B3B3;
            }
            QPushButton:pressed {
                background-color: #0D2B1F;
                border-top-color: #1A1A1A; border-left-color: #1A1A1A;
                border-bottom-color: #4A4A4A; border-right-color: #4A4A4A;
                padding-top: 14px; padding-left: 22px;
            }""")
        self.confirmButton.setObjectName("confirmButton")

        # ══════════════════════════════════════════════════════════════════════
        #  RIGHT CONTENT PANEL
        # ══════════════════════════════════════════════════════════════════════
        self.contentPanel = QtWidgets.QWidget(sa)
        self.contentPanel.setGeometry(QtCore.QRect(400, 10, 961, 891))
        self.contentPanel.setStyleSheet(
            "QWidget { background-color: #ECFAE5; border-radius: 15px; }")
        self.contentPanel.setObjectName("contentPanel")

        self.searchDate = QtWidgets.QLineEdit(self.contentPanel)
        self.searchDate.setGeometry(QtCore.QRect(20, 10, 241, 41))
        self.searchDate.setFont(self._font(11, family="Segoe UI"))
        self.searchDate.setStyleSheet("""
            QLineEdit {
                background-color: #FFFFFF; border-radius: 20px;
                padding: 8px 16px 8px 36px; font: 11pt "Segoe UI"; color: #2F3A34;
                border-style: solid; border-width: 2px;
                border-top-color: #C6F6D5; border-left-color: #C6F6D5;
                border-bottom-color: #2D6A4F; border-right-color: #2D6A4F;
            }
            QLineEdit:hover {
                background-color: #E3F2E9;
                border-top-color: #BFE8CC; border-left-color: #BFE8CC;
                border-bottom-color: #1B4332; border-right-color: #1B4332;
                color: #1F2E27;
            }
            QLineEdit:focus {
                background-color: #D6EDE1;
                border-top-color: #A9D8BA; border-left-color: #A9D8BA;
                border-bottom-color: #0E3B21; border-right-color: #0E3B21;
                color: #10261C;
            }""")
        self.searchDate.setPlaceholderText("Search client or date...")
        self.searchDate.setObjectName("searchDate")

        _action_ss = (
            "QPushButton {{ background-color: {bg}; color: #ffffff;"
            " border-style: solid; border-width: 2px;"
            " border-top-color: #ffffff; border-left-color: #ffffff;"
            " border-bottom-color: #cccccc; border-right-color: #cccccc;"
            " padding: 12px 20px; font: bold 8pt \"Segoe UI\";"
            " letter-spacing: 1px; border-radius: 15px; }}"
            "QPushButton:hover {{ background-color: {bg};"
            " border-top-color: #E6E6E6; border-left-color: #E6E6E6;"
            " border-bottom-color: #B3B3B3; border-right-color: #B3B3B3; }}"
            "QPushButton:pressed {{ background-color: {bg};"
            " border-top-color: #1A1A1A; border-left-color: #1A1A1A;"
            " border-bottom-color: #4A4A4A; border-right-color: #4A4A4A;"
            " padding-top: 14px; padding-left: 22px; }}"
        )

        self.confirmButton_2 = QtWidgets.QPushButton("CONVERT TO PDF", self.contentPanel)
        self.confirmButton_2.setGeometry(QtCore.QRect(280, 11, 161, 41))
        self.confirmButton_2.setFont(self._font(8, bold=True, family="Segoe UI"))
        self.confirmButton_2.setStyleSheet(_action_ss.format(bg="#9B0F06"))
        self.confirmButton_2.setObjectName("confirmButton_2")

        self.confirmButton_3 = QtWidgets.QPushButton("💾  TRASH", self.contentPanel)
        self.confirmButton_3.setGeometry(QtCore.QRect(450, 11, 161, 41))
        self.confirmButton_3.setFont(self._font(8, bold=True, family="Segoe UI"))
        self.confirmButton_3.setStyleSheet(_action_ss.format(bg="#DA4848"))
        self.confirmButton_3.setObjectName("confirmButton_3")

        self.tableListahan = QtWidgets.QTableWidget(self.contentPanel)
        self.tableListahan.setGeometry(QtCore.QRect(12, 57, 941, 821))
        self.tableListahan.setFont(self._font(11, family="Segoe UI"))
        self.tableListahan.setStyleSheet(_TABLE_SS.replace(
            "font: bold 11pt", "font: bold 12pt"))
        self.tableListahan.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableListahan.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableListahan.setObjectName("tableListahan")
        self.tableListahan.setColumnCount(8)
        self.tableListahan.setRowCount(1)
        self.tableListahan.setVerticalHeaderItem(0, QtWidgets.QTableWidgetItem("1"))
        for c, txt in enumerate(["Admin User", "Date of Treatment", "Name of Client",
                                  "Time of Treatment", "Chemical/s Used",
                                  "Actual Chemical/s Used", "Remarks", "Edit"]):
            item = QtWidgets.QTableWidgetItem(txt)
            item.setFont(self._font(10))
            self.tableListahan.setHorizontalHeaderItem(c, item)
        self.tableListahan.horizontalHeader().setDefaultSectionSize(300)
        self.tableListahan.horizontalHeader().setMinimumSectionSize(40)
        self.tableListahan.verticalHeader().setDefaultSectionSize(60)

        self.scrollArea.setWidget(sa)

        # ── Header bar ────────────────────────────────────────────────────────
        self.headerBar = QtWidgets.QFrame(self.centralwidget)
        self.headerBar.setGeometry(QtCore.QRect(-10, 0, 1381, 71))
        self.headerBar.setStyleSheet(
            "QFrame { background-color: #2D6A4F; padding: 8px;"
            " border-radius: 10px; margin: 6px; }")
        self.headerBar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.headerBar.setObjectName("headerBar")

        self.label = QtWidgets.QLabel(self.headerBar)
        self.label.setGeometry(QtCore.QRect(0, 0, 81, 71))
        logo_path = os.path.join(base_dir, "assets", "Logo.png")
        self.label.setPixmap(QtGui.QPixmap(logo_path))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.appTitle_2 = QtWidgets.QLabel("👤- RAIONN", self.headerBar)
        self.appTitle_2.setGeometry(QtCore.QRect(70, 10, 201, 51))
        self.appTitle_2.setStyleSheet(
            "QLabel { color: #ffffff; font: bold 15pt 'Segoe UI'; background: transparent; }")
        self.appTitle_2.setObjectName("appTitle_2")

        self.appTitle_3 = QtWidgets.QLabel("ADMIN", self.headerBar)
        self.appTitle_3.setGeometry(QtCore.QRect(1230, 26, 116, 17))
        self.appTitle_3.setFont(self._font(10, bold=True, family="Segoe UI"))
        self.appTitle_3.setStyleSheet(
            "QLabel { color: #ffffff; font: bold 10pt 'Segoe UI'; background: transparent; }")
        self.appTitle_3.setAlignment(QtCore.Qt.AlignCenter)
        self.appTitle_3.setObjectName("appTitle_3")

        Dashboard.setCentralWidget(self.centralwidget)

        # ── Left toolbar ──────────────────────────────────────────────────────
        self.toolBar_files = QtWidgets.QToolBar(Dashboard)
        self.toolBar_files.setFont(self._font(3))
        self.toolBar_files.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.toolBar_files.setStyleSheet("""
            QToolBar {
                background-color: #2D6A4F; border: 1px solid #1F4D2C;
                padding: 8px; spacing: 6px; border-radius: 10px; margin: 6px;
            }
            QToolButton { background-color: transparent; color: white;
                border-radius: 6px; padding: 5px; }
            QToolButton:hover { background-color: rgba(255,255,255,0.15); }
            QToolButton:pressed { background-color: rgba(255,255,255,0.25);
                padding-top: 7px; padding-left: 6px; }
        """)
        self.toolBar_files.setMovable(False)
        self.toolBar_files.setIconSize(QtCore.QSize(48, 48))
        self.toolBar_files.setFloatable(False)
        self.toolBar_files.setObjectName("toolBar_files")
        Dashboard.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar_files)

        def _act(name, icon_file, shortcut=None):
            a = QtWidgets.QAction(Dashboard)
            a.setObjectName(name)
            a.setText(name.replace("_", " ").upper())
            a.setIcon(QtGui.QIcon(os.path.join(base_dir, "assets", icon_file)))
            if shortcut:
                a.setShortcut(shortcut)
            return a

        self.inspection          = _act("inspection",           "Inspection.png")
        self.treatment           = _act("treatment",            "Treatment.png")
        self.recycle_bin         = _act("recycle_bin",          "Recycle Bin.png")
        self.actionPDF_STORAGE_3 = _act("actionPDF_STORAGE_3", "PDF.png", "P")
        self.logout              = _act("logout",               "Logout.png")

        # keep legacy action names so existing controller code still works
        self.actionTREATMENT    = self.treatment
        self.actionINSPECTION   = self.inspection
        self.actionRECYCLE_BIN  = self.recycle_bin
        self.actionLOGOUT       = self.logout
        self.PDF_storage        = self.actionPDF_STORAGE_3

        for a in (self.inspection, self.treatment, self.recycle_bin,
                  self.actionPDF_STORAGE_3, self.logout):
            self.toolBar_files.addAction(a)

        self.toolBar_files.setWindowTitle("toolBar_2")
        Dashboard.setWindowTitle("Dashboard")
        QtCore.QMetaObject.connectSlotsByName(Dashboard)

    # ── Private helpers ───────────────────────────────────────────────────────
    @staticmethod
    def _font(pt, bold=False, family=None):
        f = QtGui.QFont()
        f.setPointSize(pt)
        f.setBold(bold)
        if family:
            f.setFamily(family)
        return f

    def _combo(self, parent, x, y, w, h, items):
        cb = QtWidgets.QComboBox(parent)
        cb.setGeometry(QtCore.QRect(x, y, w, h))
        cb.setFont(self._font(11, family="Segoe UI"))
        cb.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        cb.setStyleSheet(_COMBO_SS)
        cb.setEditable(False)
        for it in items:
            cb.addItem(it)
        return cb

    def _table(self, parent, x, y, w, h, headers, rows=5):
        tbl = QtWidgets.QTableWidget(parent)
        tbl.setGeometry(QtCore.QRect(x, y, w, h))
        tbl.setStyleSheet(_TABLE_SS)
        tbl.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        tbl.setColumnCount(len(headers))
        tbl.setRowCount(rows)
        for r in range(rows):
            tbl.setVerticalHeaderItem(r, QtWidgets.QTableWidgetItem(str(r + 1)))
        for c, txt in enumerate(headers):
            tbl.setHorizontalHeaderItem(c, QtWidgets.QTableWidgetItem(txt))
        for r in range(rows):
            it = QtWidgets.QTableWidgetItem()
            it.setTextAlignment(QtCore.Qt.AlignCenter)
            tbl.setItem(r, 0, it)
        tbl.horizontalHeader().setDefaultSectionSize(250)
        tbl.horizontalHeader().setSortIndicatorShown(False)
        tbl.horizontalHeader().setStretchLastSection(False)
        tbl.verticalHeader().setDefaultSectionSize(40)
        return tbl

    @staticmethod
    def _add_row_btn(parent, x, y, w, h):
        btn = QtWidgets.QPushButton("+ Add Row", parent)
        btn.setGeometry(QtCore.QRect(x, y, w, h))
        btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        btn.setFont(QtGui.QFont("Segoe UI", 11))
        btn.setStyleSheet(
            "QPushButton { background-color: transparent; color: #2D6A4F;"
            " border: 1.5px dashed #2D6A4F; border-radius: 8px; padding: 6px 12px;"
            " font: 11pt \"Segoe UI\"; }"
            "QPushButton:hover { background-color: #e8f5e9; }")
        return btn


# ══════════════════════════════════════════════════════════════════════════════
#  CONTROLLER
# ══════════════════════════════════════════════════════════════════════════════
class DashboardController(QtWidgets.QMainWindow):

    BASE_W = 1455
    BASE_H = 982

    def __init__(self):
        super().__init__()
        self.ui = Ui_Dashboard()
        self.ui.setupUi(self)
        self.setMinimumSize(800, 600)
        self.resize(self.BASE_W, self.BASE_H)

    # ── Geometry helpers ──────────────────────────────────────────────────────
    def _sr(self, x, y, w, h):
        sw = self.width()  / self.BASE_W
        sh = self.height() / self.BASE_H
        return int(x * sw), int(y * sh), int(w * sw), int(h * sh)

    def _sg(self, widget, x, y, w, h):
        widget.setGeometry(QtCore.QRect(*self._sr(x, y, w, h)))

    # ── resizeEvent ───────────────────────────────────────────────────────────
    def resizeEvent(self, event):
        ui = self.ui

        # Scroll area
        self._sg(ui.scrollArea, 0, 69, self.BASE_W - 74, self.BASE_H - 69)
        ui.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(
            0, 0,
            int(1379 * self.width()  / self.BASE_W),
            int( 909 * self.height() / self.BASE_H)))

        # Header bar
        self._sg(ui.headerBar,  -10,  0, 1381, 71)
        self._sg(ui.appTitle_2,  70,  10, 201, 51)
        self._sg(ui.label,        0,   0,  81, 71)
        self._sg(ui.appTitle_3, 1230, 26, 116, 17)

        # Decorative lines
        self._sg(ui.line,   864, -10, 241, 20)
        self._sg(ui.line_8, 682, -10, 181, 20)
        self._sg(ui.line_3,  -5,  -9, 1131, 20)

        # Section header
        self._sg(ui.sectionHeader, _LBL_X, 10, _LBL_W, 23)

        # ── CLIENT NAME ───────────────────────────────────────────────────────
        self._sg(ui.label_2,           _LBL_X, 40, _LBL_W, _LBL_H)
        self._sg(ui.nameofClientinput,     18, 70,    361,     41)

        # ── DATE OF TREATMENT (label_3) ───────────────────────────────────────
        self._sg(ui.label_3,  _LBL_X, 110, _LBL_W, _LBL_H)
        self._sg(ui.label_20,     90,  140,     81,      19)
        self._sg(ui.label_21,    190,  140,     81,      19)
        self._sg(ui.label_22,    290,  140,     91,      19)
        self._sg(ui.month,        95,  160,     81,      42)
        self._sg(ui.date,        197,  160,     71,      42)
        self._sg(ui.year,        290,  160,     91,      42)

        # ── TIME OF TREATMENT (label_4) ───────────────────────────────────────
        self._sg(ui.label_4,  _LBL_X, 210, _LBL_W, _LBL_H)
        self._sg(ui.label_18,     30,  260,     61,      19)
        self._sg(ui.hours,       100,  248,     71,      42)
        self._sg(ui.time,        200,  248,     71,      42)
        self._sg(ui.PM_or_AM,    300,  248,     81,      42)
        self._sg(ui.label_19,     40,  310,     33,      19)
        self._sg(ui.hours_2,     100,  298,     71,      42)
        self._sg(ui.time_2,      200,  298,     71,      42)
        self._sg(ui.PM_or_AM_2,  300,  298,     81,      42)

        # ── CHEMICALS USED (label_5) ──────────────────────────────────────────
        self._sg(ui.label_5,       _LBL_X, 357, _LBL_W,  _LBL_H)
        self._sg(ui.chemicalUsed,      12,  380,    381,     171)
        self._sg(ui.addChemRow,        20,  560,    361,      36)

        # ── ACTUAL CHEMICALS ON HAND (label_6) ───────────────────────────────
        self._sg(ui.label_6,            _LBL_X, 607, _LBL_W,  _LBL_H)
        self._sg(ui.actualchemicalUsed,     10,  630,    381,     171)
        self._sg(ui.addActualRow,           26,  810,    351,      36)

        # ── Save button ───────────────────────────────────────────────────────
        self._sg(ui.confirmButton, 90, 855, 211, 41)

        # ── Content panel ─────────────────────────────────────────────────────
        self._sg(ui.contentPanel, 400, 10, 961, 891)

        # Widgets inside contentPanel (scaled relative to panel's own base size)
        cp_w, cp_h = ui.contentPanel.width(), ui.contentPanel.height()
        bw, bh = 961, 891

        def _cp(widget, x, y, w, h):
            widget.setGeometry(QtCore.QRect(
                int(x * cp_w / bw), int(y * cp_h / bh),
                int(w * cp_w / bw), int(h * cp_h / bh)))

        _cp(ui.searchDate,      20,  10, 241, 41)
        _cp(ui.confirmButton_2, 280, 11, 161, 41)
        _cp(ui.confirmButton_3, 450, 11, 161, 41)
        _cp(ui.tableListahan,   12,  57, 941, 821)

        super().resizeEvent(event)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = DashboardController()
    window.show()
    sys.exit(app.exec_())