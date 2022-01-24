import disnake
from . import config

class Link(disnake.ui.View):
    def __init__(self):
        super().__init__()
        name = config.button_name
        link = config.link
        self.add_item(disnake.ui.Button(label=name, url=link))