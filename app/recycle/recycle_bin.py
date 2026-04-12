from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from ui.recycle_bin import Ui_RecycleBin
from PyQt5.QtGui import QIcon
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(os.path.dirname(CURRENT_DIR), "ui", "assets")

class RecyclBinWindow(QMainWindow):
    def __init__(self, api_service, on_restore_callback=None, parent=None):
        super().__init__(parent)
        self.ui = Ui_RecycleBin()
        self.ui.setupUi(self)
        self.api = api_service
        self.on_restore_callback = on_restore_callback
        
        self.setWindowIcon(QIcon(f"{IMAGE_PATH}/Logo.png"))
        
        self.ui.Restore_btn.clicked.connect(self.handle_restore)
        self.ui.Restore_all_btn.clicked.connect(self.handle_restore_all)
        self.ui.Delete_permanently_btn.clicked.connect(self.handle_permanent_delete_restore)
        self.ui.recycle_table.setColumnCount(7)
        
        self.ui.recycle_table.setColumnWidth(4, 300)
        self.ui.recycle_table.setColumnWidth(5, 400)
        self.ui.recycle_table.setColumnWidth(6, 400)
        
        self.ui.recycle_table.setWordWrap(True)
        self.ui.recycle_table.verticalHeader().setSectionResizeMode(
            self.ui.recycle_table.verticalHeader().ResizeToContents
        )
        
        self.load_bin_data_restore()
        
    def load_bin_data_restore(self):
        records = self.api.get_recycle_bin()
        self.ui.recycle_table.setRowCount(0)
        
        def frm_chemicals(data_list, is_actual=False):
            if not isinstance(data_list, list): return "n/a"
            parts_name = []
            for item in data_list:
                name = item.get('actual_chemicals_name') if is_actual else None
                name = name or item.get('chemical_name') or item.get('chemicals_name') or "Unkown"
                qty = item.get('quantity', '0')
                parts_name.append(f"[C]: {name} - [Q]: {qty}")
            return "\n".join(parts_name)
        
        for row, r in enumerate(records):
            self.ui.recycle_table.insertRow(row)
            
            rec_id = r.get('id')
            category_display = r.get('category', 'Unknown')
            admin_name = r.get('admin_under') or "n/a"
            
            chem_data = r.get('chemical_use') or r.get('chemicals_use') or r.get('chemicals')
            actual_data = r.get('actual_chemical_used') or r.get('actual_chemicals_used') 
            
            chem_output = frm_chemicals(chem_data)
            actual_chem_output = frm_chemicals(actual_data, is_actual=True)
            
            cat_item = QTableWidgetItem(category_display)
            cat_item.setData(Qt.UserRole, rec_id)
            
            self.ui.recycle_table.setItem(row, 0, cat_item)  
            self.ui.recycle_table.setItem(row, 1, QTableWidgetItem(admin_name)) 
            self.ui.recycle_table.setItem(row, 2, QTableWidgetItem(f"{r.get('date')}/{r.get('month')}/{r.get('year')}"))
            self.ui.recycle_table.setItem(row, 3, QTableWidgetItem(r.get('client_name')))
            self.ui.recycle_table.setItem(row, 4, QTableWidgetItem(f"[S]: {r.get('start_time')} - [E]: {r.get('end_time')} | {r.get('meridiem')}"))
            self.ui.recycle_table.setItem(row, 5, QTableWidgetItem(chem_output))
            self.ui.recycle_table.setItem(row, 6, QTableWidgetItem(actual_chem_output))
            
    def get_selected_id_restore(self):
        selected_row = self.ui.recycle_table.currentRow()
        if selected_row > -1:
            return self.ui.recycle_table.item(selected_row, 0).data(Qt.UserRole)
        return None
    
    def handle_restore(self):
        rec_id = self.get_selected_id_restore()
        success, msg = self.api.restore_record(rec_id)
        if rec_id:
            if success:
                QMessageBox.information(self, "Success", "Record restored successfully")
                self.load_bin_data_restore()
                if self.on_restore_callback:
                    self.on_restore_callback()
            else:
                if "429" in str(msg):
                    QMessageBox.critical(self, "Rate Limit Exceeded", 
                        "You are restoring data too fast. Please wait a minute before adding more records.")
                else:
                    QMessageBox.critical(self, "Error", f"Failed to restore: {msg}")
        else:
            QMessageBox.warning(self, "Error", "Please select a record to restore")
            
    def handle_restore_all(self):
        success, msg = self.api.restore_all()
        if success:
            QMessageBox.information(self, "Success", "All records restored")
            self.load_bin_data_restore()
            if self.on_restore_callback:
                self.on_restore_callback()
        else:
            if "429" in str(msg):
                    QMessageBox.critical(self, "Rate Limit Exceeded", 
                        "You are restoring all data too fast. Please wait a minute before adding more records.")
            else:
                QMessageBox.critical(self, "Error", f"Failed to restore all: {msg}")
            
    def handle_permanent_delete_restore(self):
        rec_id = self.get_selected_id_restore()
        if rec_id:
            confirm = QMessageBox.question(self, "Confirm", "Are you sure? This cannot be undone.", 
                                         QMessageBox.Yes | QMessageBox.No)
            
            if confirm == QMessageBox.Yes:
                success, msg = self.api.permanent_delete(rec_id)
                if success:
                    self.load_bin_data_restore()
                    if self.on_restore_callback:
                        self.on_restore_callback()
                    QMessageBox.information(self, "Record", f"Record Permanently removed")
                else:
                    if "429" in str(msg):
                        QMessageBox.critical(self, "Rate Limit Exceeded", 
                            "You are deleting data too fast. Please wait a minute before adding more records.")
                    else:
                        QMessageBox.critical(self, "Error", f"Failed to delete data: {msg}")
            else: 
                QMessageBox.warning(self, "Error", msg)
        
    