import os
from PIL import Image
from kivymd.uix.filemanager import MDFileManager
from kivymd.app import MDApp
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.core.window import Window
from pytesseract import pytesseract

Window.size = (500, 500)


class ExtractingTextApp(MDApp):
    def __init__(self):
        super().__init__()
        self.path_to_tesseract = None
        self.image_file = None
        self.extract_button = None
        self.image_text = None
        self.choose_button = None
        self.location_label = None
        self.title = "Extracting Text App"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
        )

    def move_label(self, obj):
        text = self.location_label.text
        updated_text = text[1:] + text[0]
        self.location_label.text = updated_text

    def open_file_manager(self, obj):
        self.file_manager.show(os.getcwd())

    def select_path(self, path):
        if path.lower().endswith(('.jpg', '.png', '.jpeg')):
            self.file_manager.close()
            self.image_file = path
            location_text = " ..... " + "Selected location:..." + self.image_file + " ..... "
            self.location_label.text = location_text
            self.extract_button.disabled = False
            self.choose_button.disabled = False
        else:
            self.file_manager.close()
            self.location_label.text = "Invalid file format. Please choose an image file."
            Clock.schedule_once(self.reset_location_label, 3)  # Reset label after 3 seconds

    def reset_location_label(self, dt):
        self.location_label.text = "Please select an Image to extract text from........"

    def extract_text(self, obj):
        if self.image_file:
            self.path_to_tesseract = r"/usr/local/Cellar/tesseract/5.3.2_1/bin/tesseract"
            pytesseract.tesseract_cmd = self.path_to_tesseract
            img = Image.open(self.image_file)
            text = pytesseract.image_to_string(img)
            self.image_text.text = text
            if text != "":
                self.location_label.text = "...... Text extracted successfully! ....... "
                print(text)
            else:
                self.location_label.text = ".......  No text on the image or Text extraction failed!   .... "

    def exit_manager(self, *args):
        self.file_manager.close()

    def build(self):
        self.root = MDRelativeLayout(md_bg_color=(0.1, 0.1, 0.1, 1))
        self.image_text = TextInput(
            text="",
            pos_hint={"center_x": 0.5, "center_y": 0.62},
            size_hint=(.7, .7),
            height=480,
            width=560,
            foreground_color=(0, .5, .5),
            font_size=40,
            readonly=True,
        )
        self.root.add_widget(self.image_text)
        self.location_label = Label(
            text="..... Please select an Image to extract text from ........",
            pos_hint={"center_x": 0.5, "center_y": 0.175},
            size_hint=(.8, .8),
            height=50,
            width=560,
            color=(1, .5, 0),
            font_size=40,
        )
        self.root.add_widget(self.location_label)
        self.choose_button = Button(
            text="Choose Image",
            pos_hint={"center_x": 0.375, "center_y": 0.1},
            size_hint=(.2, .1),
            height=50,
            width=100,
            background_color=(1, .5, 0),
            bold=True,
            on_press=self.open_file_manager,
            disabled=False,
        )
        self.root.add_widget(self.choose_button)

        self.extract_button = Button(
            text="Extract Text",
            pos_hint={"center_x": 0.625, "center_y": 0.1},
            size_hint=(.2, .1),
            height=50,
            width=100,
            background_color=(1, .5, 0),
            bold=True,
            on_press=self.extract_text,
            disabled=True,
        )
        self.root.add_widget(self.extract_button)

        Clock.schedule_interval(self.move_label, .1)
        return self.root


if __name__ == "__main__":
    ExtractingTextApp().run()
