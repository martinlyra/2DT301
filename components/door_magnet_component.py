from components.basic.ComponentBuilder import BuilderHint
from components.basic.base_input_component import BaseInputComponent


@BuilderHint("door-magnet")
class DoorMagnetComponent(BaseInputComponent):

    def on_trigger(self, channel):
        super().on_trigger(channel)
