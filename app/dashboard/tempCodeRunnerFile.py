from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from ui.dashboard import Ui_Dashboard, DashboardController
from .dashboard_renderer import DashboardTableRenderer
from util.dashboard_util import DashboardFormatter
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

        self.table_renderer = DashboardTableRenderer(
            self.ui.tableListahan,
            self.handle_trash_dashboard
        )
        
        
            
        self._setup_table()
        # self.status_mode_internet_dashboard()
        self.bind_event_dashboard()
        self.load_table_data_dashboard()

    def _setup_table(self):
        self.ui.tableListahan.setWordWrap(True)
        self.ui.tableListahan.verticalHeader().setSectionResizeMode(
            self.ui.tableListahan.verticalHeader().ResizeToContents
        )

        self.ui.tableListahan.setColumnWidth(3, 350)
        self.ui.tableListahan.setColumnWidth(4, 350)
        self.ui.tableListahan.setColumnWidth(5, 350)

    def bind_event_dashboard(self):
        self.ui.confirmButton.clicked.connect(self.handle_submit_dashboard)
        self.ui.inspection.triggered.connect(lambda: self.switch_mode_category_dashboard('inspection'))
        self.ui.treatment.triggered.connect(lambda: self.switch_mode_category_dashboard('treatment'))
        self.ui.logout.triggered.connect(self.handle_logout_dashboard)
        self.ui.searchDate.textChanged.connect(self.handle_search_input_dashboard)

    # def status_mode_internet_dashboard(self):
    #     if self.api:
    #         self.is_online = self.api.check_connection_service()

    #     img = "online.png" if self.is_online else "offline.png"
    #     pixmap = QPixmap(os.path.join(IMAGE_PATH, img))

    #     if not pixmap.isNull():
    #         lbl = self.ui.label_16
    #         w, h = (lbl.width() or 40), (lbl.height() or 40)
    #         lbl.setPixmap(pixmap.scaled(w, h, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def switch_mode_category_dashboard(self, mode):
        self.current_category = mode

        self.ui.label_2.setText(f"Client - {mode}")
        self.ui.label_3.setText(f"Date of {mode}")
        self.ui.label_4.setText(f"Time of {mode}")
        self.ui.label_5.setText(f"Chemical/s Used - {mode}")
        self.ui.label_6.setText(f"Actual Chemical/s Used - {mode}")
        self.ui.label_17.setText(f"({mode})")

        headers = [
            (0, "Admin"),
            (1, f"Date of ({mode})"),
            (2, f"Name of Client - ({mode})"),
            (3, f"Time of ({mode})"),
            (4, f"Chemical/s Used - ({mode})"),
            (5, f"Actual Chemical/s Used - ({mode})"),
            (6, "Edit"),
            (7, "Trash"),
        ]

        for col, text in headers:
            self.ui.tableListahan.setHorizontalHeaderItem(col, QTableWidgetItem(text))

        self.load_table_data_dashboard()

    def handle_submit_dashboard(self):

        def extract(table, key):
            results = []
            for row in range(table.rowCount()):
                name_item = table.item(row, 0)
                qty_item = table.item(row, 1)

                if name_item and name_item.text().strip():
                    results.append({
                        key: name_item.text().strip(),
                        "quantity": qty_item.text().strip() if qty_item else "0"
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
                "meridiem": self.ui.PM_or_AM.currentText(),
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
        
    def handle_trash_dashboard(self, rec_id):
        if rec_id is None:
            return

        reply = QMessageBox.question(
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

        self.ui.chemicalUsed.clearContents()
        self.ui.actualchemicalUsed.clearContents()