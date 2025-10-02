from PySide6.QtWidgets import QLabel
import uuid

class LabelElement(QLabel):
    def __init__(self, parent=None, text:str=""):
        super().__init__(parent)
        self.setText(text) 
        self.uuid = str(uuid.uuid4())

    def getUUID(self):
        return self.uuid
    
class ElementList(list):
    def __init__(self):
        super().__init__()

    def addElement(self, element:LabelElement):
        self.append(element)
    
    def getElements(self):
        return self
    
    def setElement(self, new_element:LabelElement, element_id:str = None):
        if element_id is None:
            element_id = new_element.uuid
        for i, e in enumerate(self):
            if e.uuid == element_id:
                self[i] = new_element
                return
        raise ValueError("Element not found in the list.")

    def delElement(self, element:LabelElement):
        if element in self:
            self.remove(element)
        else:
            raise ValueError("Element not found in the list.")