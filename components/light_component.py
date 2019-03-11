import time

from components.basic.ComponentBuilder import BuilderHint
from components.basic.base_component import BaseComponent


@BuilderHint("light")
class LightComponent(BaseComponent):
    state = 0
    
    def toggle(self):
        if self.state == 0:
            self.state = 1
        else:
            self.state = 0
            
        for pin in self.pins:
            if pin.is_output():
                pin.write(self.state)
                
