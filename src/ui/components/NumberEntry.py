import tkinter as tk

class NumberEntry(tk.Entry):
    def __init__(self, master=None, command=None, min=0, max=100, **kwargs):
        super().__init__(master, **kwargs)
        self.min = min
        self.max = max
        self.command = command

        self.var = tk.StringVar()
        self.var.set(min)
        self.config(textvariable=self.var)

        self._setup_validate_number()
        self._setup_command()
        self._bind_arrow_keys()
    
    def _setup_validate_number(self):
        self.config(validate="key", validatecommand=(self.register(self._check_number), '%P'))

    def _setup_command(self):
        if self.command:
            self.var.trace_add("write", lambda *args: self.command(int(self.var.get() if self.var.get() else 0)))

    def _bind_arrow_keys(self):
        self.bind("<Up>", lambda e: self.var.set(min(self.max, int(self.var.get() if self.var.get() else 0) + 1)))
        self.bind("<Down>", lambda e: self.var.set(max(self.min, int(self.var.get() if self.var.get() else 0) - 1)))

    def _check_number(self, value):
        if not value:
            return True
        try:
            value = int(value)
            if self.min <= value <= self.max:
                return True
            else:
                return False
        except ValueError:
            return False
        
    def get(self):
        try:
            return int(self.var.get())
        except ValueError:
            return 0