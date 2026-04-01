import FreeSimpleGUI as sg
import os
from PIL import Image
import io
from processing_list import ImgNegative, ImgRotate

#FUNGSI PREVIEW 
def create_preview(image_or_path, max_size=380):
    if isinstance(image_or_path, str):
        img = Image.open(image_or_path)
    else:
        img = image_or_path.copy()
    img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()

#LAYOUT 
file_list_column = [
    [sg.Text("Open Image Folder :")],
    [sg.In(size=(20, 1), enable_events=True, key="ImgFolder"),
     sg.FileBrowse(button_text="Browse", file_types=(("Image Files", "*.png *.jpg *.jpeg *.gif"),))],
    [sg.Text("Choose an image from list :")],
    [sg.Listbox(values=[], enable_events=True, size=(18, 10), key="ImgList")],
]

image_viewer_column = [
    [sg.Text("Image Input :")],
    [sg.Text(size=(40, 1), key="FilepathImgInput")],
    [sg.Image(key="ImgInputViewer", size=(380, 380))],
]

list_processing = [
    [sg.Text("Image Information:")],
    [sg.Text(size=(20, 1), key="ImgSize")],
    [sg.Text(size=(20, 1), key="ImgColorDepth")],
    [sg.Text("List of Processing:")],
    [sg.Button("Image Negative", size=(20, 1), key="ImgNegative")],
    [sg.Button("Image Rotate", size=(20, 1), key="ImgRotate")],
    [sg.Button("Reset Image", size=(20, 1), key="Reset", button_color=("white", "red"))],
]

image_viewer_column2 = [
    [sg.Text("Image Processing Output:")],
    [sg.Text(size=(40, 1), key="ImgProcessingType")],
    [sg.Image(key="ImgOutputViewer", size=(380, 380))],
]

layout = [[
    sg.Column(file_list_column), sg.VSeperator(),
    sg.Column(image_viewer_column), sg.VSeperator(),
    sg.Column(list_processing), sg.VSeperator(),
    sg.Column(image_viewer_column2),
]]

window = sg.Window("Mini Image Editor", layout, finalize=True)

current_image_path = None
current_coldepth = None
original_image = None          
current_output_image = None    

#EVENT LOOP 
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    # BROWSE FOLDER 
    if event == "ImgFolder":
        path = values["ImgFolder"].strip()
        if not path:
            continue

        if os.path.isfile(path):
            folder = os.path.dirname(path)
            selected_file = os.path.basename(path)
            window["ImgFolder"].update(folder)
        else:
            folder = path
            selected_file = None

        try:
            file_list = os.listdir(folder)
        except:
            file_list = []

        fnames = [f for f in file_list if os.path.isfile(os.path.join(folder, f)) 
                  and f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

        window["ImgList"].update(fnames)

        window["ImgSize"].update("")
        window["ImgColorDepth"].update("")
        window["FilepathImgInput"].update("")
        window["ImgProcessingType"].update("")
        window["ImgInputViewer"].update(data=b"")
        window["ImgOutputViewer"].update(data=b"")
        current_image_path = None
        current_coldepth = None
        original_image = None
        current_output_image = None

        if selected_file and selected_file in fnames:
            filename = os.path.join(folder, selected_file)
            current_image_path = filename
            window["FilepathImgInput"].update(filename)
            window["ImgProcessingType"].update(filename)

            try:
                img_original = Image.open(filename)
                original_image = img_original.copy()
                current_output_image = img_original.copy()  

                preview_data = create_preview(filename)
                window["ImgInputViewer"].update(data=preview_data)
                window["ImgOutputViewer"].update(data=preview_data)

                w, h = img_original.size
                window["ImgSize"].update(f"Image Size : {w} x {h}")

                mode_to_coldepth = {"1":1, "L":8, "P":8, "RGB":24, "RGBA":32,
                                    "CMYK":32, "YCbCr":24, "LAB":24, "HSV":24,
                                    "I":32, "F":32}
                current_coldepth = mode_to_coldepth.get(img_original.mode, 0)
                window["ImgColorDepth"].update(f"Color Depth : {current_coldepth}")
            except:
                pass

    #PILIH DARI LIST 
    elif event == "ImgList" and values["ImgList"]:
        filename = os.path.join(values["ImgFolder"], values["ImgList"][0])
        current_image_path = filename
        window["FilepathImgInput"].update(filename)
        window["ImgProcessingType"].update(filename)

        try:
            img_original = Image.open(filename)
            original_image = img_original.copy()
            current_output_image = img_original.copy()  

            preview_data = create_preview(filename)
            window["ImgInputViewer"].update(data=preview_data)
            window["ImgOutputViewer"].update(data=preview_data)

            w, h = img_original.size
            window["ImgSize"].update(f"Image Size : {w} x {h}")

            mode_to_coldepth = {"1":1, "L":8, "P":8, "RGB":24, "RGBA":32,
                                "CMYK":32, "YCbCr":24, "LAB":24, "HSV":24,
                                "I":32, "F":32}
            current_coldepth = mode_to_coldepth.get(img_original.mode, 0)
            window["ImgColorDepth"].update(f"Color Depth : {current_coldepth}")
        except:
            pass

    #TOMBOL PROCESSING 
    if event in ("ImgNegative", "ImgRotate") and current_image_path and current_coldepth is not None:
        try:
            if event == "ImgNegative":
                img_to_process = current_output_image if current_output_image else Image.open(current_image_path)
                img_output = ImgNegative(img_to_process, current_coldepth)
                proc_text = "Image Negative"

            elif event == "ImgRotate":
                img_to_process = current_output_image if current_output_image else Image.open(current_image_path)
                img_output = ImgRotate(img_to_process)
                proc_text = "Image Rotate (90°)"

           
            current_output_image = img_output.copy()

            processed_preview = create_preview(img_output)
            window["ImgOutputViewer"].update(data=processed_preview)
            window["ImgProcessingType"].update(proc_text)

        except Exception as e:
            sg.popup_error(f"Gagal memproses:\n{str(e)}")

    #TOMBOL RESET 
    elif event == "Reset" and original_image is not None:
        try:
            current_output_image = original_image.copy()  
            processed_preview = create_preview(original_image)
            window["ImgOutputViewer"].update(data=processed_preview)
            window["ImgProcessingType"].update("Original Image (Reset)")
        except Exception as e:
            sg.popup_error(f"Gagal reset gambar:\n{str(e)}")

window.close()