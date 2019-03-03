from components.basic.base_component import BaseComponent
from events.events import Observable


class BaseInputComponent(BaseComponent, Observable):
    def __init__(self):
        super().__init__()
