from PyQt5.QtWidgets import QMainWindow
from ui.docs_viewer import Ui_DocxViewer

class DocsViewerWindow(QMainWindow):
    def __init__(self, api_service):
        super().__init__()
        self.ui = Ui_DocxViewer
        self.api = api_service
        