from PyQt5.QtWidgets import QStyledItemDelegate, QLineEdit

class LiveUpdateDelgate(QStyledItemDelegate):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.textChanged.connect(lambda: self.on_text_changed(editor, index))
        return editor
    
    def on_text_changed(self, editor, index):
        self.commitData.emit(editor)
        self.callback()