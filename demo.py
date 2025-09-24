from Lib import XHTApp, XHTWindow

if __name__ == '__main__':
        app = XHTApp.Example()
        app.run(XHTWindow.Window(app.config_path))