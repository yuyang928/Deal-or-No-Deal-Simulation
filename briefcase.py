import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFont

class Briefcase:
    _closed_img_base = "case_closed.jpg"
    _opened_img_base = "case_opened.jpg"

    def _prepare_image(self, path, text=None, size=(120, 120), text_color="black", border_color=None):
        img = Image.open(path).resize(size)
        draw = ImageDraw.Draw(img)
        if border_color:
            draw.rectangle([0, 0, size[0]-1, size[1]-1], outline=border_color, width=8)
        if text:
            font = ImageFont.truetype("arial.ttf", 18)
            bbox = draw.textbbox((0, 0), text, font=font)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(((size[0]-w)/2, (size[1]-h)/2), text, fill=text_color, font=font)
        return ImageTk.PhotoImage(img)

    def __init__(self, frame, number, value, command):
        self.number = number
        self.value = value

        self.closed_img = self._prepare_image(self._closed_img_base, str(number))
        formatted = f"${value:,.2f}" if value < 1 else f"${value:,.0f}"
        self.opened_img = self._prepare_image(self._opened_img_base, formatted, text_color="gold")
        self.kept_img = self._prepare_image(self._closed_img_base, "Kept", border_color="gold")
        self.button = tk.Button(frame, image=self.closed_img, command=lambda: command(self))

    def grid(self, row, column):
        self.button.grid(row=row, column=column, padx=5, pady=5)

    def open(self):
        self.button.config(image=self.opened_img, state="disabled")

    def keep(self):
        self.button.config(image=self.kept_img, state="disabled")
