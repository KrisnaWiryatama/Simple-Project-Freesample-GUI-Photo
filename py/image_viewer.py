import FreeSimpleGUI as sg
import os.path
from PIL import Image
from processing_list import *

# ======================= HELPER: Dynamic display size =======================
def get_display_size(img_pil, max_w=480, max_h=480):
    """Hitung ukuran tampilan proporsional tanpa memotong gambar."""
    if img_pil is None:
        return (max_w, max_h)
    w, h = img_pil.size
    ratio = min(max_w / w, max_h / h, 1.0)  
    return (int(w * ratio), int(h * ratio))

def get_display_image_dynamic(img_pil, max_w=480, max_h=480):
    """Simpan preview dengan ukuran dinamis sesuai gambar, tanpa crop."""
    if img_pil is None:
        return None
    img_temp = img_pil.copy()
    img_temp.thumbnail((max_w, max_h), Image.LANCZOS)
    temp_path = "temp_gui_preview.png"
    img_temp.save(temp_path)
    return temp_path

def get_display_image_dynamic2(img_pil, max_w=480, max_h=480):
    """Simpan preview ke file berbeda agar tidak tabrakan dengan preview 1."""
    if img_pil is None:
        return None
    img_temp = img_pil.copy()
    img_temp.thumbnail((max_w, max_h), Image.LANCZOS)
    temp_path = "temp_gui_preview2.png"
    img_temp.save(temp_path)
    return temp_path

def get_display_image_dynamic3(img_pil, max_w=480, max_h=480):
    """Simpan preview output."""
    if img_pil is None:
        return None
    img_temp = img_pil.copy()
    img_temp.thumbnail((max_w, max_h), Image.LANCZOS)
    temp_path = "temp_gui_preview3.png"
    img_temp.save(temp_path)
    return temp_path

def update_output_info(window, img_out, process_name):
    """Memperbarui teks informasi untuk panel Output Image Info."""
    if img_out:
        w, h = img_out.size
        window["OutImgSize"].update(f"Size : {w} x {h}")
        
        # Deteksi color depth output
        mode_to_coldepth = {"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32}
        c_depth = mode_to_coldepth.get(img_out.mode, 24)
        window["OutImgColorDepth"].update(f"Color Depth : {c_depth} bit")
        window["OutImgProcess"].update(f"Process : {process_name}")

# ======================= KONSTANTA UKURAN TAMPILAN =======================
# Maksimal tampilan per panel (dalam pixel GUI)
# Untuk 512x512 → tampil 480x480, untuk 256x256 → tampil 256x256 (tidak di-upscale)
MAX_DISPLAY = 480

# ======================= LAYOUT =======================

# --- Panel Kiri: File Browser + Info ---
file_list_column = [
    [sg.Text("Open Image Folder :")],
    [sg.In(size=(22, 1), enable_events=True, key="ImgFolder"), sg.FolderBrowse()],
    [sg.Text("Choose an image from list :")],
    [sg.Listbox(values=[], enable_events=True, size=(22, 8), key="ImgList")],
    [sg.HSeparator()],

    # Bagian Informasi Gambar Input
    [sg.Text("─── Input Image Info ───", font=("Helvetica", 9, "bold"), text_color="#ffffff")],
    [sg.Text("Size : -", size=(24, 1), key="ImgSize")],
    [sg.Text("Color Depth : -", size=(24, 1), key="ImgColorDepth")],
    [sg.HSeparator()],
    
    # Bagian Informasi Gambar Output (Baru & Dinamis)
    [sg.Text("─── Output Image Info ───", font=("Helvetica", 9, "bold"), text_color="#ffffff")],
    [sg.Text("Size : -", size=(24, 1), key="OutImgSize")],
    [sg.Text("Color Depth : -", size=(24, 1), key="OutImgColorDepth")],
    [sg.Text("Process : None", size=(24, 2), key="OutImgProcess")], # Menampilkan detail proses/kernel
    [sg.HSeparator()],
    
    # Blend panel
    [sg.pin(sg.Column([
        [sg.Text("─── Blend Mode ───", font=("Helvetica", 9, "bold"))],
        [sg.Button("Select 2nd Image", key="ImgSelect2", size=(20, 1))],
        [sg.Text("Opacity (%):")],
        [sg.Slider(range=(0, 100), orientation='h', default_value=50,
                   key="BlendAlpha", enable_events=True, size=(18, 12))],
        [sg.Image(key="ImgInputViewer2", size=(200, 150))],
    ], key="ColBlend", visible=False))],
]

# --- Panel Tengah: Input Image ---
image_input_column = [
    [sg.Text("Image Input :", font=("Helvetica", 10, "bold"))],
    [sg.Text("", size=(50, 1), key="FilepathImgInput")],
    # Gunakan pad dan size agar panel tidak collapse
    [sg.Image(key="ImgInputViewer", size=(MAX_DISPLAY, MAX_DISPLAY),
              background_color=sg.theme_background_color())],
]

# --- Panel Kanan: Output Image ---
image_output_column = [
    [sg.Text("Image Processing Output :", font=("Helvetica", 10, "bold"))],
    [sg.Text("", size=(50, 1), key="ImgProcessingType")],
    [sg.Image(key="ImgOutputViewer", size=(MAX_DISPLAY, MAX_DISPLAY),
              background_color=sg.theme_background_color())],
]

# --- Toolbar Processing (Menggunakan TabGroup untuk memisahkan fitur) ---
# Tab 1: Operasi Piksel & Kecerahan yang sudah ada
tab_basic_layout = [
    [
        sg.Button("Image Negative",  size=(14, 1), key="ImgNegative"),
        sg.Button("Image Grayscale", size=(14, 1), key="ImgGrayscale"),
        sg.Button("Logaritmik",      size=(12, 1), key="Log"),
        sg.Button("Blend Mode",      size=(12, 1), key="ModeBlend"),
        sg.VSeparator(),
        sg.Text("Brightness:"),
        sg.Slider(range=(-255, 255), orientation='h', size=(16, 14),
                  default_value=0, key="BrightVal", enable_events=True),
        sg.Button("Reset", size=(6, 1), key="Default"),
    ]
]

# Tab 2: Geometri yang sudah ada
tab_geometry_layout = [
    [
        sg.Button("Rotate 90° CW",  size=(13, 1), key="ImgRotate"),
        sg.Button("Rotate 90° CCW", size=(13, 1), key="ImgRotateCCW"),
        sg.Button("Rotate 180°",    size=(12, 1), key="ImgRotate180"),
        sg.Button("Flip Vertikal",  size=(12, 1), key="flipv"),
        sg.Button("Flip Horizontal",size=(14, 1), key="fliph"),
        sg.VSeparator(),
        sg.Text("Zoom Factor:"),
        sg.Combo([2, 3, 4], default_value=2, key="ZoomFact", size=(3, 1)),
        sg.Button("Zoom In",  key="BtnZoomIn",  size=(8, 1)),
        sg.Button("Zoom Out", key="BtnZoomOut", size=(9, 1)),
    ]
]

# Tab 3: Tab Baru untuk Linear & Spatial Filter (Memindahkan Mean/Median dan persiapan fitur baru)
tab_Non_linear_layout = [
    [
        sg.Text("Kernel Size:"),
        sg.Combo(["3x3", "5x5", "7x7"], default_value="3x3", key="KernelSize", size=(5, 1), readonly=True),
        sg.VSeparator(),
        sg.Button("Mean Filter", size=(12, 1), key="imgmean"),
        sg.Button("Median Filter", size=(12, 1), key="ImgMedian")
    ]
]

# Tab 4 Linear
tab_Linear_Layout = [
    [
        sg.Button("Sobel Filter", size=(12, 1), key="ImgSobel"),
        sg.Button("Robert Cross Filter", size=(16, 1), key="ImgRobertCross"),
        sg.Button("Gradient Filter", size=(12, 1), key="ImgGradient"),
        sg.Button("Prewitt Filter", size=(12, 1), key="ImgPrewitt"),
        sg.Button("Frei-Chen Filter", size=(12, 1), key="ImgFreiChen"),
        sg.Button("Gaussian Filter", size=(12, 1), key="ImgGaussian"),
        sg.Button("Laplacian of Gaussian Filter", size=(22, 1), key="ImgLoG"),
        sg.Button("Compass Filter", size=(12, 1), key="ImgCompass"),
        sg.Button("Canny", size=(12, 1), key="ImgCanny"),
        sg.Button("Emboss Filter", size=(12, 1), key="ImgEmboss")
    ]
]

# Tab 5 Morfologi
tab_Operasi_Morfologi_Layout = [
    [
        sg.Text("Ukuran Kernel Morfologi:", font=("Helvetica", 10)),
        sg.Combo(["3x3", "5x5", "7x7", "9x9", "11x11", "15x15", "21x21"], default_value="3x3", key="KernelSizeMorph", readonly=True, size=(6, 1)),
        sg.Text("Iterasi:"),
        sg.Combo([str(i) for i in range(1, 11)], default_value="1", key="MorphIterations", readonly=True, size=(4, 1))
    ],
    [sg.HorizontalSeparator()],
    [
        sg.Button("Erosion", size=(12, 1), key="ImgErosion",),
        sg.Button("Dilation", size=(12, 1), key="ImgDilation"),
        sg.Button("Opening", size=(12, 1), key="ImgOpening"),
        sg.Button("Closing", size=(12, 1), key="ImgClosing") 
    ]
]

# Satukan semua tab ke dalam Toolbar
toolbar = [
    [
        sg.TabGroup([
            [
                sg.Tab("Basic & Color", tab_basic_layout),
                sg.Tab("Geometry & Transform", tab_geometry_layout),
                sg.Tab("Non Linear", tab_Non_linear_layout, key="TabNonLinear"),
                sg.Tab("Linear", tab_Linear_Layout, key="TabLinear"),
                sg.Tab("Operasi Morfologi", tab_Operasi_Morfologi_Layout, key="TabMorfologi")
            ]
        ], expand_x=True, title_color="black", selected_title_color="#f9f9f9")
    ]
]

# --- Layout utama ---
layout = [
    # Toolbar di atas (Sekarang berisi TabGroup)
    [sg.Frame("List of Processing", toolbar, expand_x=True)],
    [sg.HSeparator()],
    # Konten utama: file panel | input image | output image
    [
        sg.Column(file_list_column,
                  vertical_alignment='top',
                  scrollable=False,
                  size=(230, 580)),
        sg.VSeperator(),
        sg.Column(image_input_column,
                  vertical_alignment='top',
                  expand_x=True,
                  expand_y=True,
                  scrollable=True,
                  size=(MAX_DISPLAY + 20, 580)),
        sg.VSeperator(),
        sg.Column(image_output_column,
                  vertical_alignment='top',
                  expand_x=True,
                  expand_y=True,
                  scrollable=True,
                  size=(MAX_DISPLAY + 20, 580)),
    ],
]

window = sg.Window(
    "Mini Image Editor",
    layout,
    resizable=True,
    finalize=True,
).finalize()

# ======================= STATE =======================
filename_out = "out.png"
img_original = None
img_input    = None
img_input2   = None
coldepth     = 24

# ======================= EVENT LOOP =======================
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # --- Folder dipilih ---
    if event == "ImgFolder":
        folder = values["ImgFolder"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [
            f for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".gif", ".jpg", ".jpeg"))
        ]
        window["ImgList"].update(fnames)
        window["ImgInputViewer"].update(filename='')
        window["ImgOutputViewer"].update(filename='')

    # --- Gambar dipilih dari list ---
    elif event == "ImgList":
        try:
            filename = os.path.join(values["ImgFolder"], values["ImgList"][0])
            img_original = Image.open(filename)
            img_input    = Image.open(filename)

            display_path = get_display_image_dynamic(img_input, MAX_DISPLAY, MAX_DISPLAY)
            window["FilepathImgInput"].update(filename)
            window["ImgProcessingType"].update(filename)
            window["ImgInputViewer"].update(filename=display_path)
            window["ImgOutputViewer"].update(filename=display_path)

            img_w, img_h = img_input.size
            window["ImgSize"].update(f"Image Size : {img_w} x {img_h}")
            mode_to_coldepth = {"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32}
            coldepth = mode_to_coldepth.get(img_input.mode, 24)
            window["ImgColorDepth"].update(f"Color Depth : {coldepth}")

            window["OutImgSize"].update(f"Size : {img_w} x {img_h}")
            window["OutImgColorDepth"].update(f"Color Depth : {coldepth} bit")
            window["OutImgProcess"].update("Process : Original Image")

        except Exception as e:
            print(f"Error load image: {e}")

    # --- ARITMATIKA ---
    elif event == "ImgNegative":
        if img_input:
            try:
                window["ImgProcessingType"].update("Image Negative")
                img_output = ImgNegative(img_input, coldepth)
                img_output.save(filename_out)
                window["ImgOutputViewer"].update(
                    filename=get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY))
                
                update_output_info(window, img_output, "Image Negative")
            except Exception as e:
                print(f"Error Negative: {e}")

    elif event == "ImgGrayscale":
        if img_input:
            try:
                window["ImgProcessingType"].update("Image Grayscale")
                img_output = ImgGrayscale(img_input, coldepth)
                img_output.save(filename_out)
                window["ImgOutputViewer"].update(
                    filename=get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY))
                
                update_output_info(window, img_output, "Image Grayscale")
            except Exception as e:
                print(f"Error Grayscale: {e}")

    elif event == "Log":
        if img_input:
            try:
                window["ImgProcessingType"].update("Logarithmic")
                img_output = log(img_input, coldepth)
                img_output.save(filename_out)
                window["ImgOutputViewer"].update(
                    filename=get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY))
                update_output_info(window, img_output, "Logarithmic")
            except Exception as e:
                print(f"Error Log: {e}")

    elif event == "BrightVal":
        if img_original:
            try:
                nilai = int(values["BrightVal"])
                window["ImgProcessingType"].update(f"Brightness ({nilai})")
                img_output = ImgBrightness(img_original, coldepth, nilai)
                img_output.save(filename_out)
                window["ImgOutputViewer"].update(
                    filename=get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY))
                update_output_info(window, img_output, f"Brightness ({nilai})")
            except Exception as e:
                print(f"Error Brightness: {e}")

    elif event == "ModeBlend":
        # Toggle visibilitas kolom blend
        is_visible = window["ColBlend"].visible
        window["ColBlend"].update(visible=not is_visible)

    elif event == "ImgSelect2":
        filename2 = sg.popup_get_file("Pilih Gambar Kedua", no_window=True)
        if filename2:
            img_input2 = Image.open(filename2)
            display_path2 = get_display_image(img_input2)
            window["ImgInputViewer2"].update(filename=display_path2)

    elif event == "BlendAlpha":
        try:
            # Pastikan img_input2 sudah ada
            img_output = ImgBlend(img_original, img_input2, values["BlendAlpha"])
            img_output.save(filename_out)
            display_out = get_display_image(img_output)
            window["ImgOutputViewer"].update(filename=display_out)
        except Exception as e:
            print(f"Pilih gambar kedua dulu: {e}")

    elif event in ("imgmean", "ImgMean"):
        if img_input:
            try:
                # Ambil ukuran kernel dari combo box (misal "5x5" -> diubah jadi integer 5)
                k_str = values["KernelSize"]
                k_size = int(k_str.split('x')[0])
                
                window["ImgProcessingType"].update(f"Mean Filter ({k_str})")
                
                # Jalankan filter dengan parameter k_size tambahan
                img_output = ImgMeanFilter(img_input, coldepth, k_size)
                
                img_output.save(filename_out)
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)

                update_output_info(window, img_output, f"Mean Filter ({k_str})")
                img_input = img_output
            except Exception as e:
                print(f"Error Mean Filter: {e}")

    elif event == "ImgMedian":
        if img_input:
            try:
                # Ambil ukuran kernel dari combo box (misal "7x7" -> diubah jadi integer 7)
                k_str = values["KernelSize"]
                k_size = int(k_str.split('x')[0])
                
                window["ImgProcessingType"].update(f"Median Filter ({k_str})")
                
                # Jalankan filter dengan parameter k_size tambahan
                img_output = ImgMedianFilter(img_input, coldepth, k_size)
                
                img_output.save(filename_out)
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)

                update_output_info(window, img_output, f"Median Filter ({k_str})")
                img_input = img_output
            except Exception as e:
                print(f"Error Median Filter: {e}")

    elif event == "ImgSobel":
        if img_input:
            try:
                window["ImgProcessingType"].update("Sobel Filter (Edge Detection)")
                
                # Menjalankan fungsi Sobel Filter yang baru dibuat
                img_output = ImgSobelFilter(img_input, coldepth)
                
                img_output.save(filename_out)
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)

                # Memperbarui panel informasi output di sebelah kiri
                update_output_info(window, img_output, "Sobel Filter")
                
                # Menyimpan state output ke input agar bisa diproses berantai jika mau
                img_input = img_output
            except Exception as e:
                print(f"Error Sobel Filter: {e}")

    elif event == "ImgRobertCross":
        if img_input:
            try:
                window["ImgProcessingType"].update("Robert Cross Filter (Edge Detection)")
                
                # Menjalankan fungsi Robert Cross Filter yang baru dibuat
                img_output = ImgRobertCrossFilter(img_input, coldepth)
                
                img_output.save(filename_out)
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)

                # Memperbarui panel informasi output di sebelah kiri
                update_output_info(window, img_output, "Robert Cross Filter")
                
                # Menyimpan state output ke input agar bisa diproses berantai jika mau
                img_input = img_output
            except Exception as e:
                print(f"Error Robert Cross Filter: {e}")

    elif event == "ImgGradient":
        if img_input:
            try:
                window["ImgProcessingType"].update("Gradient Filter (Edge Detection)")
                
                # Menjalankan fungsi Gradient Filter yang baru dibuat
                img_output = ImgGradientFilter(img_input, coldepth)
                
                img_output.save(filename_out)
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)

                # Memperbarui panel informasi output di sebelah kiri
                update_output_info(window, img_output, "Gradient Filter")
                
                # Menyimpan state output ke input agar bisa diproses berantai jika mau
                img_input = img_output
            except Exception as e:
                print(f"Error Gradient Filter: {e}")

    elif event == "ImgPrewitt":
        if img_input:
            try:
                window["ImgProcessingType"].update("Prewitt Filter (Edge Detection)")
                
                # Menjalankan fungsi Prewitt Filter yang baru dibuat
                img_output = ImgPrewittFilter(img_input, coldepth)
                
                img_output.save(filename_out)
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)

                # Memperbarui panel informasi output di sebelah kiri
                update_output_info(window, img_output, "Prewitt Filter")
                
                # Menyimpan state output ke input agar bisa diproses berantai jika mau
                img_input = img_output
            except Exception as e:
                print(f"Error Prewitt Filter: {e}")

    elif event == "ImgFreiChen":
        if img_input:
            try:
                window["ImgProcessingType"].update("Frei-Chen Filter (Orthogonal Edge Detection)")
                
                # Menjalankan fungsi Frei-Chen Filter yang baru dibuat
                img_output = ImgFreiChenFilter(img_input, coldepth)
                
                img_output.save(filename_out)
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)

                # Memperbarui panel informasi output di sebelah kiri
                update_output_info(window, img_output, "Frei-Chen Filter")
                
                # Menyimpan state output ke input agar bisa diproses berantai jika mau
                img_input = img_output
            except Exception as e:
                print(f"Error Frei-Chen Filter: {e}")

    elif event == "ImgGaussian":
        if img_input:
            try:
                window["ImgProcessingType"].update("Gaussian Filter (11x11 Smoothing)")
                
                # Menjalankan fungsi Gaussian Filter
                img_output = ImgGaussianFilter(img_input, coldepth)
                
                img_output.save(filename_out)
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)

                # Memperbarui panel informasi output di sebelah kiri
                update_output_info(window, img_output, "Gaussian Filter (11x11)")
                
                # Menyimpan state output ke input agar bisa diproses berantai
                img_input = img_output
            except Exception as e:
                print(f"Error Gaussian Filter: {e}")

    elif event == "ImgLoG":
        if img_input:
            try:
                window["ImgProcessingType"].update("Laplacian of Gaussian (LoG) Filter")
                
                # Menjalankan fungsi Laplacian of Gaussian Filter
                img_output = ImgLoGFilter(img_input, coldepth)
                
                img_output.save(filename_out)
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)

                # Memperbarui panel informasi output di sebelah kiri
                update_output_info(window, img_output, "LoG Filter")
                
                # Menyimpan state output ke input agar bisa diproses berantai
                img_input = img_output
            except Exception as e:
                print(f"Error LoG Filter: {e}")

    elif event == "ImgCompass":
        if img_input:
            try:
                window["ImgProcessingType"].update("Compass Filter (Kirsch Edge Detection)")
                
                # Menjalankan fungsi Compass Filter
                img_output = ImgCompassFilter(img_input, coldepth)
                
                img_output.save(filename_out)
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)

                # Memperbarui panel informasi output di sebelah kiri
                update_output_info(window, img_output, "Compass Filter")
                
                # Menyimpan state output ke input agar bisa diproses berantai
                img_input = img_output
            except Exception as e:
                print(f"Error Compass Filter: {e}")

    elif event == "ImgCanny":
        if img_input:
            try:
                window["ImgProcessingType"].update("Canny Edge Detection")
                
                # Menjalankan fungsi rangkaian algoritma Canny
                img_output = ImgCannyDetection(img_input, coldepth)
                
                img_output.save(filename_out)
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)

                # Memperbarui panel informasi output di sebelah kiri
                update_output_info(window, img_output, "Canny Edge")
                
                # Menyimpan state output ke input agar bisa diproses berantai
                img_input = img_output
            except Exception as e:
                print(f"Error Canny Detection: {e}")

    elif event == "ImgEmboss":
        if img_input:
            try:
                window["ImgProcessingType"].update("Emboss Filter (3D Carving Effect)")
                
                # Menjalankan fungsi Emboss Filter
                img_output = ImgEmbossFilter(img_input, coldepth)
                
                img_output.save(filename_out)
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)

                # Memperbarui panel informasi output di sebelah kiri
                update_output_info(window, img_output, "Emboss Filter")
                
                # Menyimpan state output ke input agar bisa diproses berantai
                img_input = img_output
            except Exception as e:
                print(f"Error Emboss Filter: {e}")

    elif event == "ImgErosion":
        if img_input:
            try:
                # Ambil ukuran kernel dari combo box yang ada di Tab Non Linear (key: "KernelSize")
                k_str = values["KernelSizeMorph"]
                k_size = int(k_str.split('x')[0]) # Mengonversi "3x3" -> integer 3
                
                window["ImgProcessingType"].update(f"Min Erosion ({k_str})")
                
                # Jalankan fungsi erosi
                img_output = ImgErosion(img_input, coldepth, k_size)
                img_output.save(filename_out)
                
                # Update visualisasi gambar di panel output
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)
                
                # Supaya skema berantai bisa bebas dilakukan, hasil output dijadikan input baru
                img_input = img_output 
                
                # Perbarui teks informasi detail output di panel sebelah kiri
                update_output_info(window, img_output, f"Min Erosion ({k_str})")
            except Exception as e:
                print(f"Error Erosion: {e}")

    elif event == "ImgDilation":
        if img_input:
            try:
                # Membaca ukuran kernel dari combo box Tab 5 (key: "KernelSizeMorph")
                k_str = values["KernelSizeMorph"]
                k_size = int(k_str.split('x')[0]) # Mengonversi "3x3" -> integer 3
                
                window["ImgProcessingType"].update(f"Max Dilation ({k_str})")
                
                # Jalankan fungsi dilatasi
                img_output = ImgDilation(img_input, coldepth, k_size)
                img_output.save(filename_out)
                
                # Update visualisasi gambar di panel output
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)
                
                # Supaya skema berantai bisa bebas dilakukan, hasil output dijadikan input baru
                img_input = img_output 
                
                # Perbarui teks informasi detail output di panel sebelah kiri
                update_output_info(window, img_output, f"Max Dilation ({k_str})")
            except Exception as e:
                print(f"Error Dilation: {e}")

    elif event == "ImgOpening":
        if img_input:
            try:
                k_str = values["KernelSizeMorph"]
                k_size = int(k_str.split('x')[0])
                iterations = int(values["MorphIterations"])
                
                window["ImgProcessingType"].update(f"Morphology Opening ({k_str} | Iterasi: {iterations})")
                
                # --- PROSES BERTAHAP (CHAINING STATE) ---
                # Menggunakan img_input langsung sebagai basis pengerjaan loop
                temp_img = img_input
                
                # Jalankan Erosi sebanyak N kali
                for _ in range(iterations):
                    temp_img = ImgErosion(temp_img, coldepth, k_size)
                
                # Jalankan Dilatasi sebanyak N kali dari hasil erosi terakhir
                for _ in range(iterations):
                    temp_img = ImgDilation(temp_img, coldepth, k_size)
                
                # Konversi hasil akhir ke biner jika tipe citra 1-bit
                if coldepth == 1:
                    img_output = temp_img.convert("1")
                else:
                    img_output = temp_img
                
                # Simpan hasil pemrosesan saat ini ke file output temporer
                img_output.save(filename_out)
                
                # Tampilkan ke GUI layar kanan
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)
                
                img_input = img_output.copy() 
                
                # Update teks informasi di GUI
                update_output_info(window, img_input, f"Opening ({k_str} | Iterasi: {iterations})")
                
            except Exception as e:
                print(f"Error Opening: {e}")

    elif event == "ImgClosing":
        if img_input:
            try:
                k_str = values["KernelSizeMorph"]
                k_size = int(k_str.split('x')[0])
                iterations = int(values["MorphIterations"])
                
                window["ImgProcessingType"].update(f"Morphology Closing ({k_str} | Iterasi: {iterations})")
                
                # --- PROSES BERTAHAP (CHAINING STATE) ---
                temp_img = img_input
                
                # Jalankan Dilatasi sebanyak N kali
                for _ in range(iterations):
                    temp_img = ImgDilation(temp_img, coldepth, k_size)
                
                # Jalankan Erosi sebanyak N kali dari hasil dilatasi terakhir
                for _ in range(iterations):
                    temp_img = ImgErosion(temp_img, coldepth, k_size)
                
                if coldepth == 1:
                    img_output = temp_img.convert("1")
                else:
                    img_output = temp_img
                
                img_output.save(filename_out)
                
                display_path = get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY)
                window["ImgOutputViewer"].update(filename='')
                window["ImgOutputViewer"].update(filename=display_path)
                
                img_input = img_output.copy()
                
                update_output_info(window, img_input, f"Closing ({k_str} | Iterasi: {iterations})")
                
            except Exception as e:
                print(f"Error Closing: {e}")

    # --- GEOMETRI ---
    elif event == "ImgRotate":
        if img_input:
            img_output = ImgRotate(img_input, coldepth, 90, "C")
            img_input = img_output
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(
                filename=get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY))

    elif event == "ImgRotateCCW":
        if img_input:
            img_output = ImgRotate(img_input, coldepth, -90, "CC")
            img_input = img_output
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(
                filename=get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY))

    elif event == "ImgRotate180":
        if img_input:
            img_output = ImgRotate(img_input, coldepth, 180, "180")
            img_input = img_output
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(
                filename=get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY))

    elif event == "fliph":
        if img_input:
            img_output = ImgFlip(img_input, coldepth, "H")
            img_input = img_output
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(
                filename=get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY))

    elif event == "flipv":
        if img_input:
            img_output = ImgFlip(img_input, coldepth, "V")
            img_input = img_output
            img_output.save(filename_out)
            window["ImgOutputViewer"].update(
                filename=get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY))

    # --- RESET ---
    elif event == "Default":
        if img_original:
            try:
                window["BrightVal"].update(0)
                window["BlendAlpha"].update(50)
                img_input = img_original.copy()
                window["ImgOutputViewer"].update(
                    filename=get_display_image_dynamic3(img_input, MAX_DISPLAY, MAX_DISPLAY))
                window["ImgProcessingType"].update("Reset to original")
            except Exception as e:
                print(f"Error Reset: {e}")

    # --- ZOOM ---
    elif event == "BtnZoomIn":
        if img_input:
            try:
                factor = int(values["ZoomFact"])
                img_output = ImgZoomIn(img_input, coldepth, factor)
                img_input = img_output
                window["ImgOutputViewer"].update(
                    filename=get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY))
                
                update_output_info(window, img_output, f"Zoom In (Factor: {factor}x)")
            except Exception as e:
                print(f"Error Zoom In: {e}")

    elif event == "BtnZoomOut":
        if img_input:
            try:
                factor = int(values["ZoomFact"])
                img_output = ImgZoomOut(img_input, coldepth, factor)
                img_input = img_output
                window["ImgOutputViewer"].update(
                    filename=get_display_image_dynamic3(img_output, MAX_DISPLAY, MAX_DISPLAY))
                
                update_output_info(window, img_output, f"Zoom Out (Factor: {factor}x)")
            except Exception as e:
                print(f"Error Zoom Out: {e}")

    elif event == "Default":
        if img_original:
            try:
                window["BrightVal"].update(0)
                window["BlendAlpha"].update(50)
                img_input = img_original.copy()
                window["ImgOutputViewer"].update(
                    filename=get_display_image_dynamic3(img_input, MAX_DISPLAY, MAX_DISPLAY))
                window["ImgProcessingType"].update("Reset to original")

                # UPDATE INFO OUTPUT
                update_output_info(window, img_input, "Reset to Original")
            except Exception as e:
                print(f"Error Reset: {e}")

window.close()