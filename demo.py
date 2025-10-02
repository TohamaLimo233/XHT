from Lib import XHTApp, XHTWindow, Element

if __name__ == '__main__':
        app = XHTApp.Example()
        el=Element.LabelElement(text="100000000")
        es=Element.ElementList()
        es.addElement(el)
        window = XHTWindow.Window(app.config_path, es)
        window.AddTrayMenu("退出1", window.close)
        app.run(window)

        el.setText("200000000")
        # 修复：调整setElement参数顺序
        es.setElement(el, el.uuid)
        app.window.setElementList(es)