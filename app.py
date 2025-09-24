from Lib import XHTApp, XHTWindow
import os

work_path = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(work_path, "config")

if __name__ == '__main__':
        app = XHTApp.Example()
        app.run(XHTWindow.Window(config_path))