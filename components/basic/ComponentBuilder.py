valid_components = []


class BuilderHint():
    def __init__(self, xml_tag_name : str):
        self.tag = xml_tag_name

    def __call__(self, _class_):
        valid_components.append((self.tag,_class_))
        print("Added", _class_.__name__, "with the tag \"", self.tag, "\"")
        return _class_

