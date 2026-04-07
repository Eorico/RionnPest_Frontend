from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox, QPushButton, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ui.dashboard import Ui_Dashboard, DashboardController
from ui.trash_btn import btn_style
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(os.path.dirname(CURRENT_DIR), "ui", "assets")

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
        
        self.ui.tableListahan.setWordWrap(True)
        self.ui.tableListahan.verticalHeader().setSectionResizeMode(
            self.ui.tableListahan.verticalHeader().ResizeToContents
        )
        
        self.ui.tableListahan.setColumnWidth(3, 350)  
        self.ui.tableListahan.setColumnWidth(4, 350)  
        self.ui.tableListahan.setColumnWidth(5, 350) 
        
        self.ui.tableListahan.setColumnCount(7)
        
        self.load_table_data_dashboard()
        self.status_mode_internet_dashboard()
        
    def status_mode_internet_dashboard(self):
        if self.api:
            self.is_online = self.api.check_connection_service()
        
        img = "online.png" if self.is_online else "offline.png"
        pixmap = QPixmap(os.path.join(IMAGE_PATH, img))
        
        if not pixmap.isNull():
          lbl = self.ui.label_16
          w, h = (lbl.width() or 40), (lbl.height() or 40)
          lbl.setPixmap(pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation))
          
        
    def switch_mode_category_dashboard(self, mode):
        self.current_category = mode
        
        self.ui.label_2.setText(f"Client - {mode}")
        self.ui.label_3.setText(f"Date of {mode}")
        self.ui.label_4.setText(f"Time of {mode}")
        self.ui.label_5.setText(f"Chemical/s Used - {mode}")
        self.ui.label_6.setText(f"Actual Chemical/s Used - {mode}")
        self.ui.label_17.setText(f"({mode})")
        
        hrz_headers = [
            (0, "Admin"),
            (1, f"Date of ({mode})"),
            (2, f"Name of Client - ({mode})"),
            (3, f"Time of ({mode})"),
            (4, f"Chemical/s Used - ({mode})"),
            (5, f"Actual Chemical/s Used - ({mode})"),
            (6, f"Trash")
        ]
        
        for col, text in hrz_headers:
            self.ui.tableListahan.setHorizontalHeaderItem(col, QTableWidgetItem(text))
        
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
        
        def fmt_time(hrs, min): return f"{int(hrs):02d}:{int(min):02d}"
        
        try:
            
            print(f"DEBUG: All API attributes: {vars(self.api)}")
            
            cur_admin = getattr(self.api, 'admin_under', None)
            print(f"DEBUG: Admin inventory under: {cur_admin}")
            
            data = {
                "admin_under": cur_admin,
                "date": int(self.ui.date.currentText()),
                "month": int(self.ui.month.currentText()),
                "year": int(self.ui.year.currentText()),
                "category": self.current_category,
                "client_name": self.ui.nameofClientinput.text(),
                "start_time": fmt_time(self.ui.hours.currentText(), self.ui.time.currentText()),
                "end_time": fmt_time(self.ui.hours_2.currentText(), self.ui.time_2.currentText()),
                "meridiem": self.ui.PM_or_AM.currentText(),
                "chemical_use": extract_table_data(self.ui.chemicalUsed, "chemical_name"),
                "actual_chemical_used": extract_table_data(self.ui.actualchemicalUsed, "chemical_name")
            }
            
            if not data["client_name"]:
                return QMessageBox.warning(self, "Validation", "Client name is require.")
            
            if not data["chemical_use"] or not data["actual_chemical_used"]:
                return QMessageBox.warning(self, "Validation", "Chemical data is required.")
            
            success, msg = self.api.add_inventory_record(data)
            if success:
                QMessageBox.information(self, "Success", f"{self.current_category.capitalize()} recorded!")
                self.clear_inputs_dashboard()
                self.load_table_data_dashboard()
                print(f"Success", f"{self.current_category.capitalize()} recorded!")
            else:
                QMessageBox.critical(self, "Error", f"Failed to save: {msg}")
                print(f"Failed to save: {msg}")
            
        except ValueError as e:
            QMessageBox.warning(self, "Validation", f"Date and Time are required.")
            print(f"Error input: {e}")
            return
    
    def load_table_data_dashboard(self):
        
        def frm_chemicals(data_list, is_actual=False):
            if not isinstance(data_list, list): return "n/a"
            parts_name = []
            for item in data_list:
                name = item.get('actual_chemicals_name') if is_actual else None
                name = name or item.get('chemical_name') or item.get('chemicals_name') or "Unkown"
                qty = item.get('quantity', '0')
                parts_name.append(f"[C]: {name} - [Q]: {qty}")
            return "\n".join(parts_name)
                
        self.ui.tableListahan.setRowCount(0)
    
        records = self.api.get_active_inventory()
        
        filtered_records = [r for r in records if r.get('category') == self.current_category]
        
        for row_idx, r in enumerate(filtered_records):
            def set_clm(col, val): 
                if isinstance(val, QPushButton): 
                    container = QWidget()
                    layout = QHBoxLayout(container)
                    layout.addWidget(val)
                    layout.setAlignment(Qt.AlignCenter)
                    layout.setContentsMargins(0, 0, 0, 0)
                    self.ui.tableListahan.setCellWidget(row_idx, col, container)
                else:
                    self.ui.tableListahan.setItem(row_idx, col, QTableWidgetItem(val))
            
            rec_id = r.get('id')
            
            self.ui.tableListahan.insertRow(row_idx)
            
            admin_name = r.get('admin_under') or 'n/a'
            
            d = r.get('date', '')
            m = r.get('month', '')
            y = r.get('year', '')
            full_date = f"{m}/{d}/{y}"
            
            start = r.get('start_time', 'n/a')
            end = r.get('end_time', 'n/a')
            peri = r.get('meridiem', 'n/a')
            combined_time = f"[S]: {start} - [E]: {end} | {peri}"
            
            chem_data = r.get('chemical_use') or r.get('chemicals_use') or r.get('chemicals')
            actual_data = r.get('actual_chemical_used') or r.get('actual_chemicals_used') 
            
            btn_trash = QPushButton("Trash")
            btn_trash.setFixedSize(80, 28)
            btn_trash.setStyleSheet(btn_style)
            
            btn_trash.clicked.connect(lambda _, rid=rec_id: self.handle_trash_dashboard(rid))
            
            set_clm(0, admin_name)
            set_clm(1, full_date)
            set_clm(2, r.get('client_name'))
            set_clm(3, combined_time)
            set_clm(4, frm_chemicals(chem_data))
            set_clm(5, frm_chemicals(actual_data, is_actual=True))
            set_clm(6, btn_trash)
            
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
        
    def handle_trash_dashboard(self, rec_id):
        if rec_id is None:
            return
        
        reply = QMessageBox(
            self, 'Move to Trash',
            'Are you sure you want to move this record to the recycle bin?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, msg = self.api.move_to_bin(rec_id)
            if success:
                QMessageBox.information(self, "Success", "Record move to trash")
                self.load_table_data_dashboard()
            else:
                QMessageBox.critical(self, "Error", f"Failed to move to trash: {msg}")
        
    def handle_logout_dashboard(self):
        reply = QMessageBox.question(self, 'Confirm Logout', 'Are you sure you want to exit the system?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()