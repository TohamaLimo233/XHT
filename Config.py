import json
import os


class Config:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), "config.json")
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, "r") as f:
                config = json.load(f)
            return config
        except FileNotFoundError:
            raise FileNotFoundError
