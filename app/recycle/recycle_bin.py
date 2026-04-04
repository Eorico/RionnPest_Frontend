from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from ui.recycle_bin import Ui_RecycleBin

class RecyclBinWindow(QMainWindow):
    def __init__(self, api_service):
        super().__init__()
        self.ui = Ui_RecycleBin()
        self.ui.setupUi(self)
        self.api = api_service
        
        self.ui.Restore_btn.clicked.connect(self.handle_restore)
        self.ui.Restore_all_btn.clicked.connect(self.handle_restore_all)
        self.ui.Delete_permanently_btn.clicked.connect(self.handle_permanent_delete_restore)
        
        self.load_bin_data_restore()
        
    def load_bin_data_restore(self):
        records = self.api.get_recycle_bin()
        self.ui.recycle_table.setRowCount(0)
        
        for row, r in enumerate(records):
            self.ui.recycle_table.insertRow(row)
            
            category_raw = r.get('category', 'Unknown')
            category_display = category_raw.capitalize()
            
            self.ui.recycle_table.setItem(row, 0, QTableWidgetItem(category_display))  
            self.ui.recycle_table.setItem(row, 1, QTableWidgetItem(str(r.get('id')))) 
            self.ui.recycle_table.setItem(row, 2, QTableWidgetItem(r.get('client_name')))
            self.ui.recycle_table.setItem(row, 3, QTableWidgetItem(r.get('treatment_date')))
            self.ui.recycle_table.setItem(row, 4, QTableWidgetItem(r.get('start_time')))
            self.ui.recycle_table.setItem(row, 5, QTableWidgetItem(r.get('chemical_name')))
            self.ui.recycle_table.setItem(row, 6, QTableWidgetItem(str(r.get('actual_chemical_on_hand'))))
            
    def get_selected_id_restore(self):
        selected_row = self.ui.recycle_table.currentRow()
        if selected_row > -1:
            return self.ui.recycle_table.item(selected_row, 1).text()
        return None
    
    def handle_restore(self):
        rec_id = self.get_selected_id_restore()
        if rec_id and self.api.restore_record(rec_id):
            QMessageBox.information(self, "Success", "Record restored successfully")
            self.load_bin_data_restore()
        else:
            QMessageBox.warning(self, "Error", "Please select a record to restore")
            
    def handle_restore_all(self):
        if self.api.restore_all():
            self.load_bin_data_restore()
            
    def handle_permanent_delete_restore(self):
        rec_id = self.get_selected_id_restore()
        if rec_id:
            confirm = QMessageBox.question(self, "Confirm", "Are you sure? This cannot be undone.", 
                                         QMessageBox.Yes | QMessageBox.No)
            
            if confirm == QMessageBox.Yes:
                self.api.permanent_delete(rec_id)
                self.load_bin_data_restore()
        
    