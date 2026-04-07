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