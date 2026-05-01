from PyQt5.QtWidgets import QTableWidgetItem

class ChemTableView:
    def _get_table(self):
        raise NotImplementedError("Subclass must implement _get_table function")
    
    def emit_data(self):
        table = self._get_table()
        result = []
        
        for row in range(table.rowCount()):
            name = table.item(row, 0).text().strip() if table.item(row, 0) else ""
            qty = table.item(row, 1).text().strip() if table.item(row, 1) else ""
            remarks = table.item(row, 2).text().strip() if table.item(row, 2) else ""
            
            if name or qty or remarks:
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
        table.blockSignals(True)
    