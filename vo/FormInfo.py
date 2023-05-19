class FormInfo:
    def __init__(self, name, title, classname, small_client_width):
        self.name: str = name
        self.title: str = title
        self.classname: str = classname if classname else None
        self.small_client_width: int = int(small_client_width) if small_client_width else 0

    def enable_change_rect(self):
        return self.small_client_width > 0
