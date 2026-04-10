from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import QTimer, pyqtSignal
from ui.intro import Ui_Intro

class IntroWindow(QMainWindow):
    finished = pyqtSignal()
    
    def __init__(self, sync_manager, api_service):
        super().__init__()
        self.ui = Ui_Intro()
        self.ui.setupUi(self)
        
        self.sync_manager = sync_manager
        self.is_online = False
        self.api = api_service
        
        self.show()
        QApplication.processEvents()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress_intro)
        self.timer.start(30)
        
    def update_progress_intro(self):
        val = self.ui.Progress_Loader.value()
        
        if 20 <= val <= 25 and not hasattr(self, '_checked_conn'):
            self._checked_conn = True 
            self.ui.indicator.setText("Checking Connection...")
            QApplication.processEvents()
            
            if self.api:
                self.is_online = self.api.check_connection_service()
                print(f"Connection: {self.is_online}")
            
            if self.is_online:
                self.ui.indicator.setText("Status: Online")
                self.ui.indicator.setStyleSheet("color: #27AE60; font-weight: bold;")
                self.ui.Progress_Loader.setStyleSheet("""
                     QProgressBar {
                         border: 2px solid #aaaaa;
                         border-radius: 5px;
                         text-align: center;
                         color: #79AE6F;
                     }                                                                     
                """)
            else:
                self.ui.indicator.setText("Status: Offline Mode")
                self.ui.indicator.setStyleSheet("color: #E67E22;")
                self.ui.Progress_Loader.setStyleSheet("""
                     QProgressBar {
                         border: 2px solid #aaaaa;
                         border-radius: 5px;
                         text-align: center;
                         color: #79AE6F;
                     }                                   
                """)
            
            QApplication.processEvents()
                
        elif val == 60:
            if self.is_online:
                self.ui.indicator.setText("Syncing Records...")
                QApplication.processEvents()
                self.sync_manager.sync_data()
            else:
                self.ui.indicator.setText("Offline: Skiping Cloud Sync")
                
        elif val == 90:
            self.ui.indicator.setText("Finalizing System...")
        
        if val < 100:
            self.ui.Progress_Loader.setValue(val + 1)
        else: 
            self.timer.stop()
            self.timer.singleShot(500, self.finished.emit)
            