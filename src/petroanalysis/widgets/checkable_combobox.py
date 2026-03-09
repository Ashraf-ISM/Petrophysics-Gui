from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QComboBox


class CheckableCombobox(QComboBox):
    def __init__(self,parent = None):
        super().__init__(parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self.closeOnLineEditClick = False
        self.lineEdit().installEventFilter(self)
        self.view().viewport().installEventFilter(self)
        self.model().dataChanged.connect(self.updateLineEditField)

    def eventFilter(self, widget, event):
        if widget is self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
        elif widget is self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().currentIndex()
                item = self.model().item(index.row())
                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                return True
        return super().eventFilter(widget, event)

    def hidePopup(self):
        super().hidePopup()
        self.startTimer(100)

    def addItems(self, items):
        for text in items:
            self.addItem(text)

    def addItem(self, text):
        super().addItem(text)
        index = self.model().index(self.count() - 1, 0)
        item = self.model().itemFromIndex(index)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)

    def updateLineEditField(self):
        text_container = [self.model().item(i).text() for i in range(self.count()) if
                          self.model().item(i).checkState() == Qt.Checked]
        text_string = ' '.join(text_container)
        self.lineEdit().setText(text_string)
    def getSelectedItems(self):
        selected_items = [self.model().item(i).text() for i in range(self.count()) if
                          self.model().item(i).checkState() == Qt.Checked]
        return selected_items
    def setItemsSelected(self,list_of_items):
        for item in list_of_items:
            index = self.findText(item)
            if index >= 0:
                self.model().item(index).setCheckState(Qt.Checked)
        self.updateLineEditField()
