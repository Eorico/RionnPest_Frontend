from PyQt5.QtWidgets import (
    QMainWindow, QListWidgetItem, QMessageBox, QPushButton,
    QHBoxLayout, QWidget, QTableWidgetItem, QLabel
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QCursor
from ui.docs_viewer import Ui_DocxViewer


class DocxViewer(QMainWindow):

    def __init__(self, api_service, parent=None):
        super().__init__(parent)
        self.api = api_service
        self.ui  = Ui_DocxViewer()
        self.ui.setupUi(self)

        self._doc_map     = {}
        self._current_doc = None

        self.ui.inventoryTable1.setColumnCount(7)
        for col, txt in enumerate([
            "Category", "Date", "Name of Client", "Time",
            "Chemical/s Used", "Actual Chemical/s Used", "Remarks"
        ]):
            self.ui.inventoryTable1.setHorizontalHeaderItem(
                col, QTableWidgetItem(txt)
            )

        self.ui.filesList.itemClicked.connect(self._on_file_selected)
        self.ui.tocList.itemClicked.connect(self._on_toc_selected)

        self.refresh_file_list()

    # ── File list ─────────────────────────────────────────────────────────────

    def refresh_file_list(self):
        self.ui.filesList.clear()
        self._doc_map.clear()
        docs = self.api.get_documents()
        for doc in docs:
            self._add_file_item(doc)

    def _add_file_item(self, doc: dict):
        item_widget = QWidget()
        item_widget.setStyleSheet("background: transparent;")

        layout = QHBoxLayout(item_widget)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(8)

        file_btn = QPushButton(f"📄  {doc['file_name']}")
        file_btn.setFlat(True)
        file_btn.setCursor(QCursor(Qt.PointingHandCursor))
        file_btn.setStyleSheet("""
            QPushButton {
                color: rgba(198, 246, 213, 0.85);
                background: transparent;
                border: none;
                font: 10pt 'Segoe UI';
                text-align: left;
                padding: 0;
            }
            QPushButton:hover { color: #FFFFFF; }
        """)
        file_btn.clicked.connect(lambda _, d=doc: self._load_document(d))
        layout.addWidget(file_btn, 1)

        del_btn = QPushButton("✕")
        del_btn.setFixedSize(20, 20)
        del_btn.setCursor(QCursor(Qt.PointingHandCursor))
        del_btn.setToolTip("Delete file")
        del_btn.setStyleSheet("""
            QPushButton {
                color: rgba(255, 100, 100, 0.70);
                background: transparent;
                border: none;
                border-radius: 10px;
                font: 8pt 'Segoe UI';
                padding: 0;
            }
            QPushButton:hover {
                color: #FF6B6B;
                background: rgba(255, 80, 80, 0.18);
            }
            QPushButton:pressed {
                background: rgba(255, 80, 80, 0.35);
            }
        """)
        del_btn.clicked.connect(lambda _, d=doc: self._delete_document(d))
        layout.addWidget(del_btn)

        list_item = QListWidgetItem()
        list_item.setSizeHint(QSize(item_widget.sizeHint().width(), 40))
        list_item.setData(Qt.UserRole, doc["id"])
        self.ui.filesList.addItem(list_item)
        self.ui.filesList.setItemWidget(list_item, item_widget)
        self._doc_map[doc["id"]] = doc

    def _delete_document(self, doc: dict):
        reply = QMessageBox.question(
            self, "Delete File",
            f"Delete '{doc['file_name']}'?\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            success, msg = self.api.delete_document(doc["id"])
            if success:
                self.refresh_file_list()
                if self._current_doc and self._current_doc["id"] == doc["id"]:
                    self.ui.inventoryTable1.setRowCount(0)
                    self.ui.tocList.clear()
                    self.ui.docTitleLabel.setText("")
                    self._current_doc = None
            else:
                QMessageBox.critical(self, "Error", f"Failed to delete: {msg}")

    # ── Load document ─────────────────────────────────────────────────────────

    def _on_file_selected(self, item: QListWidgetItem):
        doc_id = item.data(Qt.UserRole)
        doc    = self._doc_map.get(doc_id)
        if doc:
            self._load_document(doc)

    def _load_document(self, doc: dict):
        raw = self.api.download_document(doc["id"])
        if not raw:
            QMessageBox.warning(self, "Error", "Could not download document.")
            return
        records = self._parse_docx_to_records(raw)
        self._current_doc = {"id": doc["id"], "title": doc["file_name"], "records": records}
        self._render_document(records, doc["file_name"])
        self._build_toc(records)

    # ── Render ────────────────────────────────────────────────────────────────

    def _render_document(self, records: list, title: str):
        t = self.ui.inventoryTable1
        t.setSortingEnabled(False)
        t.setRowCount(0)
        self.ui.docTitleLabel.setText(title)

        for r in records:
            row = t.rowCount()
            t.insertRow(row)

            category = (r.get("category") or "").strip().capitalize() or "—"

            # Remarks: col 6 from the docx already contains [C]/[A.C.U] labels.
            # _extract_remarks returns it as-is, or builds the labels fresh
            # if reading live API records (not yet docx-parsed).
            remarks = self._extract_remarks(r)

            values = [
                category,
                f"{r.get('month','')}/{r.get('date','')}/{r.get('year','')}",
                r.get("client_name", "") or "—",
                r.get("start_time", "") or "—",
                self._fmt_chem(r.get("chemical_use") or r.get("chemicals_use") or []),
                self._fmt_chem(
                    r.get("actual_chemicals_used") or r.get("actual_chemical_used") or [],
                    key="actual_chemicals_name"
                ),
                remarks,
            ]

            for col, v in enumerate(values):
                item = QTableWidgetItem(str(v))
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                t.setItem(row, col, item)

        t.setSortingEnabled(True)
        t.resizeRowsToContents()

    def _build_toc(self, records: list):
        self.ui.tocList.clear()
        self.ui.tocList.addItem("1. Inventory Table")
        for i, r in enumerate(records, start=1):
            date_str = f"{r.get('month','')}/{r.get('date','')}/{r.get('year','')}"
            client   = r.get("client_name", "—")
            category = (r.get("category", "") or "").capitalize()
            self.ui.tocList.addItem(
                QListWidgetItem(f"   {i}. [{category}] {client} — {date_str}")
            )
        self.ui.tocList.addItem("2. Statement")

    def _on_toc_selected(self, item: QListWidgetItem):
        text = item.text().strip()
        if text.startswith("1."):
            self.ui.pageScrollArea.verticalScrollBar().setValue(0)
        elif text.startswith("2."):
            self.ui.pageScrollArea.verticalScrollBar().setValue(
                self.ui.pageScrollArea.verticalScrollBar().maximum()
            )

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _extract_remarks(r: dict) -> str:
        """
        Returns remarks with [C] / [A.C.U] labels.

        When reading a parsed docx (col 6 already has the labelled string),
        the top-level r["remarks"] contains it — return directly.

        When reading a live API record, build the labels from the chemical
        entry dicts, same as docs_generator._extract_remarks().
        """
        # 1. Already-labelled string from _parse_docx_to_records (col 6)
        top = (r.get("remarks") or "").strip()
        if top and top != "-":
            return top

        parts = []

        # 2. [C] — from chemical_use entries
        for c in (r.get("chemical_use") or r.get("chemicals_use") or []):
            val = (c.get("remarks") or "").strip()
            if val:
                parts.append(f"[C] {val}")

        # 3. [A.C.U] — from actual_chemical_used entries
        for c in (r.get("actual_chemicals_used") or r.get("actual_chemical_used") or []):
            val = (c.get("remarks") or "").strip()
            if val:
                parts.append(f"[A.C.U] {val}")

        return "; ".join(parts) if parts else "—"

    @staticmethod
    def _fmt_chem(chems: list, key: str = "chemical_name") -> str:
        if not chems:
            return "—"
        parts = []
        for c in chems:
            name = (
                c.get(key)
                or c.get("chemical_name")
                or c.get("actual_chemicals_name")
                or c.get("name")
                or "?"
            )
            parts.append(name)
        return "; ".join(parts)

    @staticmethod
    def _parse_docx_to_records(raw: bytes) -> list:
        from io import BytesIO
        from docx import Document

        try:
            if isinstance(raw, str):
                raw = bytes.fromhex(raw)

            doc = Document(BytesIO(raw))
            if not doc.tables:
                return []

            tbl  = doc.tables[0]
            recs = []

            for row in tbl.rows[1:]:
                cells = [c.text.strip() for c in row.cells]
                if not any(cells):
                    continue

                if len(cells) >= 7:
                    category = cells[0]
                    date_str = cells[1]
                    client   = cells[2]
                    time_str = cells[3]
                    chem     = cells[4]
                    actual   = cells[5]
                    remarks  = cells[6]   # already "[C] x; [A.C.U] y" or "-"
                elif len(cells) == 6:
                    category = ""
                    date_str = cells[0]
                    client   = cells[1]
                    time_str = cells[2]
                    chem     = cells[3]
                    actual   = cells[4]
                    remarks  = cells[5]
                else:
                    continue

                parts = date_str.split("/")
                month = parts[0] if len(parts) > 0 else ""
                day   = parts[1] if len(parts) > 1 else ""
                year  = parts[2] if len(parts) > 2 else ""

                recs.append({
                    "category":              category,
                    "month":                 month,
                    "date":                  day,
                    "year":                  year,
                    "client_name":           client,
                    "start_time":            time_str,
                    "chemical_use":          [{"chemical_name": chem}] if chem else [],
                    "actual_chemicals_used": [{"actual_chemicals_name": actual}] if actual else [],
                    "remarks":               remarks,  # passed through as-is
                })

            return recs

        except Exception:
            import traceback
            traceback.print_exc()
            return []