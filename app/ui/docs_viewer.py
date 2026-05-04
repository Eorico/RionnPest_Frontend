# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

# ══════════════════════════════════════════════════════════════════════════════
#  Shared style constants
# ══════════════════════════════════════════════════════════════════════════════
_CLR_PRIMARY     = "#2D6A4F"
_CLR_PRIMARY_DK  = "#1B4332"
_CLR_PRIMARY_XDK = "#0D1F17"
_CLR_ACCENT      = "#C6F6D5"
_CLR_BG          = "#F0FAF4"
_CLR_SIDEBAR_BG  = "#1B4332"
_CLR_PANEL_BG    = "#EAF7EE"
_CLR_WHITE       = "#FFFFFF"
_CLR_TEXT        = "#1B4332"
_CLR_SUBTEXT     = "#6B8F78"
_CLR_BORDER      = "#D4E6DA"

_MENUBAR_SS = """
QMenuBar {
    background-color: #1B4332;
    color: #C6F6D5;
    font: 10pt 'Segoe UI';
    padding: 2px 6px;
    border: none;
    spacing: 2px;
}
QMenuBar::item {
    padding: 5px 14px;
    border-radius: 4px;
    background: transparent;
    color: rgba(198,246,213,0.80);
}
QMenuBar::item:selected {
    background-color: rgba(255,255,255,0.12);
    color: #FFFFFF;
}
QMenuBar::item:pressed {
    background-color: rgba(255,255,255,0.20);
}
QMenu {
    background-color: #FFFFFF;
    color: #1B4332;
    border: 1px solid #D4E6DA;
    border-radius: 8px;
    font: 10pt 'Segoe UI';
    padding: 4px 0;
}
QMenu::item {
    padding: 7px 22px 7px 16px;
    border-radius: 4px;
    margin: 1px 4px;
}
QMenu::item:selected {
    background-color: #2D6A4F;
    color: #FFFFFF;
}
QMenu::separator {
    height: 1px;
    background-color: #E0EEE7;
    margin: 4px 12px;
}
"""

_TOOLBAR_SS = """
QToolBar {
    background-color: #2D6A4F;
    border: none;
    border-bottom: 1px solid #1B4332;
    spacing: 2px;
    padding: 5px 10px;
}
QToolBar::separator {
    background-color: rgba(198,246,213,0.25);
    width: 1px;
    margin: 6px 8px;
}
QToolBar QToolButton {
    background-color: transparent;
    color: rgba(198,246,213,0.85);
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 5px 12px;
    font: 10pt 'Segoe UI';
    min-width: 60px;
}
QToolBar QToolButton:hover {
    background-color: rgba(255,255,255,0.14);
    border-color: rgba(198,246,213,0.30);
    color: #FFFFFF;
}
QToolBar QToolButton:pressed {
    background-color: rgba(255,255,255,0.22);
    border-color: rgba(198,246,213,0.50);
}
"""

_STATUSBAR_SS = """
QStatusBar {
    background-color: #1B4332;
    color: rgba(198,246,213,0.65);
    font: 8pt 'Segoe UI';
    border-top: 1px solid #0D1F17;
    padding: 2px 10px;
}
QStatusBar::item { border: none; }
"""

_SIDEBAR_HEADER_SS = """
QLabel {
    background-color: #0D1F17;
    color: rgba(198,246,213,0.55);
    font: bold 7pt 'Segoe UI';
    letter-spacing: 3px;
    padding: 8px 14px;
    border: none;
}
"""

_LIST_SS = """
QListWidget {
    background-color: transparent;
    color: #C6F6D5;
    border: none;
    font: 10pt 'Segoe UI';
    outline: none;
    padding: 4px 0;
}
QListWidget::item {
    padding: 8px 14px;
    border-radius: 6px;
    margin: 1px 6px;
    color: rgba(198,246,213,0.75);
}
QListWidget::item:hover {
    background-color: rgba(255,255,255,0.08);
    color: #C6F6D5;
}
QListWidget::item:selected {
    background-color: rgba(198,246,213,0.15);
    color: #FFFFFF;
    border-left: 3px solid #74C69D;
    padding-left: 11px;
}
QScrollBar:vertical {
    background: transparent; width: 6px; margin: 4px 2px;
}
QScrollBar::handle:vertical {
    background: rgba(198,246,213,0.25); border-radius: 3px; min-height: 20px;
}
QScrollBar::handle:vertical:hover { background: rgba(198,246,213,0.45); }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
"""

_SPLITTER_SS = """
QSplitter#leftSplitter::handle {
    background-color: rgba(255,255,255,0.08);
    height: 1px;
}
QSplitter#leftSplitter::handle:hover {
    background-color: rgba(198,246,213,0.25);
}
"""

_SCROLL_AREA_SS = """
QScrollArea#pageScrollArea {
    background-color: #E8F5EE;
    border: none;
}
QWidget#scrollAreaContent {
    background-color: #E8F5EE;
}
QScrollBar:vertical {
    background: #D4E6DA; width: 10px; border-radius: 5px; margin: 2px;
}
QScrollBar::handle:vertical {
    background: #74C69D; border-radius: 5px; min-height: 24px;
}
QScrollBar::handle:vertical:hover   { background: #2D6A4F; }
QScrollBar::handle:vertical:pressed { background: #1B4332; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }
QScrollBar:horizontal {
    background: #D4E6DA; height: 10px; border-radius: 5px; margin: 2px;
}
QScrollBar::handle:horizontal {
    background: #74C69D; border-radius: 5px; min-width: 24px;
}
QScrollBar::handle:horizontal:hover   { background: #2D6A4F; }
QScrollBar::handle:horizontal:pressed { background: #1B4332; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: transparent; }
"""

_TABLE_SS = """
QTableWidget#inventoryTable1,
QTableWidget#inventoryTable2 {
    background-color: #FFFFFF;
    alternate-background-color: #F4FBF7;
    gridline-color: #E0EEE7;
    color: #1B4332;
    font: 10pt 'Segoe UI';
    border: none;
    border-radius: 6px;
    selection-background-color: #C6F6D5;
    selection-color: #1B4332;
}
QTableWidget#inventoryTable1::item,
QTableWidget#inventoryTable2::item {
    padding: 6px 10px;
    border: none;
}
QTableWidget#inventoryTable1::item:hover,
QTableWidget#inventoryTable2::item:hover {
    background-color: #E8F5EE;
}
QTableWidget#inventoryTable1 QHeaderView::section,
QTableWidget#inventoryTable2 QHeaderView::section {
    background-color: #2D6A4F;
    color: #FFFFFF;
    font: bold 9pt 'Segoe UI';
    padding: 8px 10px;
    border: none;
    border-right: 1px solid #1B4332;
    border-bottom: 2px solid #52B788;
}
QTableWidget#inventoryTable1 QHeaderView::section:hover,
QTableWidget#inventoryTable2 QHeaderView::section:hover {
    background-color: #1B4332;
}
QTableCornerButton::section {
    background-color: #2D6A4F; border: none;
}
QScrollBar:vertical {
    background: #EAF5EF; width: 8px; border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #74C69D; border-radius: 4px; min-height: 20px;
}
QScrollBar::handle:vertical:hover { background: #2D6A4F; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
"""

_NOTES_SS = """
QTextEdit#notesEdit {
    background-color: #FAFFFE;
    color: #1B4332;
    font: 10pt 'Segoe UI';
    border: 1.5px solid #D4E6DA;
    border-radius: 8px;
    padding: 10px 12px;
    selection-background-color: #C6F6D5;
}
QTextEdit#notesEdit:focus {
    border-color: #2D6A4F;
    background-color: #F8FDF9;
}
"""


# ══════════════════════════════════════════════════════════════════════════════
#  UI class
# ══════════════════════════════════════════════════════════════════════════════
class Ui_DocxViewer(object):

    def setupUi(self, DocxViewer):
        DocxViewer.setObjectName("DocxViewer")
        DocxViewer.setMinimumSize(1416, 988)
        DocxViewer.setStyleSheet(
            f"QMainWindow, QWidget#centralwidget {{ background-color: {_CLR_BG}; }}"
            + _MENUBAR_SS + _TOOLBAR_SS + _STATUSBAR_SS
            + _SPLITTER_SS + _SCROLL_AREA_SS + _TABLE_SS + _NOTES_SS
        )

        # ── Central widget ────────────────────────────────────────────────────
        self.centralwidget = QtWidgets.QWidget(DocxViewer)
        self.centralwidget.setObjectName("centralwidget")

        main_h = QtWidgets.QHBoxLayout(self.centralwidget)
        main_h.setContentsMargins(0, 0, 0, 0)
        main_h.setSpacing(0)
        self.mainHLayout = main_h

        # ══════════════════════════════════════════════════════════════════════
        #  LEFT SIDEBAR
        # ══════════════════════════════════════════════════════════════════════
        sidebar = QtWidgets.QWidget()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(f"background-color: {_CLR_SIDEBAR_BG};")

        sidebar_v = QtWidgets.QVBoxLayout(sidebar)
        sidebar_v.setContentsMargins(0, 0, 0, 0)
        sidebar_v.setSpacing(0)
        self.leftPanelVLayout = sidebar_v

        self.leftSplitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.leftSplitter.setObjectName("leftSplitter")
        self.leftSplitter.setHandleWidth(1)
        self.leftSplitter.setChildrenCollapsible(False)
        self.leftSplitter.setStyleSheet(_SPLITTER_SS)

        # ── Files panel ───────────────────────────────────────────────────────
        self.filesPanel = QtWidgets.QWidget()
        self.filesPanel.setObjectName("filesPanel")
        self.filesPanel.setMinimumHeight(180)
        self.filesPanel.setStyleSheet(f"background-color: {_CLR_SIDEBAR_BG};")

        files_v = QtWidgets.QVBoxLayout(self.filesPanel)
        files_v.setContentsMargins(0, 0, 0, 0)
        files_v.setSpacing(0)
        self.filesPanelVLayout = files_v

        self.filesPanelHeader = QtWidgets.QLabel("  AVAILABLE FILES")
        self.filesPanelHeader.setObjectName("filesPanelHeader")
        self.filesPanelHeader.setFixedHeight(36)
        self.filesPanelHeader.setStyleSheet(_SIDEBAR_HEADER_SS)
        files_v.addWidget(self.filesPanelHeader)

        self.filesList = QtWidgets.QListWidget()
        self.filesList.setObjectName("filesList")
        self.filesList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.filesList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.filesList.setStyleSheet(_LIST_SS)
        self.filesList.addItem(QtWidgets.QListWidgetItem("Sample File List.pdf"))
        files_v.addWidget(self.filesList)

        # ── ToC panel ─────────────────────────────────────────────────────────
        self.tocPanel = QtWidgets.QWidget()
        self.tocPanel.setObjectName("tocPanel")
        self.tocPanel.setMinimumHeight(150)
        self.tocPanel.setStyleSheet(f"background-color: {_CLR_SIDEBAR_BG};")

        toc_v = QtWidgets.QVBoxLayout(self.tocPanel)
        toc_v.setContentsMargins(0, 0, 0, 0)
        toc_v.setSpacing(0)
        self.tocPanelVLayout = toc_v

        self.tocPanelHeader = QtWidgets.QLabel("  TABLE OF CONTENTS")
        self.tocPanelHeader.setObjectName("tocPanelHeader")
        self.tocPanelHeader.setFixedHeight(36)
        self.tocPanelHeader.setStyleSheet(_SIDEBAR_HEADER_SS)
        toc_v.addWidget(self.tocPanelHeader)

        self.tocList = QtWidgets.QListWidget()
        self.tocList.setObjectName("tocList")
        self.tocList.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tocList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tocList.setStyleSheet(_LIST_SS)
        self.tocList.addItem(QtWidgets.QListWidgetItem("1. Sample Panel Content"))
        toc_v.addWidget(self.tocList)

        self.leftSplitter.addWidget(self.filesPanel)
        self.leftSplitter.addWidget(self.tocPanel)
        self.leftSplitter.setSizes([340, 300])
        sidebar_v.addWidget(self.leftSplitter)

        main_h.addWidget(sidebar)

        # Vertical separator
        v_sep = QtWidgets.QFrame()
        v_sep.setFrameShape(QtWidgets.QFrame.VLine)
        v_sep.setFixedWidth(1)
        v_sep.setStyleSheet("background-color: #0D1F17; border: none;")
        main_h.addWidget(v_sep)

        # ══════════════════════════════════════════════════════════════════════
        #  MAIN DOCUMENT AREA
        # ══════════════════════════════════════════════════════════════════════
        self.pageScrollArea = QtWidgets.QScrollArea()
        self.pageScrollArea.setObjectName("pageScrollArea")
        self.pageScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.pageScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.pageScrollArea.setWidgetResizable(True)

        self.scrollAreaContent = QtWidgets.QWidget()
        self.scrollAreaContent.setObjectName("scrollAreaContent")

        self.scrollContentVLayout = QtWidgets.QVBoxLayout(self.scrollAreaContent)
        self.scrollContentVLayout.setContentsMargins(48, 36, 48, 48)
        self.scrollContentVLayout.setSpacing(28)

        # ══════════════════════════════════════════════════════════════════════
        #  PAGE 1
        # ══════════════════════════════════════════════════════════════════════
        self.paperPage1 = self._make_page("paperPage1")
        lay1 = QtWidgets.QVBoxLayout(self.paperPage1)
        lay1.setContentsMargins(56, 48, 56, 48)
        lay1.setSpacing(0)
        self.paperLayout1 = lay1

        # Company header
        hdr_block1 = QtWidgets.QWidget()
        hdr_block1.setStyleSheet("background: transparent;")
        hdr_h1 = QtWidgets.QHBoxLayout(hdr_block1)
        hdr_h1.setContentsMargins(0, 0, 0, 0)
        hdr_h1.setSpacing(14)

        accent_bar = QtWidgets.QFrame()
        accent_bar.setFixedWidth(5)
        accent_bar.setStyleSheet(
            "background-color: #2D6A4F; border-radius: 3px; border: none;")
        hdr_h1.addWidget(accent_bar)

        title_col = QtWidgets.QVBoxLayout()
        title_col.setSpacing(2)

        self.companyName = QtWidgets.QLabel("Raionn Pest Solutions")
        self.companyName.setObjectName("companyName")
        self.companyName.setStyleSheet(
            "color: #1B4332; font: bold 20pt 'Georgia'; background: transparent;")
        title_col.addWidget(self.companyName)

        self.companyTagline = QtWidgets.QLabel(
            "Professional Pest Control and Inventory Management  |  raionnpest@gmail.com")
        self.companyTagline.setObjectName("companyTagline")
        self.companyTagline.setStyleSheet(
            "color: #6B8F78; font: 9pt 'Segoe UI'; background: transparent;")
        title_col.addWidget(self.companyTagline)

        hdr_h1.addLayout(title_col)
        hdr_h1.addStretch()

        chip = QtWidgets.QLabel("  ACTIVE  ")
        chip.setFixedHeight(24)
        chip.setStyleSheet("""
            QLabel {
                background-color: #D1FAE5;
                color: #065F46;
                font: bold 8pt 'Segoe UI';
                border-radius: 12px;
                padding: 0 10px;
                letter-spacing: 2px;
            }
        """)
        hdr_h1.addWidget(chip, 0, QtCore.Qt.AlignVCenter)
        lay1.addWidget(hdr_block1)

        lay1.addSpacing(16)
        self.headerDivider = self._make_hline("headerDivider", "#2D6A4F", 2)
        lay1.addWidget(self.headerDivider)
        lay1.addSpacing(14)

        # Meta row
        meta_row = QtWidgets.QHBoxLayout()
        meta_row.setSpacing(0)

        self.docTitleLabel = QtWidgets.QLabel("Inventory Report — Q1 2025")
        self.docTitleLabel.setObjectName("docTitleLabel")
        self.docTitleLabel.setStyleSheet(
            "color: #1B4332; font: bold 14pt 'Segoe UI'; background: transparent;")
        meta_row.addWidget(self.docTitleLabel)
        meta_row.addStretch()

        self.metaLabel = QtWidgets.QLabel(
            "Generated: January 31, 2025  |  Prepared by: Admin  |  Status: Active")
        self.metaLabel.setObjectName("metaLabel")
        self.metaLabel.setStyleSheet(
            "color: #6B8F78; font: 9pt 'Segoe UI'; background: transparent;")
        self.metaLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        meta_row.addWidget(self.metaLabel)
        lay1.addLayout(meta_row)

        lay1.addSpacing(6)
        self.innerDivider = self._make_hline("innerDivider", "#C6F6D5", 1)
        lay1.addWidget(self.innerDivider)
        lay1.addSpacing(18)

        # Section label (QWidget wrapper — inner QLabel objectName = "sectionLabel")
        self.sectionLabel = self._make_section_lbl(
            self.paperPage1, "sectionLabel", "Inventory Table")
        lay1.addWidget(self.sectionLabel)
        lay1.addSpacing(10)

        # Table 1
        self.inventoryTable1 = self._make_table("inventoryTable1", 10, 6)
        lay1.addWidget(self.inventoryTable1)

        lay1.addStretch()
        lay1.addSpacing(12)

        # Footer 1 (QWidget wrapper — inner QLabel objectName = "pageFooter1")
        self.pageFooter1 = self._make_footer(
            self.paperPage1, "pageFooter1",
            "Raionn Pest Solutions — Confidential", "Page 1 of 2")
        lay1.addWidget(self.pageFooter1)

        self.scrollContentVLayout.addWidget(self.paperPage1)

        # ══════════════════════════════════════════════════════════════════════
        #  PAGE 2
        # ══════════════════════════════════════════════════════════════════════
        self.paperPage2 = self._make_page("paperPage2")
        lay2 = QtWidgets.QVBoxLayout(self.paperPage2)
        lay2.setContentsMargins(56, 48, 56, 48)
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
            "background-color: #2D6A4F; border-radius: 3px; border: none;")
        hdr_h2.addWidget(accent_bar2)

        self.companyName2 = QtWidgets.QLabel("Raionn Pest Solutions")
        self.companyName2.setObjectName("companyName2")
        self.companyName2.setStyleSheet(
            "color: #1B4332; font: bold 14pt 'Georgia'; background: transparent;")
        hdr_h2.addWidget(self.companyName2)
        hdr_h2.addStretch()

        pg2_chip = QtWidgets.QLabel("  Page 2  ")
        pg2_chip.setFixedHeight(22)
        pg2_chip.setStyleSheet("""
            QLabel {
                background-color: #EAF7EE;
                color: #2D6A4F;
                font: bold 8pt 'Segoe UI';
                border-radius: 11px;
                border: 1px solid #C6F6D5;
                padding: 0 8px;
            }
        """)
        hdr_h2.addWidget(pg2_chip, 0, QtCore.Qt.AlignVCenter)
        lay2.addWidget(hdr_block2)

        lay2.addSpacing(12)
        self.headerDivider2 = self._make_hline("headerDivider2", "#2D6A4F", 2)
        lay2.addWidget(self.headerDivider2)
        lay2.addSpacing(22)

        # Notes label (QWidget wrapper — inner QLabel objectName = "notesLabel")
        self.notesLabel = self._make_section_lbl(
            self.paperPage2, "notesLabel", "Statement  (click to edit)")
        lay2.addWidget(self.notesLabel)
        lay2.addSpacing(10)

        self.notesEdit = QtWidgets.QTextEdit()
        self.notesEdit.setObjectName("notesEdit")
        self.notesEdit.setMinimumHeight(220)
        self.notesEdit.setAcceptRichText(False)
        self.notesEdit.setPlaceholderText(
            "Click here to type your notes, observations, "
            "or remarks for this report...")
        lay2.addWidget(self.notesEdit)

        lay2.addStretch()
        lay2.addSpacing(12)

        # Footer 2 (QWidget wrapper — inner QLabel objectName = "pageFooter2")
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
        main_h.addWidget(self.pageScrollArea)

        DocxViewer.setCentralWidget(self.centralwidget)

        # ══════════════════════════════════════════════════════════════════════
        #  TOOLBAR
        # ══════════════════════════════════════════════════════════════════════
        self.mainToolBar = QtWidgets.QToolBar(DocxViewer)
        self.mainToolBar.setObjectName("mainToolBar")
        self.mainToolBar.setMovable(False)
        self.mainToolBar.setFloatable(False)
        self.mainToolBar.setIconSize(QtCore.QSize(16, 16))
        DocxViewer.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)

        # ══════════════════════════════════════════════════════════════════════
        #  MENU BAR
        # ══════════════════════════════════════════════════════════════════════
        self.menubar = QtWidgets.QMenuBar(DocxViewer)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1416, 33))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        DocxViewer.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(DocxViewer)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setSizeGripEnabled(True)
        DocxViewer.setStatusBar(self.statusbar)

        # ── Actions ───────────────────────────────────────────────────────────
        self.actionOpen      = QtWidgets.QAction(DocxViewer)
        self.actionOpen.setObjectName("actionOpen")
        self.actionRefresh   = QtWidgets.QAction(DocxViewer)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionExport    = QtWidgets.QAction(DocxViewer)
        self.actionExport.setObjectName("actionExport")
        self.actionPrint     = QtWidgets.QAction(DocxViewer)
        self.actionPrint.setObjectName("actionPrint")
        self.actionZoomIn    = QtWidgets.QAction(DocxViewer)
        self.actionZoomIn.setObjectName("actionZoomIn")
        self.actionZoomOut   = QtWidgets.QAction(DocxViewer)
        self.actionZoomOut.setObjectName("actionZoomOut")
        self.actionZoomReset = QtWidgets.QAction(DocxViewer)
        self.actionZoomReset.setObjectName("actionZoomReset")
        self.actionFind      = QtWidgets.QAction(DocxViewer)
        self.actionFind.setObjectName("actionFind")
        self.actionClose     = QtWidgets.QAction(DocxViewer)
        self.actionClose.setObjectName("actionClose")
        self.actionAbout     = QtWidgets.QAction(DocxViewer)
        self.actionAbout.setObjectName("actionAbout")

        self.mainToolBar.addAction(self.actionOpen)
        self.mainToolBar.addAction(self.actionRefresh)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actionExport)
        self.mainToolBar.addAction(self.actionPrint)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actionZoomIn)
        self.mainToolBar.addAction(self.actionZoomOut)
        self.mainToolBar.addAction(self.actionZoomReset)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.actionFind)

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

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(DocxViewer)
        QtCore.QMetaObject.connectSlotsByName(DocxViewer)

    # ══════════════════════════════════════════════════════════════════════════
    #  Helpers
    # ══════════════════════════════════════════════════════════════════════════
    def _make_page(self, obj_name: str) -> QtWidgets.QFrame:
        page = QtWidgets.QFrame()
        page.setObjectName(obj_name)
        page.setFrameShape(QtWidgets.QFrame.NoFrame)
        page.setStyleSheet(f"""
            QFrame#{obj_name} {{
                background-color: #FFFFFF;
                border-radius: 4px;
                border: 1px solid #D4E6DA;
            }}
        """)
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(28)
        shadow.setOffset(0, 4)
        shadow.setColor(QtGui.QColor(0, 0, 0, 40))
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
            f"background-color: {color}; border: none; max-height: {height}px;")
        return f

    def _make_section_lbl(self, parent, obj_name: str,
                          text: str) -> QtWidgets.QWidget:
        """Returns QWidget wrapper. The inner QLabel carries the objectName."""
        row = QtWidgets.QWidget(parent)
        row.setStyleSheet("background: transparent; border: none;")
        h = QtWidgets.QHBoxLayout(row)
        h.setContentsMargins(0, 0, 0, 0)
        h.setSpacing(8)

        pip = QtWidgets.QFrame()
        pip.setFixedSize(4, 18)
        pip.setStyleSheet(
            "background-color: #52B788; border-radius: 2px; border: none;")
        h.addWidget(pip, 0, QtCore.Qt.AlignVCenter)

        lbl = QtWidgets.QLabel(text)
        lbl.setObjectName(obj_name)   # ← objectName on the inner QLabel
        lbl.setStyleSheet(
            "color: #1B4332; font: bold 11pt 'Segoe UI'; "
            "background: transparent; border: none;")
        h.addWidget(lbl)
        h.addStretch()
        return row

    def _make_footer(self, parent, obj_name: str,
                     left_text: str, right_text: str) -> QtWidgets.QWidget:
        """Returns QWidget wrapper. The left inner QLabel carries the objectName."""
        row = QtWidgets.QWidget(parent)
        row.setStyleSheet("background: transparent; border: none;")

        v = QtWidgets.QVBoxLayout(row)
        v.setContentsMargins(0, 8, 0, 0)
        v.setSpacing(6)

        div = QtWidgets.QFrame()
        div.setFrameShape(QtWidgets.QFrame.HLine)
        div.setFixedHeight(1)
        div.setStyleSheet("background-color: #C6F6D5; border: none;")
        v.addWidget(div)

        inner = QtWidgets.QHBoxLayout()
        inner.setContentsMargins(0, 0, 0, 0)

        left_lbl = QtWidgets.QLabel(left_text)
        left_lbl.setObjectName(obj_name)   # ← objectName on the inner QLabel
        left_lbl.setStyleSheet(
            "color: #A0C4AE; font: 8pt 'Segoe UI'; "
            "background: transparent; border: none;")
        inner.addWidget(left_lbl)
        inner.addStretch()

        right_lbl = QtWidgets.QLabel(right_text)
        right_lbl.setStyleSheet(
            "color: #A0C4AE; font: 8pt 'Segoe UI'; "
            "background: transparent; border: none;")
        inner.addWidget(right_lbl)
        v.addLayout(inner)

        return row

    def _make_table(self, obj_name: str, rows: int,
                    cols: int) -> QtWidgets.QTableWidget:
        tbl = QtWidgets.QTableWidget(rows, cols)
        tbl.setObjectName(obj_name)
        tbl.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        tbl.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        tbl.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)
        tbl.setEditTriggers(
            QtWidgets.QAbstractItemView.AnyKeyPressed |
            QtWidgets.QAbstractItemView.DoubleClicked |
            QtWidgets.QAbstractItemView.EditKeyPressed)
        tbl.setAlternatingRowColors(True)
        tbl.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        tbl.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        tbl.setShowGrid(True)
        tbl.setGridStyle(QtCore.Qt.SolidLine)

        for col, txt in enumerate([
            "Date of Treatment", "Name of Client", "Time of Treatment",
            "Chemical/s Used", "Actual Chemical/s Used", "Remarks"
        ]):
            tbl.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(txt))

        tbl.horizontalHeader().setDefaultSectionSize(157)
        tbl.horizontalHeader().setStretchLastSection(True)
        tbl.verticalHeader().setDefaultSectionSize(36)
        tbl.verticalHeader().setVisible(False)

        for r in range(rows):
            for c in range(cols):
                tbl.setItem(r, c, QtWidgets.QTableWidgetItem(""))

        return tbl

    # ══════════════════════════════════════════════════════════════════════════
    #  retranslateUi
    #  Rule: only call .setText() on actual QLabel / QAction objects.
    #        For wrapper QWidgets use findChild to reach the inner QLabel.
    # ══════════════════════════════════════════════════════════════════════════
    def retranslateUi(self, DocxViewer):
        _t = QtCore.QCoreApplication.translate

        DocxViewer.setWindowTitle(
            _t("DocxViewer", "Raionn Pest Solutions — Document Viewer"))

        # Sidebar — these ARE QLabel, so .setText() is fine
        self.filesPanelHeader.setText(_t("DocxViewer", "  AVAILABLE FILES"))
        self.filesList.item(0).setText(_t("DocxViewer", "Sample Sir Dong"))
        self.tocPanelHeader.setText(_t("DocxViewer", "  TABLE OF CONTENTS"))
        self.tocList.item(0).setText(
            _t("DocxViewer", "1. Bakit Panot si sir Dong?"))

        # Page 1 — direct QLabel members
        self.companyName.setText(_t("DocxViewer", "Raionn Pest Solutions"))
        self.companyTagline.setText(
            _t("DocxViewer",
               "Professional Pest Control and Inventory Management"
               "  |  raionnpest@gmail.com"))
        self.docTitleLabel.setText(
            _t("DocxViewer", "Inventory Report — Q1 2025"))
        self.metaLabel.setText(
            _t("DocxViewer",
               "Generated: January 31, 2025  |  Prepared by: Admin"
               "  |  Status: Active"))

        # Table 1 headers
        for col, txt in enumerate([
            "Date of Treatment", "Name of Client", "Time of Treatment",
            "Chemical/s Used", "Actual Chemical/s Used", "Remarks"
        ]):
            h_item = self.inventoryTable1.horizontalHeaderItem(col)
            if h_item:
                h_item.setText(_t("DocxViewer", txt))
        self.inventoryTable1.setSortingEnabled(True)

        # pageFooter1 — QWidget wrapper, reach inner QLabel via findChild
        lbl1 = self.pageFooter1.findChild(QtWidgets.QLabel, "pageFooter1")
        if lbl1:
            lbl1.setText(
                _t("DocxViewer",
                   "Raionn Pest Solutions — Confidential"
                   "                    Page 1 of 2"))

        # Page 2 — direct QLabel member
        self.companyName2.setText(_t("DocxViewer", "Raionn Pest Solutions"))

        # notesLabel — QWidget wrapper, reach inner QLabel via findChild
        lbl2 = self.notesLabel.findChild(QtWidgets.QLabel, "notesLabel")
        if lbl2:
            lbl2.setText(_t("DocxViewer", "Statement  (click to edit)"))

        # notesEdit is a real QTextEdit
        self.notesEdit.setPlaceholderText(
            _t("DocxViewer",
               "Click here to type your notes, observations, "
               "or remarks for this report..."))

        # pageFooter2 — QWidget wrapper, reach inner QLabel via findChild
        lbl3 = self.pageFooter2.findChild(QtWidgets.QLabel, "pageFooter2")
        if lbl3:
            lbl3.setText(
                _t("DocxViewer",
                   "Raionn Pest Solutions © 2025 — Confidential"
                   "             Page 2 of 2"))

        # Menus
        self.menuFile.setTitle(_t("DocxViewer", "File"))
        self.menuView.setTitle(_t("DocxViewer", "View"))
        self.menuEdit.setTitle(_t("DocxViewer", "Edit"))
        self.menuHelp.setTitle(_t("DocxViewer", "Help"))

        # Actions
        self.actionOpen.setText(_t("DocxViewer", "Open"))
        self.actionOpen.setToolTip(
            _t("DocxViewer", "Open a document  (Ctrl+O)"))
        self.actionOpen.setShortcut(_t("DocxViewer", "Ctrl+O"))

        self.actionRefresh.setText(_t("DocxViewer", "Refresh"))
        self.actionRefresh.setToolTip(
            _t("DocxViewer", "Refresh file list  (F5)"))
        self.actionRefresh.setShortcut(_t("DocxViewer", "F5"))

        self.actionExport.setText(_t("DocxViewer", "Export"))
        self.actionExport.setToolTip(
            _t("DocxViewer", "Export document  (Ctrl+E)"))
        self.actionExport.setShortcut(_t("DocxViewer", "Ctrl+E"))

        self.actionPrint.setText(_t("DocxViewer", "Print"))
        self.actionPrint.setToolTip(
            _t("DocxViewer", "Print document  (Ctrl+P)"))
        self.actionPrint.setShortcut(_t("DocxViewer", "Ctrl+P"))

        self.actionZoomIn.setText(_t("DocxViewer", "Zoom In"))
        self.actionZoomIn.setToolTip(_t("DocxViewer", "Zoom in  (Ctrl++)"))
        self.actionZoomIn.setShortcut(_t("DocxViewer", "Ctrl+="))

        self.actionZoomOut.setText(_t("DocxViewer", "Zoom Out"))
        self.actionZoomOut.setToolTip(_t("DocxViewer", "Zoom out  (Ctrl+-)"))
        self.actionZoomOut.setShortcut(_t("DocxViewer", "Ctrl+-"))

        self.actionZoomReset.setText(_t("DocxViewer", "Reset Zoom"))
        self.actionZoomReset.setShortcut(_t("DocxViewer", "Ctrl+0"))

        self.actionFind.setText(_t("DocxViewer", "Find"))
        self.actionFind.setToolTip(
            _t("DocxViewer", "Find in document  (Ctrl+F)"))
        self.actionFind.setShortcut(_t("DocxViewer", "Ctrl+F"))

        self.actionClose.setText(_t("DocxViewer", "Close"))
        self.actionClose.setShortcut(_t("DocxViewer", "Ctrl+W"))

        self.actionAbout.setText(_t("DocxViewer", "About"))
        self.mainToolBar.setWindowTitle(_t("DocxViewer", "Main Toolbar"))


# ══════════════════════════════════════════════════════════════════════════════
#  Entry point
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    DocxViewer = QtWidgets.QMainWindow()
    ui = Ui_DocxViewer()
    ui.setupUi(DocxViewer)
    DocxViewer.show()
    sys.exit(app.exec_())