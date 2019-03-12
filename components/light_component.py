import time

from components.basic.ComponentBuilder import BuilderHint
from components.basic.base_component import BaseComponent


@BuilderHint("light")
class LightComponent(BaseComponent):
    state = 0
    
    def toggle(self, override=None):
        if override is None:
            if self.state == 0:
                self.state = 1
            else:
                self.state = 0
        else:
            self.state = override
            
        for pin in self.pins:
            if pin.is_output():
                pin.write(self.state)
                
