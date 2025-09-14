from utils.braille_utils import array_to_ascii, array_to_braille
from utils.image_to_braille import image_to_braille
from tkinter import StringVar, Tk, filedialog, Label, Button, PanedWindow, Frame, BooleanVar, Checkbutton
from tkinter.ttk import Combobox
from PIL import ImageTk, Image

from ui.components import TextArea, NumberEntry

DEFAULT_AUTO_UPDATE_IMAGE = True

ascii_transformers = {
    "array_to_ascii": {
        "function": array_to_ascii,
        "char_pixel_dimentions": (3, 2)
    },
    "array_to_braille": {
        "function": array_to_braille,
        "char_pixel_dimentions": (4, 2)
    }
}

class App(Tk):

    def __init__(self):
        super().__init__()

        self.current_image = None
        self.current_image_path = None
        self.auto_update_var = BooleanVar(value=DEFAULT_AUTO_UPDATE_IMAGE)

        self.title("Image to Braille Converter")
        self.geometry("600x600")

        self.root_pane = PanedWindow(self, orient="vertical", sashrelief="raised")
        self.root_pane.pack(fill="both", expand=True)
        
        self.top_frame = Frame(self.root_pane)
        self.root_pane.add(self.top_frame)

        self.bottom_frame = Frame(self.root_pane)
        self.root_pane.add(self.bottom_frame)

        self.top_pane = PanedWindow(self.top_frame, orient="horizontal", sashrelief="raised")
        self.top_pane.pack(side="top", fill="both", expand=True)

        self.left_frame = Frame(self.top_pane, width=800)
        self.top_pane.add(self.left_frame)
        self.resize_after_id = None
        self.bind("<Configure>", lambda _: self._on_resize_image_frame())

        self.right_frame = Frame(self.top_pane, width=200)
        self.top_pane.add(self.right_frame)

        self.imageLabel = Label(self.right_frame, text="No image selected")
        self.imageLabel.pack(fill="both", expand=True)

        self._create_shrink_factor(self.left_frame)
        self._create_threshold(self.left_frame)
        self._create_invert_color(self.left_frame)
        self._create_auto_update(self.left_frame)
        self._create_option_ascii_transformer(self.left_frame)

        self.button = Button(self.left_frame, text="Select Image", command=lambda: self._select_image())
        self.button.pack(anchor="w")

        self.asciiText = TextArea(self.bottom_frame)
        self.asciiText.pack(fill="both", expand=True)
        self.bind("<Control-u>", lambda event: self._on_key_toggle_auto_update(event))
        self.bind("<Control-i>", lambda event: self._on_key_toggle_invert_color(event))

    def _create_shrink_factor(self, master):
        self.shrink_factor_frame = Frame(master)
        self.shrink_factor_frame.pack(fill="x")
        self.shrink_factor_label = Label(self.shrink_factor_frame, text="Shrink Factor (0-20):")
        self.shrink_factor_label.pack(side="left")
        self.shrink_factor = NumberEntry(
            self.shrink_factor_frame, 
            min=0, 
            max=20,
            command=lambda _=None: self._display_ascii_image()
        )
        self.shrink_factor.delete(0, 'end')
        self.shrink_factor.insert(0, "0")
        self.shrink_factor.pack(side="left")
    
    def _create_threshold(self, master):
        self.threshold_frame = Frame(master)
        self.threshold_frame.pack(fill="x")
        self.threshold_label = Label(self.threshold_frame, text="Threshold (0-255):")
        self.threshold_label.pack(side="left")
        self.threshold = NumberEntry(
            self.threshold_frame,
            min=0,
            max=255,
            command=lambda _=None: self._display_ascii_image()
        )
        self.threshold.delete(0, 'end')
        self.threshold.insert(0, "40")
        self.threshold.pack(side="left")

    def _create_invert_color(self, master):
        self.invert_color_var = BooleanVar(value=False)
        self.invert_color_checkbox = Checkbutton(
            master, 
            text="Invert Colors", 
            variable=self.invert_color_var,
            command=lambda: self._display_ascii_image()
        )
        self.invert_color_checkbox.pack(anchor="w")
    
    def _on_key_toggle_invert_color(self, event):
        if not (event.state & 0x0004):
            return

        self.invert_color_var.set(not self.invert_color_var.get())
        self._display_ascii_image()

    def _create_auto_update(self, master):
        self.auto_update_checkbox = Checkbutton(
            master, 
            text="Auto Update", 
            variable=self.auto_update_var,
            command=lambda: self._on_checkbox_click_toggle_auto_update()
        )
        self.auto_update_checkbox.pack(anchor="w")
    
    def _create_option_ascii_transformer(self, master):
        self.ascii_transformer_var = StringVar(master)
        self.ascii_transformer_var.set("array_to_braille")
        self.ascii_transformer_checkbox = Combobox(
            master,
            textvariable=self.ascii_transformer_var,
            values = list(ascii_transformers.keys()),
        )
        self.ascii_transformer_checkbox.bind("<<ComboboxSelected>>", lambda _: self._display_ascii_image()) 
        self.ascii_transformer_checkbox.pack(anchor="w")

    def _on_checkbox_click_toggle_auto_update(self):
        if self.auto_update_var.get():
            self._display_ascii_image()

    def _on_key_toggle_auto_update(self, event):
        if not (event.state & 0x0004):
                return

        self.auto_update_var.set(not self.auto_update_var.get())
        if self.auto_update_var.get():
            self._display_ascii_image()

    def _on_resize_image_frame(self):
        if self.resize_after_id:
            self.after_cancel(self.resize_after_id)
        self.resize_after_id = self.after(100, lambda: self._display_image_preview())

    def _select_image(self):
        self.current_image_path = self._open_file_dialog()
        if not self.current_image_path:
            return

        self.current_image = Image.open(self.current_image_path)
        self._display_image_preview()
        self._display_ascii_image()
        self._after_image_display()
    
    def _display_image_preview(self):
        if not self.current_image_path:
            return

        img = self._format_display_image(self.current_image)
        img = ImageTk.PhotoImage(img)

        self.imageLabel.config(
            image=img,
            text="",
        )
        self.imageLabel.image = img

    def _format_display_image(self, img):
        resize = lambda w, h, sf: img.resize((int(w * sf), int(h * sf)), Image.NEAREST)

        scale_w = self.right_frame.winfo_width() / img.width
        scale_h = self.right_frame.winfo_height() / img.height
        scale_factor = min(scale_w, scale_h, 1.0)

        if scale_factor < 1.0:
            img = resize(img.width, img.height, scale_factor)

        return img

    def _display_ascii_image(self):
        if not self.auto_update_var.get() or not self.current_image_path:
            return

        buffer = self._convert_image(self.current_image)
        self.asciiText.config(width=100, height=20)
        self.asciiText.insert_text(buffer)
        self.asciiText.pack(fill="both", expand=True)

    def _after_image_display(self):
        self.shrink_factor.config(state="normal")
        self.threshold.config(state="normal")

    def _open_file_dialog(self):
        return filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
    
    def _convert_image(self, image: Image.Image):
        return image_to_braille(
            image=image,
            pixel_transformer=ascii_transformers[self.ascii_transformer_var.get()]["function"],
            scale_factor=self.shrink_factor.get(),
            threshold=self.threshold.get(),
            invert_color=self.invert_color_var.get(),
            char_pixel_dimentions=ascii_transformers[self.ascii_transformer_var.get()]["char_pixel_dimentions"]
        )