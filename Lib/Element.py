from PySide6.QtWidgets import QLabel

class LabelElement(QLabel):
    def __init__(self, parent=None, order:int=1, text:str=""):
        super().__init__(parent)
        self.order=0
        self.SetOrder(order)
        self.setText(text)
    
    def SetOrder(self, order:int=1):
        """设置显示顺序"""
        if self.order < 0:
            raise ValueError("order must be a value between 0 and 10")
        else:
            self.order=order
        return
    def GetOrder(self):
        """获取显示顺序"""
        return self.order