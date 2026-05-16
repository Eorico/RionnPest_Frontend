from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from enum import Enum

class RowAction(Enum):
    ADD = "add"
    DELETE = "delete"

class ChemTableView:
    def _get_table(self):
        raise NotImplementedError("Subclass must implement _get_table function")
    
    def emit_data(self, *args):
        table = self._get_table()
        result = []
        
        for row in range(table.rowCount()):
            name = table.item(row, 0).text().strip() if table.item(row, 0) else ""
            qty = table.item(row, 1).text().strip() if table.item(row, 1) else ""
            remarks = table.item(row, 2).text().strip() if table.item(row, 2) else ""
            
 
            result.append({
                "name": name,
                "qty": qty,
                "remarks": remarks
            })
                
        self.data_changed.emit(result)
            
    def load_data(self, data: list):
        table = self._get_table()
        table.blockSignals(True)
        for row in range(table.rowCount()):
            entry = data[row] if row < len(data) else {}
            table.setItem(row, 0, QTableWidgetItem(entry.get("name", "")))
            table.setItem(row, 1, QTableWidgetItem(entry.get("qty", "")))
            table.setItem(row, 2, QTableWidgetItem(entry.get("remarks", "")))
            
        table.blockSignals(False)
        
    def operation_row(self, action: RowAction):
        table = self._get_table()
        if action == RowAction.ADD:
            new_row = table.rowCount()
            table.insertRow(new_row)
            for col in range(3):
                table.setItem(new_row, col, QTableWidgetItem(""))
            self.refresh_row_numbers()
            table.scrollToBottom()
            table.setCurrentCell(new_row, 0)
            self.emit_data()
        elif action == RowAction.DELETE:
            current = table.currentRow()
            row_to_delete = current if current >= 0 else table.rowCount() - 1
            if row_to_delete >= 0:
                table.removeRow(row_to_delete)
                self.refresh_row_numbers()
                self.emit_data()
    
    def refresh_row_numbers(self):
        table = self._get_table()
        for row in range(table.rowCount()):
            item = QTableWidgetItem(str(row + 1))
            item.setTextAlignment(Qt.AlignCenter)