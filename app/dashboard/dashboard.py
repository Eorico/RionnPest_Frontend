from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox,  QMainWindow, QAbstractItemView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from ui.dashboard import Ui_Dashboard
from .dashboard_renderer import DashboardTableRenderer
from util.dashboard_util import DashboardFormatter
from util.operation_util import Operation
from util.docs_generator import generate_docx
from docs_viewer.docs_viewer import DocxViewer
from datetime import datetime
from PyQt5.QtCore import pyqtSignal 
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(os.path.dirname(CURRENT_DIR), "ui", "assets")
DEFAULT_ROW_COUNT = 5

class DashboardWindow(Operation, QMainWindow):
    logged_out = pyqtSignal()
    record_saved = pyqtSignal()
    def __init__(self, api_service):
        super().__init__()
        self.ui = Ui_Dashboard()
        self.ui.setupUi(self)
        self.ui._install_drag(self)
        self.api = api_service
        self.current_category = "treatment"
        self.is_online = False
        self._docx_viewer = None
        
        self.setWindowIcon(QIcon(f"{IMAGE_PATH}/Logo.png"))
        
        self._setup_table()
        self._setup_renderer()
        self.bind_event_dashboard()
        self.load_table_data_dashboard()
        
        self.ui.confirmButton_3.clicked.connect(self.handle_trash_selected)
        self.ui.confirmButton_2.clicked.connect(self.handle_docx_selected)
        
        for col in range(3):
            self.ui.chemicalUsed.setColumnWidth(col, 150)
            
        for col in range(3):
            self.ui.actualchemicalUsed.setColumnWidth(col, 180)

    def _setup_table(self):
        table = self.ui.tableListahan

        table.setSelectionMode(QAbstractItemView.NoSelection)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setMouseTracking(True)
        table.viewport().setMouseTracking(True)
        table.setWordWrap(True)
         
        table.verticalHeader().setSectionResizeMode(
            table.verticalHeader().ResizeToContents
        )
       
        table.setColumnCount(9)
        table.horizontalHeader().setSectionResizeMode(0, table.horizontalHeader().Interactive)
        table.setColumnWidth(0, 50)
        table.setColumnWidth(2, 350)
        table.setColumnWidth(3, 350)
        table.setColumnWidth(4, 350)  
        table.setColumnWidth(5, 350) 
        table.setColumnWidth(6, 350)   
        table.setColumnWidth(7, 250)   
        table.setColumnWidth(8, 150)  

        fixed_ss = table.styleSheet().replace("background-color: transparent;", "")
        table.setStyleSheet(fixed_ss)
        
        table.setColumnHidden(0, True)
        self._set_headers()
        
    def _set_headers(self):
        for col, text in enumerate([
            "", "Admin User", 
            "Date of | (Treatment)" , "Name of Client | (Treatment)",
            "Time of | (Treatment)", "Chemical/s Used | (Treatment)",
            "Actual Chemical/s Used | (Treatment)", "Remarks", "Edit"
        ]):
            self.ui.tableListahan.setHorizontalHeaderItem(
                col, QTableWidgetItem(text)
            )
            
    def _setup_renderer(self):
        self.table_renderer = DashboardTableRenderer(
            self.ui.tableListahan,
            on_trash_callback=self.handle_trash_dashboard,
            on_edit_callback=self.handle_edit_dashboard,
            current_admin=(getattr(self.api, 'admin_under', None) or '').strip().lower()  # ← fix
        )
        
    def _get_checked_ids(self) -> list:
        return [r.get("id") for r in self.table_renderer.get_checked_records()]
    
    def _clear_checks(self):
        self.table_renderer.clear_all_checks()
        
    def _reload(self):
        self.load_table_data_dashboard()
            
    def bind_event_dashboard(self):
        self.ui.confirmButton.clicked.connect(self.handle_submit_dashboard)
        self.ui.inspection.clicked.connect(lambda: self.switch_mode_category_dashboard('inspection'))
        self.ui.treatment.clicked.connect(lambda: self.switch_mode_category_dashboard('treatment'))
        self.ui.logout.clicked.connect(self.handle_logout_dashboard)
        self.ui.searchDate.textChanged.connect(self.handle_search_input_dashboard)
        self.ui.actionPDF_STORAGE.triggered.connect(self.open_docx_viewer)

    def switch_mode_category_dashboard(self, mode):
        self.current_category = mode
        
        mode_capital = mode.upper()

        self.ui.HeaderTreatment.setText(f"NEW {mode_capital} ENTRY")
        self.ui.nameLabel.setText(f"CLIENT - {mode_capital}")
        self.ui.dateLabel.setText(f"DATE OF {mode_capital}")
        self.ui.timeLabel.setText(f"TIME OF {mode_capital}")
        self.ui.chemLabel.setText(f"CHEMICAL/S USED - {mode_capital}")
        self.ui.actualChemLabel.setText(f"ACTUAL CHEMICAL/S USED - {mode_capital}")

        for col, text in [
            (0, ""),  
            (1, "Admin User"),
            (2, f"Date of | ({mode_capital})"),
            (3, f"Name of Client | ({mode_capital})"),
            (4, f"Time of | ({mode_capital})"),
            (5, f"Chemical/s Used | ({mode_capital})"),
            (6, f"Actual Chemical/s Used | ({mode_capital})"),
            (7, "Remarks"),
            (8, "Edit")
        ]:
            self.ui.tableListahan.setHorizontalHeaderItem(
                col, QTableWidgetItem(text)
            )

        self.load_table_data_dashboard()

    def handle_submit_dashboard(self):

        def extract(table, key):
            results = []
            for row in range(table.rowCount()):
                name_item = table.item(row, 0)
                qty_item = table.item(row, 1)
                remarks_item = table.item(row, 2)

                if name_item and name_item.text().strip():
                    results.append({
                        key: name_item.text().strip(),
                        "quantity": qty_item.text().strip() if qty_item else "0",
                        "remarks": remarks_item.text().strip() if remarks_item else "",
                    })
            return results

        try:
            data = {
                "admin_under": getattr(self.api, 'admin_under', None),
                "date": int(self.ui.date.currentText()),
                "month": int(self.ui.month.currentText()),
                "year": int(self.ui.year.currentText()),
                "category": self.current_category,
                "client_name": self.ui.nameofClientinput.text(),
                "start_time": DashboardFormatter.format_time(
                    self.ui.hours.currentText(),
                    self.ui.time.currentText()
                ),
                "end_time": DashboardFormatter.format_time(
                    self.ui.hours_2.currentText(),
                    self.ui.time_2.currentText()
                ),
                "start_meridiem": self.ui.PM_or_AM.currentText(),
                "end_meridiem":   self.ui.PM_or_AM_2.currentText(),     
                "chemical_use": extract(self.ui.chemicalUsed, "chemical_name"),
                "actual_chemical_used": extract(self.ui.actualchemicalUsed, "chemical_name"),
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
                self.record_saved.emit()
            else:
                if "429" in str(msg):
                    QMessageBox.critical(self, "Rate Limit Exceeded",
                        "You are submitting data too fast. Please wait a minute before adding more records.")
                else:
                    QMessageBox.critical(self, "Error", f"Failed to save: {msg}")

        except ValueError as e:
            QMessageBox.warning(self, "Validation", "Date and Time are required.")
            print(f"Error input: {e}")

    def load_table_data_dashboard(self):       
        self.table_renderer.update_admin(
            (getattr(self.api, 'admin_under', None) or '').strip().lower()
        )
        records = self.api.get_active_inventory()
        filtered = [r for r in records if r.get('category') == self.current_category]
        self.table_renderer.render(filtered)

    def handle_search_input_dashboard(self):
        query = self.ui.searchDate.text().lower().strip()
        all_records = self.api.get_active_inventory()
        category_records = [r for r in all_records if r.get('category') == self.current_category]

        if not query:
            self.ui.tableListahan.clearSpans()
            self.load_table_data_dashboard()
            return

        filtered = []
        for r in category_records:
            full_date = f"{r.get('month')}/{r.get('date')}/{r.get('year')}".lower()
            client = str(r.get('client_name', '')).lower()

            if query in full_date or query in client:
                filtered.append(r)

        if not filtered:
            self.ui.tableListahan.setRowCount(0)
            self.ui.tableListahan.insertRow(0)
            msg = QTableWidgetItem(f"No existing inventory on this date: {query}")
            msg.setTextAlignment(Qt.AlignCenter)
            self.ui.tableListahan.setItem(0, 0, msg)
            self.ui.tableListahan.setSpan(0, 0, 1, 7)
            return

        self.table_renderer.render(filtered)
        
    def handle_trash_dashboard(self, rec_id, record_admin=None):
        if rec_id is None:
            return
        
        if record_admin and record_admin != getattr(self.api, 'admin_under', None):
            QMessageBox.warning(self, "Permission Denied", "You can only move your own records to trash.")
            return

        success, msg = self.api.move_to_bin(rec_id)
        if not success:
            QMessageBox.critical(self, "Error", f"Failed to move  to trash: {msg}")
        else:
            self.load_table_data_dashboard()

    def handle_logout_dashboard(self):
        reply = QMessageBox.question(
            self,
            'Confirm Logout',
            'Are you sure you want to exit the system?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.close()

    def clear_inputs_dashboard(self):
        self.ui.nameofClientinput.clear()

        for combo in [
            self.ui.date, self.ui.month, self.ui.year,
            self.ui.hours, self.ui.time, self.ui.PM_or_AM,
            self.ui.hours_2, self.ui.time_2, self.ui.PM_or_AM_2
        ]:
            combo.setCurrentIndex(0)

        for table in [self.ui.chemicalUsed, self.ui.actualchemicalUsed]:
            table.setRowCount(DEFAULT_ROW_COUNT)
            for row in range(DEFAULT_ROW_COUNT):
                for col in range(table.columnCount()):
                    table.setItem(row, col, QTableWidgetItem(""))
        
    def update_table_inputs_dashboard(self, table_widget, data):
        table_widget.blockSignals(True)
        table_widget.setUpdatesEnabled(False)

        new_count = max(DEFAULT_ROW_COUNT, len(data))
        table_widget.setRowCount(new_count)
        
        for row, entry in enumerate(data):
            table_widget.setItem(row, 0, QTableWidgetItem(entry.get('name', '')))
            table_widget.setItem(row, 1, QTableWidgetItem(entry.get('qty', '')))
            if table_widget.columnCount() > 2:
                table_widget.setItem(row, 2, QTableWidgetItem(entry.get('remarks', '')))
                
        for row in range(len(data), new_count):
            for col in range(table_widget.columnCount()):
                table_widget.setItem(row, col, QTableWidgetItem(""))

        table_widget.setUpdatesEnabled(True)
        table_widget.blockSignals(False)

    def _require_selection(self, action: str):
        records = self.table_renderer.get_checked_records()
        if not records:
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(
                self, "No Row Selected",
                f"Check at least one row first, then press {action}."
            )
        return records

    def handle_trash_selected(self):
        records = self._require_selection("TRASH")
        if not records:
            return

        current_admin = getattr(self.api, 'admin_under', None)

        own_records     = [r for r in records if r.get('admin_under') == current_admin]
        foreign_records = [r for r in records if r.get('admin_under') != current_admin]

        if foreign_records:
            names = ", ".join(r.get('admin_under', '?') for r in foreign_records)
            QMessageBox.warning(self, "Permission Denied",
                                f"You cannot trash records belonging to: {names}.\n"
                                f"Only your own records will be processed.")

        if not own_records:
            return

        if not self._confirm("Move to Trash",
                            f"Move {len(own_records)} of your record(s) to the recycle bin"):
            return

        self._bulk_operation(
            ids=[r.get('id') for r in own_records],
            operation=lambda rec_id: self.api.move_to_bin(rec_id),
            success_msg="{count} record(s) moved to recycle bin.",
            failed_title="Trash Failed"
        )
        
    def handle_docx_selected(self):
        records = self._require_selection("CONVERT TO DOCUMENT")
        if not records:
            return

        title     = f"Inventory Report — {datetime.now().strftime('%B %d, %Y')}"
        file_name = f"inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"

        try:
            docx_bytes = generate_docx(records, title=title)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate document:\n{e}")
            return

        success, result = self.api.upload_document(title, file_name, docx_bytes)
        if not success:
            QMessageBox.critical(self, "Upload Failed", str(result))
            return

        QMessageBox.information(self, "Success", f"Document saved:\n{file_name}")
        self.table_renderer.clear_all_checks()

        # ── Always ensure the viewer exists and is refreshed ──────────────
        # Create it if it hasn't been opened yet so the file list is ready
        # when the user opens it.  If it IS open, refresh it live.
        if self._docx_viewer is None:
            self._docx_viewer = DocxViewer(self.api, parent=self)

        self._docx_viewer.refresh_file_list()

        # If it's already visible, also bring it to the front
        if self._docx_viewer.isVisible():
            self._docx_viewer.raise_()
            self._docx_viewer.activateWindow()

    def open_docx_viewer(self):
        if self._docx_viewer is None:
            self._docx_viewer = DocxViewer(self.api, parent=self)

        self._docx_viewer.refresh_file_list()
        self._docx_viewer.show()
        self._docx_viewer.raise_()
        self._docx_viewer.activateWindow()

    def handle_edit_dashboard(self, updated_record: dict):
        current_admin = getattr(self.api, 'admin_under', None)
        if updated_record.get('admin_under') != current_admin:
            QMessageBox.warning(self, "Permission Denied",
                                "You can only edit your own records.")
            return

        success, msg = self.api.update_inventory_record(
            updated_record["id"], updated_record
        )
        if success:
            QMessageBox.information(self, "Success", "Record updated.")
            self.load_table_data_dashboard()
        else:
            QMessageBox.critical(self, "Error", f"Failed to update: {msg}")
            
    def handle_logout_dashboard(self):
        reply = QMessageBox.question(
            self,
            'Confirm Logout',
            'Are you sure you want to exit the system?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.logged_out.emit()