btn_style = """
QPushButton {
    background-color: #ff4d4d;
    color: white;

    border-style: solid;
    border-width: 2px;

    /* Light top/left, dark bottom/right = raised */
    border-top-color: #ffffff;
    border-left-color: #ffffff;
    border-bottom-color: #555555;
    border-right-color: #555555;

    border-radius: 6px;
    padding: 6px;
}

QPushButton:hover {
    background-color: #ff1a1a;
}

QPushButton:pressed {
    /* Reverse colors = pressed inward */
    border-top-color: #555555;
    border-left-color: #555555;
    border-bottom-color: #ffffff;
    border-right-color: #ffffff;

    padding-top: 8px;
    padding-left: 8px;
    padding-bottom: 4px;
    padding-right: 4px;

    background-color: #cc0000;
}
"""

edit_style = """
QDialog { background-color: #F0FAF4; }
QLabel  { font: 11pt 'Segoe UI'; color: #1B4332; }
QLineEdit, QComboBox {
    background: #fff; border-radius: 6px; padding: 4px 8px;
    font: 11pt 'Segoe UI'; color: #1B4332;
    border: 2px solid; border-top-color: #C6F6D5;
    border-left-color: #C6F6D5; border-bottom-color: #2D6A4F;
    border-right-color: #2D6A4F;
}
QTableWidget {
    background: #fff; font: 10pt 'Segoe UI'; color: #1B4332;
    border: 2px solid #2D6A4F; border-radius: 6px;
}
QHeaderView::section {
    background: #2F6B3F; color: #fff;
    font: bold 10pt 'Segoe UI'; padding: 4px;
}
QPushButton {
    background: #2F6B3F; color: #fff; border-radius: 8px;
    padding: 8px 18px; font: bold 11pt 'Segoe UI';
}
QPushButton:hover   { background: #1B4332; }
QPushButton:pressed { background: #081A13; }
"""