from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QCoreApplication
from ui.dashboard import Ui_Dashboard, DashboardController

class DashboardWindow(DashboardController):
    def __init__(self, api_service):
        super().__init__()
        self.ui = Ui_Dashboard()
        self.ui.setupUi(self)
        self.api = api_service
        
        self.current_category = "treatment"
        
        self.ui.confirmButton.clicked.connect(self.handle_submit_dashboard)
        self.ui.Inspection_btn.clicked.connect(lambda: self.switch_mode_category_dashboard('Inspection'))
        self.ui.Treatment_btn.clicked.connect(lambda: self.switch_mode_category_dashboard('Treatment'))
        self.ui.Logout_btn.clicked.connect(self.close)
        
        self.load_table_data_dashboard()
        
        self.ui.Logout_btn.clicked.connect(self.handle_logout_dashboard)
        
    def switch_mode_category_dashboard(self, mode):
        is_inspection = (mode == "Inspection")
        self.current_category = "inspection" if is_inspection else "treatment"
        prefix = mode
        
        self.ui.label_3.setText(f"Date of {prefix}")
        self.ui.label_4.setText(f"Time of {prefix}")
        
        header_date = self.ui.tableListahan.horizontalHeader(1)
        header_time = self.ui.tableListahan.horizontalHeader(3)
        
        if header_date:
            header_date.setText(f"Date of {prefix}")
        
        if header_time:
            header_time.setText(f"Time of {prefix}")
            
        self.load_table_data_dashboard()
    
    def handle_submit_dashboard(self):
        try:
            data = {
                "Date": self.ui.dateofTreatment.date().toPyDate().isoformat(),
                "category": self.current_category,
                "client_name": self.ui.nameofClientinput.text(),
                "start_time": self.ui.startofTime.time().toString("HH:mm:ss"),
                "end_time": self.ui.endofTime.time().toString("HH:mm:ss"),
                "chemical_name": self.ui.chemicalUsed.text(),
                "actual_chemical_on_hand": float(self.ui.actualchemicalUsed.text() or 0)
            }
        except ValueError:
            QMessageBox.warning(self, "Validation", f"Client Name cannot be empty")
            return
        
        success, msg = self.api.add_inventory_record(data)
        
        if success:
            QMessageBox.information(self, "Success", f"{self.current_category.capitalize()} recorded!")
            self.clear_inputs_dashboard()
            self.load_table_data_dashboard()
        else:
            QMessageBox.critical(self, "Error", f"Failed to save: {msg}")
    
    def load_table_data_dashboard(self):
        # Clear existing rows
        self.ui.tableListahan.setRowCount(0)
        
        # Fetch records from API
        records = self.api.get_active_inventory()
        
        # Filter for the current view (Treatment or Inspection)
        filtered_records = [r for r in records if r.get('category') == self.current_category]
        
        for row_idx, r in enumerate(filtered_records):
            self.ui.tableListahan.insertRow(row_idx)
            # Adjust column indexes (0-based) based on your UI design
            self.ui.tableListahan.setItem(row_idx, 0, QTableWidgetItem(str(r.get('id'))))
            self.ui.tableListahan.setItem(row_idx, 1, QTableWidgetItem(str(r.get('Date'))))
            self.ui.tableListahan.setItem(row_idx, 2, QTableWidgetItem(r.get('client_name')))
            self.ui.tableListahan.setItem(row_idx, 3, QTableWidgetItem(r.get('start_time')))
            self.ui.tableListahan.setItem(row_idx, 4, QTableWidgetItem(r.get('end_time')))
            self.ui.tableListahan.setItem(row_idx, 5, QTableWidgetItem(r.get('chemical_name')))
            self.ui.tableListahan.setItem(row_idx, 6, QTableWidgetItem(r.get('actual_chemical_on_hand')))
            
    def clear_inputs_dashboard(self):
        self.ui.dateofTreatment.clear()
        self.ui.nameofClientinput.clear()
        self.ui.startofTime.clear()
        self.ui.endofTime.clear()
        self.ui.chemicalUsed.clearSelection()
        self.ui.actualchemicalUsed.clearSelection()
        
    def handle_logout_dashboard(self):
        reply = QMessageBox.question(self, 'Exit', 'Are you sure you want to exit the system?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QCoreApplication.instance().quit()