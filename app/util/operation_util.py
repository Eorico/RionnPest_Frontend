from PyQt5.QtWidgets import QMessageBox

class Operation:
    # Reusable helper functions across the system
    
    def _get_checked_ids(self) -> list:
        raise NotImplementedError
    
    def _clear_checks(self):
        raise NotImplementedError
    
    def _reload(self):
        raise NotImplementedError
    
    def _require_check(self, action: str) ->  list:
        ids = self._get_checked_ids()
        if not ids:
            QMessageBox.warning(
                self, "No Selection",
                f"Check at least one record to {action}"
            )
        return ids
    
    def _confirm(self, title: str, message: str) -> bool:
        return QMessageBox.question(
            self, title, message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        ) == QMessageBox.Yes
        
    def _bulk_operation(
        self, 
        ids: list,
        success_msg: str,
        operation: str,
        failed_title: str,
        after_reload=None
    ):
        
        failed = []
        
        for rec_id in ids:
            ok, msg = operation(rec_id)
            if not ok:
                failed.append(str(msg))
                
        self._clear_checks()
        self._reload()
        
        if callable(after_reload):
            after_reload()
            
        if failed:
            QMessageBox.critical(
                self, failed_title,
                f"{len(failed)} record(s) failed:\n" + "\n".join(failed)
            )
        else:
            QMessageBox.information(
                self, "Success",
                success_msg.format(count=len(ids))
            )