import cv2
import gradio
import numpy
import os
import PIL
import pillow_heif

pillow_heif.register_heif_opener()

class HIEC2Any():
    def __init__(self):
        self.title = gradio.Markdown("# HEIC to Any Converter", render = False)
        self.app = gradio.Blocks()  
        self.input_file = gradio.File(label = "Select HEIC file", file_types = [".heic"], type = "filepath", render = False)
        self.image_display = gradio.Image(show_download_button = False, render = False)
        self.convert_button = gradio.Button("Convert", render = False)
        self.download_button = gradio.DownloadButton("Download", interactive = False, render = False)
        self.type_mode = gradio.Radio(["jpg", "png"], label = "Select output file type", render = False)
        self.__render()
        
    
    def __render(self):
        with self.app:
            self.title.render()
            self.input_file.render()
            self.type_mode.render()
            self.convert_button.render()
            self.image_display.render()
            self.download_button.render()
            
            self.__set_behavior()
    
    def __set_behavior(self):
        self.convert_button.click(self.convert, inputs = [self.input_file, self.type_mode], outputs = [self.image_display, self.download_button])
        
    def convert(self, input_file, type_mode):
        image = PIL.Image.open(input_file)
        print(type_mode)
        
        if image is None:
            self.download_button.interactive = False
            self.download_button.render()
            return None
        
        image = image.convert("RGB")
        image_np = numpy.array(image)
        image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        file_dir = os.path.dirname(input_file)
        file_name = f"{os.path.basename(input_file).split('.')[0]}.{type_mode}"
        
        cv2.imwrite(f"{os.path.join(file_dir, file_name)}", image_cv)
        download_button = gradio.DownloadButton("Download", value = os.path.join(file_dir, file_name), interactive = True)
        
        return [image_np, download_button]
    
    def launch(self):
        self.app.launch(width = 400)

app = HIEC2Any()
app.launch()
