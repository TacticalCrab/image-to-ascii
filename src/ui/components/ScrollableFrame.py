import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Canvas inside this frame
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical scrollbar
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Inner frame to hold widgets
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        # Update scroll region when widgets are added
        self.inner_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Enable mousewheel scrolling
        self.bind_all("<MouseWheel>", self._on_mousewheel)      # Windows/Mac

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_mousewheel_linux(self, direction):
        self.canvas.yview_scroll(direction, "units")