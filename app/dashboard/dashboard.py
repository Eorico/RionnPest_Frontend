from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ui.dashboard import Ui_Dashboard, DashboardController
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

# root_dir is app/
root_dir = os.path.dirname(current_dir)

# image_path is app/ui/assets/
image_path = os.path.join(root_dir, "ui", "assets")

class DashboardWindow(DashboardController):
    def __init__(self, api_service):
        super().__init__()
        self.ui = Ui_Dashboard()
        self.ui.setupUi(self)
        self.api = api_service
        
        self.current_category = "treatment"
        
        self.is_online = False
        
        self.ui.confirmButton.clicked.connect(self.handle_submit_dashboard)
        self.ui.Inspection_btn.clicked.connect(lambda: self.switch_mode_category_dashboard('inspection'))
        self.ui.Treatment_btn.clicked.connect(lambda: self.switch_mode_category_dashboard('treatment'))
        
        self.ui.Logout_btn.clicked.connect(self.handle_logout_dashboard)
        
        self.load_table_data_dashboard()
        
        self.status_mode_internet_dashboard()
        
    def status_mode_internet_dashboard(self):
        if self.api:
            self.is_online = self.api.check_connection_service()
        
        image_file = "online.png" if self.is_online else "offline.png"
        full_path = os.path.join(image_path, image_file)

        pixmap = QPixmap(full_path)
        
        if not pixmap.isNull():
            w = self.ui.label_16.width() if self.ui.label_16.width() > 0 else 40
            h = self.ui.label_16.height() if self.ui.label_16.height() > 0 else 40
            
            scaled_pixmap = pixmap.scaled(
                w, h,
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            )
            self.ui.label_16.setPixmap(scaled_pixmap)
        
    def switch_mode_category_dashboard(self, mode):
        is_inspection = (mode == "inspection")
        self.current_category = "inspection" if is_inspection else "treatment"
        prefix = mode
        
        self.ui.label_2.setText(f"Client - {prefix}")
        self.ui.label_3.setText(f"Date of {prefix}")
        self.ui.label_4.setText(f"Time of {prefix}")
        self.ui.label_5.setText(f"Chemical/s Used - {prefix}")
        self.ui.label_6.setText(f"Actual Chemical/s Used - {prefix}")
        self.ui.label_17.setText(f"({prefix})")
        
        self.ui.tableListahan.setHorizontalHeaderItem(1, QTableWidgetItem(f"Date of ({prefix})"))
        self.ui.tableListahan.setHorizontalHeaderItem(2, QTableWidgetItem(f"Name of Client - ({prefix})"))
        self.ui.tableListahan.setHorizontalHeaderItem(3, QTableWidgetItem(f"Time of ({prefix})"))
        self.ui.tableListahan.setHorizontalHeaderItem(4, QTableWidgetItem(f"Chemical/s Used - ({prefix})"))
        self.ui.tableListahan.setHorizontalHeaderItem(5, QTableWidgetItem(f"Actual Chemical/s Used - ({prefix})"))
        
        self.load_table_data_dashboard()
    
    def handle_submit_dashboard(self):
        
        def extract_table_data(table, name_key):
            results = []
            for row in range(table.rowCount()):
                name_item = table.item(row, 0)
                qty_item = table.item(row, 1)
                
                if name_item and name_item.text().strip():
                    results.append({
                        name_key: name_item.text().strip(),
                        "quantity": qty_item.text().strip() if qty_item else "0"
                    })
                    
            return results
        
        try:
            
            date = self.ui.date.currentText()
            month = self.ui.month.currentText()
            year = self.ui.year.currentText()
            
            date_input = int(date)
            month_input = int(month)
            year_input = int(year)
            
            start_h = self.ui.hours.currentText()
            start_m = self.ui.time.currentText()
            end_h = self.ui.hours_2.currentText()
            end_m = self.ui.time_2.currentText()
            
            meridiem = self.ui.PM_or_AM.currentText()
            
            formatted_start = f"{int(start_h):02d}:{int(start_m):02d}:00"
            formatted_end = f"{int(end_h):02d}:{int(end_m):02d}:00"
            
            data = {
                "date": date_input,
                "month": month_input,
                "year": year_input,
                "category": self.current_category,
                "client_name": self.ui.nameofClientinput.text(),
                "start_time": formatted_start,
                "end_time": formatted_end,
                "meridiem": meridiem,
                "chemical_use": extract_table_data(self.ui.chemicalUsed, "chemical_name"),
                "actual_chemical_used": extract_table_data(self.ui.actualchemicalUsed, "chemical_name")
            }
            
            if not data["client_name"].strip():
                QMessageBox.warning(self, "Validation", "Client name is required")
                return
            
            if not data["date"]:
                QMessageBox.warning(self, "Validation", "Client name is required")
                return
            
            if not data["month"]:
                QMessageBox.warning(self, "Validation", "Client name is required")
                return
            
            if not data["year"]:
                QMessageBox.warning(self, "Validation", "Client name is required")
                return
            
            if not data["start_time"]:
                QMessageBox.warning(self, "Validation", "Start time name is required")
                return
            
            if not data["end_time"]:
                QMessageBox.warning(self, "Validation", "End time name is required")
                return
            
            if len(data["chemical_use"]) == 0:
                QMessageBox.warning(self, "Validation", "Chemical use name is required")
                return
            
            if len(data["actual_chemical_used"]) == 0:
                QMessageBox.warning(self, "Validation", "Actual chemical used name is required")
                return
            
            
        except ValueError as e:
            QMessageBox.warning(self, "Validation", f"Error inputs.")
            print(f"Error input: {e}")
            return
        
        success, msg = self.api.add_inventory_record(data)
        
        if success:
            QMessageBox.information(self, "Success", f"{self.current_category.capitalize()} recorded!")
            self.clear_inputs_dashboard()
            self.load_table_data_dashboard()
            print(f"Success", f"{self.current_category.capitalize()} recorded!")
        else:
            QMessageBox.critical(self, "Error", f"Failed to save: {msg}")
            print(f"Failed to save: {msg}")
    
    def load_table_data_dashboard(self):
        # Clear existing rows
        self.ui.tableListahan.setRowCount(0)
        
        # Fetch records from API
        records = self.api.get_active_inventory()
        
        # Filter for the current view (Treatment or Inspection)
        filtered_records = [r for r in records if r.get('category') == self.current_category]
        
        for row_idx, r in enumerate(filtered_records):
            self.ui.tableListahan.insertRow(row_idx)
            # self.ui.tableListahan.setItem(row_idx, 0, QTableWidgetItem(str(r.get('id')))) to bo follow
            self.ui.tableListahan.setItem(row_idx, 1, QTableWidgetItem(str(r.get('Date'))))
            self.ui.tableListahan.setItem(row_idx, 2, QTableWidgetItem(r.get('client_name')))
            
            start = r.get('start_time', 'n/a')
            end = r.get('end_time', 'n/a')
            peri = r.get('meridiem', 'n/a')
            combined_time = f"{start} - {end} {peri}"
            self.ui.tableListahan.setItem(row_idx, 3, QTableWidgetItem(combined_time))
            
            chem_used = r.get('chemical_use', "")
            actual_chem = r.get('actual_chemical_used', "")
            
            if isinstance(chem_used, list) and isinstance(actual_chem, list):
                chem_text = ", ".join([c.get('chemical_name', '') for c in chem_used])
                actual_text = ", ".join([a.get('actual_chemical_used', '') for a in actual_chem])
            else:
                chem_text = str(chem_used)
                actual_text = str(chem_used)
                        
            self.ui.tableListahan.setItem(row_idx, 4, QTableWidgetItem(chem_text))
            self.ui.tableListahan.setItem(row_idx, 5, QTableWidgetItem(actual_text))
            
    def clear_inputs_dashboard(self):
        self.ui.nameofClientinput.clear()
        self.ui.date.setCurrentIndex(0)
        self.ui.month.setCurrentIndex(0)
        self.ui.year.setCurrentIndex(0)
        
        self.ui.hours.setCurrentIndex(0)
        self.ui.time.setCurrentIndex(0)
        self.ui.PM_or_AM.setCurrentIndex(0)
        
        self.ui.hours_2.setCurrentIndex(0)
        self.ui.time_2.setCurrentIndex(0)
        self.ui.PM_or_AM_2.setCurrentIndex(0)
        
        self.ui.chemicalUsed.clearContents()
        self.ui.actualchemicalUsed.clearContents()
        
    def handle_logout_dashboard(self):
        reply = QMessageBox.question(self, 'Confirm Logout', 'Are you sure you want to exit the system?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()