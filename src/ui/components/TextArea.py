from tkinter import Text

class TextArea(Text):
    MIN_FONT_SIZE = 4
    font_size = 12

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        super().config(wrap="none", font=("Courier", self.font_size))
        self._setup_on_scroll_resize()

    def insert_text(self, text):
        self.delete("1.0", "end")
        self.insert("1.0", text)
        self.see("end")

    def config(self, **kwargs):
        super().config(**kwargs)
    
    def _setup_on_scroll_resize(self):
        self.bind("<MouseWheel>", self._on_mouse_wheel)
    
    def _on_mouse_wheel(self, event):
        if not (event.state & 0x0004):
            return

        if event.delta > 0:
            self.font_size += 1
        
        elif self.font_size == self.MIN_FONT_SIZE:
            self.font_size = self.MIN_FONT_SIZE

        else:
            self.font_size -= 1
        
        super().config(font=("Courier", self.font_size))