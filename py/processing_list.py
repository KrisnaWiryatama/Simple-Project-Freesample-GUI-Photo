from PIL import Image, ImageOps
from PIL import Image, ImageChops
import math

def get_display_image(img_pil, max_size=(390, 693)):
    if img_pil is None: return None
    img_temp = img_pil.copy()
    img_temp.thumbnail(max_size)
    temp_path = "temp_gui_preview.png"
    img_temp.save(temp_path)
    return temp_path

#aritmatika
def ImgNegative(img_input,coldepth):

    if coldepth!=24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB',(img_input.size[0],img_input.size[1]))
    pixels = img_output.load()
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            r, g, b = img_input.getpixel((i, j))
            pixels[i,j] = (255-r, 255-g, 255-b)

    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgGrayscale(img_input, coldepth):
    # Konversi ke RGB jika perlu untuk memproses pixel
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    # Buat kanvas baru dengan ukuran yang sama
    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    pixels = img_output.load()

    for i in range(img_input.size[0]):
        for j in range(img_input.size[1]):
            r, g, b = img_input.getpixel((i, j))

            gray = int((r + g + b) / 3)
            pixels[i, j] = (gray, gray, gray)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgBrightness(img_input, coldepth, nilai):
    # Pastikan dalam mode RGB untuk pemrosesan piksel
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    pixels = img_output.load()
    
    for i in range(img_input.size[0]):
        for j in range(img_input.size[1]):
            r, g, b = img_input.getpixel((i, j))
            
            new_r = int(r) + nilai
            new_g = int(g) + nilai
            new_b = int(b) + nilai

            if new_r > 255: new_r = 255
            if new_r < 0: new_r = 0
            
            if new_g > 255: new_g = 255
            if new_g < 0: new_g = 0
            
            if new_b > 255: new_b = 255
            if new_b < 0: new_b = 0
            
            pixels[i, j] = (new_r, new_g, new_b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    
    return img_output

def log(img_input, coldepth):
    # Pastikan dalam mode RGB untuk pemrosesan piksel
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    pixels = img_output.load()

    c = 255 / math.log(1 + 255) 
    
    for i in range(img_input.size[0]):
        for j in range(img_input.size[1]):
            r, g, b = img_input.getpixel((i, j))
            
            new_r = int(c * math.log(1 + r))
            new_g = int(c * math.log(1 + g))
            new_b = int(c * math.log(1 + b))
            
            pixels[i, j] = (new_r, new_g, new_b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")
    
    return img_output

def ImgBlend(img1, img2, alpha_value):
    # Alpha_value dari slider (0-100) diubah menjadi rentang 0.0 - 1.0 (C)
    c = alpha_value / 100.0
    
    # Pastikan kedua gambar dalam mode RGB
    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')
    
    # Resize gambar kedua agar sama dengan gambar pertama
    if img1.size != img2.size:
        img2 = img2.resize(img1.size)
        
    img_output = Image.new('RGB', (img1.size[0], img1.size[1]))
    pixels = img_output.load()
    
    for i in range(img1.size[0]):
        for j in range(img1.size[1]):
            r1, g1, b1 = img1.getpixel((i, j)) # Gambar A
            r2, g2, b2 = img2.getpixel((i, j)) # Gambar B
            
            # Rumus: Pnew = C*A + (1-C)*B
            new_r = int(c * r1 + (1 - c) * r2)
            new_g = int(c * g1 + (1 - c) * g2)
            new_b = int(c * b1 + (1 - c) * b2)
            
            # Clipping if Pnew > 255
            if new_r > 255: new_r = 255
            if new_g > 255: new_g = 255
            if new_b > 255: new_b = 255
            
            pixels[i, j] = (new_r, new_g, new_b)
            
    return img_output

#geometri
def ImgRotate(img_input,coldepth,deg,direction):
    
    if coldepth!=24:
        img_input = img_input.convert('RGB')
    
    if direction == "180":
        img_output = Image.new('RGB', (img_input.size[0], img_input.size[1]))
    else: # Untuk 90 CW atau 90 CCW
        img_output = Image.new('RGB', (img_input.size[1], img_input.size[0]))

    
    pixels = img_output.load()
    width_in, height_in = img_input.size
    
    for i in range(img_output.size[0]):
        for j in range(img_output.size[1]):
            if direction == "C": # 90 Degree CW
                r, g, b = img_input.getpixel((j, height_in - 1 - i))
            elif direction == "CC": # 90 Degree CCW
                r, g, b = img_input.getpixel((width_in - 1 - j, i))
            elif direction == "180": # 180 Degree
                r, g, b = img_input.getpixel((width_in - 1 - i, height_in - 1 - j))
            pixels[i,j] = (r, g, b)

    if coldepth==1:
        img_output = img_output.convert("1")
    elif coldepth==8:
        img_output = img_output.convert("L")
    else:
        img_output = img_output.convert("RGB")

    return img_output

def ImgFlip(img_input, coldepth, mode):
    # Pastikan dalam mode RGB untuk pemrosesan piksel
    if coldepth != 24:
        img_input = img_input.convert('RGB')

    # Dimensi tetap sama, tidak berubah seperti rotasi
    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels = img_output.load()
    
    for i in range(width):
        for j in range(height):
            if mode == "H":
                r, g, b = img_input.getpixel((i, height - 1 - j))
            elif mode == "V":
                r, g, b = img_input.getpixel((width - 1 - i, j))
            
            pixels[i, j] = (r, g, b)

    # Kembalikan ke Color Depth asli sesuai variabel coldepth yang kamu miliki
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    
    return img_output

# ==================== SCALING ====================
def ImgZoomIn(img_input, coldepth, factor):
    """
    Zoom in dengan kualitas tinggi menggunakan BICUBIC interpolation.
    factor: integer atau float > 1 (misal 2, 2.5, 3, 4)
    """
    if factor <= 1:
        return img_input
    if coldepth >= 24 and img_input.mode not in ('RGB', 'RGBA'):
        img_temp = img_input.convert('RGB')
    else:
        img_temp = img_input
    
    new_size = (int(img_temp.width * factor), int(img_temp.height * factor))
    img_output = img_temp.resize(new_size, Image.BICUBIC)
    
    # Kembalikan ke color depth asli
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    elif coldepth == 24:
        img_output = img_output.convert("RGB")
    elif coldepth == 32:
        img_output = img_output.convert("RGBA")
    return img_output

def ImgZoomOut(img_input, coldepth, factor):
    """
    Zoom out dengan kualitas tinggi menggunakan LANCZOS anti-aliasing.
    factor: integer atau float > 1 (misal 2, 3, 4) -> ukuran menjadi 1/factor
    """
    if factor <= 1:
        return img_input
    
    # Sama seperti zoom in, konversi sementara jika diperlukan
    if coldepth >= 24 and img_input.mode not in ('RGB', 'RGBA'):
        img_temp = img_input.convert('RGB')
    else:
        img_temp = img_input
    
    new_size = (int(img_temp.width / factor), int(img_temp.height / factor))
    # LANCZOS adalah filter anti-aliasing terbaik untuk downsampling
    img_output = img_temp.resize(new_size, Image.LANCZOS)
    
    # Kembalikan ke color depth asli
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    elif coldepth == 24:
        img_output = img_output.convert("RGB")
    elif coldepth == 32:
        img_output = img_output.convert("RGBA")
    return img_output

def ImgMeanFilter(img_input, coldepth, k_size=3):
    if img_input.mode != 'RGB':
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels_in = img_input.load()
    pixels_out = img_output.load()

    # STEP 1: Salin dulu semua piksel asli ke output (termasuk area tepi)
    for i in range(width):
        for j in range(height):
            pixels_out[i, j] = pixels_in[i, j]

    # Hitung offset jangkauan berdasarkan ukuran kernel (misal 5x5 -> offset = 2)
    offset = k_size // 2
    total_pixel_kernel = k_size * k_size

    # STEP 2: Proses filter dengan batas range yang dinamis berdasarkan offset kernel
    for i in range(offset, width - offset):
        for j in range(offset, height - offset):
            sum_r, sum_g, sum_b = 0, 0, 0
            
            # Looping pergerakan matriks kernel secara dinamis
            for k in range(-offset, offset + 1):
                for l in range(-offset, offset + 1):
                    r, g, b = pixels_in[i + k, j + l]
                    sum_r += r
                    sum_g += g
                    sum_b += b
            
            # Pembagi disesuaikan dengan jumlah total piksel di dalam kernel (9, 25, atau 49)
            pixels_out[i, j] = (
                int(sum_r / total_pixel_kernel), 
                int(sum_g / total_pixel_kernel), 
                int(sum_b / total_pixel_kernel)
            )

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    
    return img_output


def ImgMedianFilter(img_input, coldepth, k_size=3):
    if img_input.mode != 'RGB':
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels_in = img_input.load()
    pixels_out = img_output.load()

    # STEP 1: Salin semua piksel asli ke output
    for i in range(width):
        for j in range(height):
            pixels_out[i, j] = pixels_in[i, j]

    # Hitung offset jangkauan berdasarkan ukuran kernel
    offset = k_size // 2
    # Indeks tengah untuk mencari median (misal kernel 5x5 ada 25 elemen -> indeks tengah = 12)
    median_index = (k_size * k_size) // 2

    # STEP 2: Proses filter dengan batas range dinamis
    for i in range(offset, width - offset):
        for j in range(offset, height - offset):
            list_r, list_g, list_b = [], [], []
            
            # Kumpulkan nilai piksel sesuai ukuran kernel
            for k in range(-offset, offset + 1):
                for l in range(-offset, offset + 1):
                    r, g, b = pixels_in[i + k, j + l]
                    list_r.append(r)
                    list_g.append(g)
                    list_b.append(b)
            
            # Urutkan nilai array piksel
            list_r.sort()
            list_g.sort()
            list_b.sort()
            
            # Ambil nilai median secara dinamis berdasarkan nilai median_index
            pixels_out[i, j] = (list_r[median_index], list_g[median_index], list_b[median_index])

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    
    return img_output

def ImgSobelFilter(img_input, coldepth):
    # Pastikan dalam mode RGB untuk manipulasi piksel channel
    if img_input.mode != 'RGB':
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels_in = img_input.load()
    pixels_out = img_output.load()

    # Matriks Kernel Sobel
    # Kiri ke kanan (Gx) dan Atas ke bawah (Gy)
    Gx = [
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ]
    
    Gy = [
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ]

    # Salin area tepi agar tidak kosong/hitam total jika diinginkan,
    # atau biarkan hitam secara default untuk hasil deteksi tepi yang bersih.
    for i in range(width):
        for j in range(height):
            pixels_out[i, j] = (0, 0, 0)

    # Offset kernel 3x3 adalah 1
    offset = 1

    # Proses konvolusi Sobel manual
    for i in range(offset, width - offset):
        for j in range(offset, height - offset):
            
            # Variabel penampung hasil perkalian matriks per channel
            val_gx_r, val_gx_g, val_gx_b = 0, 0, 0
            val_gy_r, val_gy_g, val_gy_b = 0, 0, 0
            
            # Looping matriks kernel 3x3
            for k in range(-offset, offset + 1):
                for l in range(-offset, offset + 1):
                    r, g, b = pixels_in[i + k, j + l]
                    
                    # Ambil bobot dari kernel (indeks disesuaikan dari -1..1 ke 0..2)
                    weight_x = Gx[k + offset][l + offset]
                    weight_y = Gy[k + offset][l + offset]
                    
                    # Akumulasi nilai rumpun Gx
                    val_gx_r += r * weight_x
                    val_gx_g += g * weight_x
                    val_gx_b += b * weight_x
                    
                    # Akumulasi nilai rumpun Gy
                    val_gy_r += r * weight_y
                    val_gy_g += g * weight_y
                    val_gy_b += b * weight_y
            
            # Hitung magnitudo gradien: sqrt(Gx^2 + Gy^2)
            magnitude_r = int(math.sqrt(val_gx_r**2 + val_gy_r**2))
            magnitude_g = int(math.sqrt(val_gx_g**2 + val_gy_g**2))
            magnitude_b = int(math.sqrt(val_gx_b**2 + val_gy_b**2))
            
            # Lakukan clipping agar nilai pixel tetap berada di rentang 0 - 255
            if magnitude_r > 255: magnitude_r = 255
            if magnitude_g > 255: magnitude_g = 255
            if magnitude_b > 255: magnitude_b = 255
            
            # Masukkan hasil ke piksel output
            pixels_out[i, j] = (magnitude_r, magnitude_g, magnitude_b)

    # Kembalikan ke Color Depth asli sesuai variabel input Anda
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    
    return img_output

def ImgRobertCrossFilter(img_input, coldepth):
    if img_input.mode != 'RGB':
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels_in = img_input.load()
    pixels_out = img_output.load()

    # Inisialisasi awal kanvas dengan warna hitam total
    for i in range(width):
        for j in range(height):
            pixels_out[i, j] = (0, 0, 0)

    # Karena kernel berukuran 2x2, kita memproses dari indeks 0 hingga N-1 
    # agar saat mengambil piksel tetangga (i+1 atau j+1) tidak terjadi IndexError
    for i in range(width - 1):
        for j in range(height - 1):
            
            # Mengambil piksel tetangga sesuai matriks menyilang 2x2
            r_curr, g_curr, b_curr = pixels_in[i, j]          # posisi (i, j)
            r_diag, g_diag, b_diag = pixels_in[i + 1, j + 1]  # posisi (i+1, j+1)
            r_nextx, g_nextx, b_nextx = pixels_in[i + 1, j]    # posisi (i+1, j)
            r_nexty, g_nexty, b_nexty = pixels_in[i, j + 1]    # posisi (i, j+1)

            # Hitung Gradien Gx (Diagonal Utama: [1, 0], [0, -1])
            val_gx_r = r_curr - r_diag
            val_gx_g = g_curr - g_diag
            val_gx_b = b_curr - b_diag

            # Hitung Gradien Gy (Diagonal Sekunder: [0, 1], [-1, 0])
            val_gy_r = r_nexty - r_nextx
            val_gy_g = g_nexty - g_nextx
            val_gy_b = b_nexty - b_nextx

            # Hitung Magnitudo Gradien: sqrt(Gx^2 + Gy^2)
            magnitude_r = int(math.sqrt(val_gx_r**2 + val_gy_r**2))
            magnitude_g = int(math.sqrt(val_gx_g**2 + val_gy_g**2))
            magnitude_b = int(math.sqrt(val_gx_b**2 + val_gy_b**2))

            # Lakukan clipping agar nilai piksel tetap berada di rentang 0 - 255
            if magnitude_r > 255: magnitude_r = 255
            if magnitude_g > 255: magnitude_g = 255
            if magnitude_b > 255: magnitude_b = 255

            # Masukkan hasil deteksi tepi ke piksel output
            pixels_out[i, j] = (magnitude_r, magnitude_g, magnitude_b)

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")

    return img_output

def ImgGradientFilter(img_input, coldepth):
    if img_input.mode != 'RGB':
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels_in = img_input.load()
    pixels_out = img_output.load()

    # Inisialisasi awal kanvas dengan warna hitam total
    for i in range(width):
        for j in range(height):
            pixels_out[i, j] = (0, 0, 0)

    # Memproses dari indeks 0 hingga N-1 agar piksel tetangga (i+1 atau j+1) tidak IndexError
    for i in range(width - 1):
        for j in range(height - 1):
            
            # Piksel saat ini, piksel kanan (X+1), dan piksel bawah (Y+1)
            r_curr, g_curr, b_curr = pixels_in[i, j]
            r_right, g_right, b_right = pixels_in[i + 1, j]
            r_down, g_down, b_down = pixels_in[i, j + 1]

            # Gradien Gx (Kanan - Saat ini)
            val_gx_r = r_right - r_curr
            val_gx_g = g_right - g_curr
            val_gx_b = b_right - b_curr

            # Gradien Gy (Bawah - Saat ini)
            val_gy_r = r_down - r_curr
            val_gy_g = g_down - g_curr
            val_gy_b = b_down - b_curr

            # Hitung Magnitudo Gradien: sqrt(Gx^2 + Gy^2)
            magnitude_r = int(math.sqrt(val_gx_r**2 + val_gy_r**2))
            magnitude_g = int(math.sqrt(val_gx_g**2 + val_gy_g**2))
            magnitude_b = int(math.sqrt(val_gx_b**2 + val_gy_b**2))

            # Clipping agar nilai piksel tetap berada di rentang 0 - 255
            if magnitude_r > 255: magnitude_r = 255
            if magnitude_g > 255: magnitude_g = 255
            if magnitude_b > 255: magnitude_b = 255

            # Masukkan hasil ke piksel output
            pixels_out[i, j] = (magnitude_r, magnitude_g, magnitude_b)

    # Kembalikan ke Color Depth asli
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")

    return img_output

def ImgPrewittFilter(img_input, coldepth):
    # Pastikan dalam mode RGB untuk manipulasi piksel channel
    if img_input.mode != 'RGB':
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels_in = img_input.load()
    pixels_out = img_output.load()

    # Matriks Kernel Prewitt (Bobot seragam -1 dan 1)
    Gx = [
        [-1, 0, 1],
        [-1, 0, 1],
        [-1, 0, 1]
    ]
    
    Gy = [
        [-1, -1, -1],
        [ 0,  0,  0],
        [ 1,  1,  1]
    ]

    # Inisialisasi awal kanvas dengan warna hitam total
    for i in range(width):
        for j in range(height):
            pixels_out[i, j] = (0, 0, 0)

    # Offset kernel 3x3 adalah 1
    offset = 1

    # Proses konvolusi Prewitt manual
    for i in range(offset, width - offset):
        for j in range(offset, height - offset):
            
            # Variabel penampung hasil perkalian matriks per channel
            val_gx_r, val_gx_g, val_gx_b = 0, 0, 0
            val_gy_r, val_gy_g, val_gy_b = 0, 0, 0
            
            # Looping matriks kernel 3x3
            for k in range(-offset, offset + 1):
                for l in range(-offset, offset + 1):
                    r, g, b = pixels_in[i + k, j + l]
                    
                    # Ambil bobot dari kernel Prewitt
                    weight_x = Gx[k + offset][l + offset]
                    weight_y = Gy[k + offset][l + offset]
                    
                    # Akumulasi nilai Gx
                    val_gx_r += r * weight_x
                    val_gx_g += g * weight_x
                    val_gx_b += b * weight_x
                    
                    # Akumulasi nilai Gy
                    val_gy_r += r * weight_y
                    val_gy_g += g * weight_y
                    val_gy_b += b * weight_y
            
            # Hitung magnitudo gradien: sqrt(Gx^2 + Gy^2)
            magnitude_r = int(math.sqrt(val_gx_r**2 + val_gy_r**2))
            magnitude_g = int(math.sqrt(val_gx_g**2 + val_gy_g**2))
            magnitude_b = int(math.sqrt(val_gx_b**2 + val_gy_b**2))
            
            # Lakukan clipping agar nilai pixel tetap berada di rentang 0 - 255
            if magnitude_r > 255: magnitude_r = 255
            if magnitude_g > 255: magnitude_g = 255
            if magnitude_b > 255: magnitude_b = 255
            
            # Masukkan hasil ke piksel output
            pixels_out[i, j] = (magnitude_r, magnitude_g, magnitude_b)

    # Kembalikan ke Color Depth asli
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    
    return img_output

def ImgFreiChenFilter(img_input, coldepth):
    if img_input.mode != 'RGB':
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels_in = img_input.load()
    pixels_out = img_output.load()

    # Konstanta sqrt(2) untuk mempermudah penulisan matriks basis Frei-Chen
    s2 = math.sqrt(2)

    # 4 Kernel Pertama Basis Tepi Frei-Chen (Tanpa konstanta depan)
    f1 = [
        [1,  0, -1],
        [s2, 0, -s2],
        [1,  0, -1]
    ]
    
    f2 = [
        [ 1,  s2,  1],
        [ 0,   0,  0],
        [-1, -s2, -1]
    ]
    
    f3 = [
        [  0, -1, s2],
        [  1,  0, -1],
        [-s2,  1,  0]
    ]
    
    f4 = [
        [ s2, -1,  0],
        [ -1,  0,  1],
        [  0,  1, -s2]
    ]

    # Inisialisasi awal kanvas dengan warna hitam total
    for i in range(width):
        for j in range(height):
            pixels_out[i, j] = (0, 0, 0)

    offset = 1

    # Proses konvolusi manual
    for i in range(offset, width - offset):
        for j in range(offset, height - offset):
            
            # Variabel penampung hasil akumulasi perkalian per channel untuk f1 s/d f4
            # Channel Red
            g1_r, g2_r, g3_r, g4_r = 0, 0, 0, 0
            # Channel Green
            g1_g, g2_g, g3_g, g4_g = 0, 0, 0, 0
            # Channel Blue
            g1_b, g2_b, g3_b, g4_b = 0, 0, 0, 0
            
            for k in range(-offset, offset + 1):
                for l in range(-offset, offset + 1):
                    r, g, b = pixels_in[i + k, j + l]
                    
                    w1 = f1[k + offset][l + offset]
                    w2 = f2[k + offset][l + offset]
                    w3 = f3[k + offset][l + offset]
                    w4 = f4[k + offset][l + offset]
                    
                    # Akumulasi proyeksi ke masing-masing basis
                    g1_r += r * w1; g2_r += r * w2; g3_r += r * w3; g4_r += r * w4
                    g1_g += g * w1; g2_g += g * w2; g3_g += g * w3; g4_g += g * w4
                    g1_b += b * w1; g2_b += b * w2; g3_b += b * w3; g4_b += b * w4
            
            # Hitung magnitudo total: sqrt(G1^2 + G2^2 + G3^2 + G4^2)
            mag_r = math.sqrt(g1_r**2 + g2_r**2 + g3_r**2 + g4_r**2)
            mag_g = math.sqrt(g1_g**2 + g2_g**2 + g3_g**2 + g4_g**2)
            mag_b = math.sqrt(g1_b**2 + g2_b**2 + g3_b**2 + g4_b**2)
            
            # Kalikan dengan konstanta normalisasi luar: 1 / (2 * sqrt(2))
            c_norm = 1.0 / (2.0 * math.sqrt(2))
            magnitude_r = int(mag_r * c_norm)
            magnitude_g = int(mag_g * c_norm)
            magnitude_b = int(mag_b * c_norm)
            
            # Clipping rentang 0 - 255
            if magnitude_r > 255: magnitude_r = 255
            if magnitude_g > 255: magnitude_g = 255
            if magnitude_b > 255: magnitude_b = 255
            
            pixels_out[i, j] = (magnitude_r, magnitude_g, magnitude_b)

    # Kembalikan ke Color Depth asli
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    
    return img_output

def ImgGaussianFilter(img_input, coldepth):
    if img_input.mode != 'RGB':
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels_in = img_input.load()
    pixels_out = img_output.load()

    # Salin piksel asli ke output untuk penanganan area tepi bingkai
    for i in range(width):
        for j in range(height):
            pixels_out[i, j] = pixels_in[i, j]

    # 1. BANGKITKAN KERNEL GAUSSIAN 11x11 SECARA DINAMIS
    k_size = 11
    offset = k_size // 2  # Nilainya adalah 5 (jangkauan dari -5 sampai 5)
    sigma = 2.0          # Nilai standar deviasi untuk mengatur kekuatan blur
    
    kernel = [[0.0 for _ in range(k_size)] for _ in range(k_size)]
    kernel_sum = 0.0

    # Hitung bobot tiap posisi berdasarkan rumus Distribusi Gauss 2D
    for x in range(-offset, offset + 1):
        for y in range(-offset, offset + 1):
            exponent = -(x**2 + y**2) / (2 * (sigma**2))
            weight = math.exp(exponent) / (2 * math.pi * (sigma**2))
            kernel[x + offset][y + offset] = weight
            kernel_sum += weight

    # Normalisasi kernel agar total jumlah bobot matriks sama dengan 1.0
    for x in range(k_size):
        for y in range(k_size):
            kernel[x][y] /= kernel_sum

    # 2. PROSES KONVOLUSI GAUSSIAN MANUAL
    for i in range(offset, width - offset):
        for j in range(offset, height - offset):
            sum_r, sum_g, sum_b = 0.0, 0.0, 0.0
            
            # Looping pergerakan kernel 11x11
            for k in range(-offset, offset + 1):
                for l in range(-offset, offset + 1):
                    r, g, b = pixels_in[i + k, j + l]
                    weight = kernel[k + offset][l + offset]
                    
                    sum_r += r * weight
                    sum_g += g * weight
                    sum_b += b * weight
            
            # Konversi hasil akumulasi float ke integer
            pixels_out[i, j] = (int(sum_r), int(sum_g), int(sum_b))

    # Kembalikan ke Color Depth asli
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    
    return img_output

def ImgLoGFilter(img_input, coldepth):
    if img_input.mode != 'RGB':
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels_in = img_input.load()
    pixels_out = img_output.load()

    # Inisialisasi awal kanvas dengan warna hitam total
    for i in range(width):
        for j in range(height):
            pixels_out[i, j] = (0, 0, 0)

    # 1. BANGKITKAN KERNEL LAPLACIAN OF GAUSSIAN (LoG) SECARA DINAMIS
    k_size = 9            # Ukuran kernel 9x9 sangat ideal untuk LoG
    offset = k_size // 2  # Nilainya adalah 4 (jangkauan dari -4 sampai 4)
    sigma = 1.4           # Nilai sigma standar untuk deteksi tepi LoG yang optimal
    
    kernel = [[0.0 for _ in range(k_size)] for _ in range(k_size)]
    
    # Hitung nilai tiap sel berdasarkan rumus Mexican Hat (LoG)
    for x in range(-offset, offset + 1):
        for y in range(-offset, offset + 1):
            r_sq = x**2 + y**2
            sigma_sq = sigma**2
            
            # Komponen rumus LoG
            term1 = -1.0 / (math.pi * (sigma_sq**2))
            term2 = 1.0 - (r_sq / (2.0 * sigma_sq))
            term3 = math.exp(-r_sq / (2.0 * sigma_sq))
            
            kernel[x + offset][y + offset] = term1 * term2 * term3

    # 2. PROSES KONVOLUSI MANUAL
    for i in range(offset, width - offset):
        for j in range(offset, height - offset):
            sum_r, sum_g, sum_b = 0.0, 0.0, 0.0
            
            # Pergerakan kernel berkeliling memproses piksel tetangga
            for k in range(-offset, offset + 1):
                for l in range(-offset, offset + 1):
                    r, g, b = pixels_in[i + k, j + l]
                    weight = kernel[k + offset][l + offset]
                    
                    sum_r += r * weight
                    sum_g += g * weight
                    sum_b += b * weight
            
            # Karena turunan kedua menghasilkan nilai bermuatan negatif dan positif,
            # kita ambil nilai mutlaknya (absolute) agar tepian terlihat putih di atas latar hitam
            magnitude_r = int(abs(sum_r))
            magnitude_g = int(abs(sum_g))
            magnitude_b = int(abs(sum_b))
            
            # Lakukan peningkatan kontras (scaling factor) jika hasil dirasa terlalu redup
            scaling = 4
            magnitude_r *= scaling
            magnitude_g *= scaling
            magnitude_b *= scaling

            # Clipping rentang warna 0 - 255
            if magnitude_r > 255: magnitude_r = 255
            if magnitude_g > 255: magnitude_g = 255
            if magnitude_b > 255: magnitude_b = 255
            
            pixels_out[i, j] = (magnitude_r, magnitude_g, magnitude_b)

    # Kembalikan ke Color Depth asli
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    
    return img_output

def ImgCompassFilter(img_input, coldepth):
    if img_input.mode != 'RGB':
        img_input = img_input.convert('RGB')

    width, height = img_input.size
    img_output = Image.new('RGB', (width, height))
    pixels_in = img_input.load()
    pixels_out = img_output.load()

    # Inisialisasi awal kanvas dengan warna hitam total
    for i in range(width):
        for j in range(height):
            pixels_out[i, j] = (0, 0, 0)

    # Definisikan 8 Kernel Arah Mata Angin (Kirsch Compass Masks)
    kernels = {
        'N':  [[ 5,  5,  5], [-3,  0, -3], [-3, -3, -3]],
        'NE': [[-3,  5,  5], [-3,  0,  5], [-3, -3, -3]],
        'E':  [[-3, -3,  5], [-3,  0,  5], [-3, -3,  5]],
        'SE': [[-3, -3, -3], [-3,  0,  5], [-3,  5,  5]],
        'S':  [[-3, -3, -3], [-3,  0, -3], [ 5,  5,  5]],
        'SW': [[-3, -3, -3], [ 5,  0, -3], [ 5,  5, -3]],
        'W':  [[ 5, -3, -3], [ 5,  0, -3], [ 5, -3, -3]],
        'NW': [[ 5,  5, -3], [ 5,  0, -3], [-3, -3, -3]]
    }

    offset = 1

    # Proses konvolusi manual
    for i in range(offset, width - offset):
        for j in range(offset, height - offset):
            
            # Variabel untuk mencatat nilai respons maksimum untuk tiap channel
            max_r, max_g, max_b = 0, 0, 0
            
            # Lakukan perulangan untuk kedelapan jenis kernel mata angin
            for name, kernel in kernels.items():
                sum_r, sum_g, sum_b = 0, 0, 0
                
                # Konvolusi 3x3 untuk kernel saat ini
                for k in range(-offset, offset + 1):
                    for l in range(-offset, offset + 1):
                        r, g, b = pixels_in[i + k, j + l]
                        weight = kernel[k + offset][l + offset]
                        
                        sum_r += r * weight
                        sum_g += g * weight
                        sum_b += b * weight
                
                # Cari nilai mutlak respons konvolusi arah ini
                sum_r = abs(sum_r)
                sum_g = abs(sum_g)
                sum_b = abs(sum_b)
                
                # Ambil nilai tertinggi (maksimum) di antara arah mata angin
                if sum_r > max_r: max_r = sum_r
                if sum_g > max_g: max_g = sum_g
                if sum_b > max_b: max_b = sum_b
            
            # Clipping rentang warna 0 - 255
            magnitude_r = int(max_r)
            magnitude_g = int(max_g)
            magnitude_b = int(max_b)
            
            if magnitude_r > 255: magnitude_r = 255
            if magnitude_g > 255: magnitude_g = 255
            if magnitude_b > 255: magnitude_b = 255
            
            pixels_out[i, j] = (magnitude_r, magnitude_g, magnitude_b)

    # Kembalikan ke Color Depth asli
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
    
    return img_output

def ImgCannyDetection(img_input, coldepth):
    # 0. Konversi awal ke RGB dan Grayscale manual untuk mempermudah perhitungan gradien
    if img_input.mode != 'RGB':
        img_input = img_input.convert('RGB')
        
    width, height = img_input.size
    pixels_in = img_input.load()
    
    # Buat array 2D untuk menyimpan nilai keabuan (grayscale)
    gray = [[0.0 for _ in range(height)] for _ in range(width)]
    for i in range(width):
        for j in range(height):
            r, g, b = pixels_in[i, j]
            gray[i][j] = 0.299 * r + 0.587 * g + 0.114 * b

    # TAHAP 1: GAUSSIAN BLUR (Kernel 5x5) untuk mereduksi noise
    # Nilai kernel Gaussian 5x5 standar hasil rumus Gauss
    gaussian_kernel = [
        [2/159,  4/159,  5/159,  4/159, 2/159],
        [4/159,  9/159, 12/159,  9/159, 4/159],
        [5/159, 12/159, 15/159, 12/159, 5/159],
        [4/159,  9/159, 12/159,  9/159, 4/159],
        [2/159,  4/159,  5/159,  4/159, 2/159]
    ]
    
    blurred = [[0.0 for _ in range(height)] for _ in range(width)]
    for i in range(2, width - 2):
        for j in range(2, height - 2):
            sum_val = 0.0
            for k in range(-2, 3):
                for l in range(-2, 3):
                    sum_val += gray[i + k][j + l] * gaussian_kernel[k + 2][l + 2]
            blurred[i][j] = sum_val

    # TAHAP 2: HITUNG GRADIENT MAGNITUDE DAN ARANGYA (SOBEL OPERATOR)
    gx_kernel = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    gy_kernel = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    
    magnitude = [[0.0 for _ in range(height)] for _ in range(width)]
    angle = [[0.0 for _ in range(height)] for _ in range(width)]
    
    for i in range(1, width - 1):
        for j in range(1, height - 1):
            val_gx = 0.0
            val_gy = 0.0
            for k in range(-1, 2):
                for l in range(-1, 2):
                    val_gx += blurred[i + k][j + l] * gx_kernel[k + 1][l + 1]
                    val_gy += blurred[i + k][j + l] * gy_kernel[k + 1][l + 1]
            
            magnitude[i][j] = math.sqrt(val_gx**2 + val_gy**2)
            # Hitung sudut radian lalu ubah ke derajat (0 s/d 180)
            deg = math.degrees(math.atan2(val_gy, val_gx))
            if deg < 0:
                deg += 180
            angle[i][j] = deg

    # TAHAP 3: NON-MAXIMUM SUPPRESSION (NMS) - Penipisan Garis Tepi
    nms = [[0.0 for _ in range(height)] for _ in range(width)]
    for i in range(1, width - 1):
        for j in range(1, height - 1):
            q = 255.0
            r = 255.0
            
            # Bulatkan sudut ke 4 arah utama (0, 45, 90, 135 derajat)
            ang = angle[i][j]
            if (0 <= ang < 22.5) or (157.5 <= ang <= 180):
                q = magnitude[i][j + 1]
                r = magnitude[i][j - 1]
            elif (22.5 <= ang < 67.5):
                q = magnitude[i + 1][j - 1]
                r = magnitude[i - 1][j + 1]
            elif (67.5 <= ang < 112.5):
                q = magnitude[i + 1][j]
                r = magnitude[i - 1][j]
            elif (112.5 <= ang < 157.5):
                q = magnitude[i - 1][j - 1]
                r = magnitude[i + 1][j + 1]
                
            # Hanya simpan nilai jika ia adalah yang terbesar di arah tersebut
            if magnitude[i][j] >= q and magnitude[i][j] >= r:
                nms[i][j] = magnitude[i][j]
            else:
                nms[i][j] = 0.0

    # TAHAP 4: DOUBLE THRESHOLDING
    # Menentukan batas ambang atas dan bawah secara proporsional
    high_threshold = 50.0
    low_threshold = 20.0
    
    # Nilai representasi intensitas warna konstan
    strong_pixel = 255
    weak_pixel = 75
    
    res = [[0 for _ in range(height)] for _ in range(width)]
    for i in range(width):
        for j in range(height):
            if nms[i][j] >= high_threshold:
                res[i][j] = strong_pixel
            elif nms[i][j] >= low_threshold:
                res[i][j] = weak_pixel
            else:
                res[i][j] = 0

    # TAHAP 5: EDGE TRACKING BY HYSTERESIS
    img_output = Image.new('RGB', (width, height))
    pixels_out = img_output.load()
    
    for i in range(1, width - 1):
        for j in range(1, height - 1):
            if res[i][j] == weak_pixel:
                # Periksa apakah ada tetangga 8-arah yang berstatus Strong
                has_strong_neighbor = False
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if res[i + k][j + l] == strong_pixel:
                            has_strong_neighbor = True
                            break
                if has_strong_neighbor:
                    res[i][j] = strong_pixel
                else:
                    res[i][j] = 0
            
            # Masukkan hasil ke kanvas gambar output
            val = res[i][j]
            pixels_out[i, j] = (val, val, val)

    # Kembalikan ke Color Depth asli
    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
        
    return img_output

def ImgEmbossFilter(img_input, coldepth):
    # 1. Paksa gambar ke Grayscale (L) untuk menjamin output abu-abu merata
    img_gray = img_input.convert('L')
    
    width, height = img_gray.size
    img_output = Image.new('L', (width, height))
    pixels_in = img_gray.load()
    pixels_out = img_output.load()

    # Inisialisasi awal kanvas dengan warna abu-abu netral
    for i in range(width):
        for j in range(height):
            pixels_out[i, j] = 128

    # ROMBAK TOTAL: Menggunakan Kernel Landai 3x3 untuk Efek Smooth Pahatan
    # Nilai pusat 0 dan selisih kecil membuat gradasi abu-abu sangat halus
    kernel = [
        [-1, -1,  0],
        [-1,  0,  1],
        [ 0,  1,  1]
    ]
    
    offset = 1
    bias = 128  # Nilai tengah abu-abu semen/logam

    # 2. Proses Konvolusi Manual
    for i in range(offset, width - offset):
        for j in range(offset, height - offset):
            sum_val = 0.0
            
            for k in range(-offset, offset + 1):
                for l in range(-offset, offset + 1):
                    pixel_value = pixels_in[i + k, j + l]
                    weight = kernel[k + offset][l + offset]
                    
                    sum_val += pixel_value * weight
            
            # Tambahkan bias 128
            res_val = int(sum_val + bias)
            
            # CLIPPING (Pembatasan ketat rentang warna 0 - 255)
            if res_val > 255: 
                res_val = 255
            elif res_val < 0: 
                res_val = 0
            
            pixels_out[i, j] = res_val

    # 3. Kembalikan ke RGB agar bisa dibaca dengan aman oleh GUI pendukung
    img_output = img_output.convert('RGB')

    if coldepth == 1:
        img_output = img_output.convert("1")
    elif coldepth == 8:
        img_output = img_output.convert("L")
        
    return img_output

def ImgErosion(img_input, coldepth, k_size=3):
    """
    Erosi menggunakan Algoritma Pergeseran Gambar (Image Shifting).
    """
    # Ubah ke mode Grayscale agar kalkulasi biner konsisten
    img_work = img_input.convert("L")
    offset = k_size // 2
    
    # Nilai dasar awal untuk Erosi adalah warna putih (255)
    # Kita akan mencari nilai MINIMUM dari setiap pergeseran
    eroded_img = img_work.copy()
    
    # Jalankan algoritma pergeseran koordinat sesuai ukuran kernel (offset)
    for dx in range(-offset, offset + 1):
        for dy in range(-offset, offset + 1):
            if dx == 0 and dy == 0:
                continue
            
            # Geser gambar secara utuh (Sama dengan menggeser kernel tetangga)
            # offset=(dx, dy) bertindak sebagai arah pergeseran koordinat matriks
            shifted = ImageChops.offset(img_work, dx, dy)
            
            # Fungsi Murni Pencarian Nilai Minimum (Erosi) antar dua gambar
            eroded_img = ImageChops.darker(eroded_img, shifted)
            
    if coldepth == 1:
        eroded_img = eroded_img.convert("1")
    return eroded_img


def ImgDilation(img_input, coldepth, k_size=3):
    """
    Dilatasi menggunakan Algoritma Pergeseran Gambar (Image Shifting).
    """
    img_work = img_input.convert("L")
    offset = k_size // 2
    
    dilated_img = img_work.copy()
    
    for dx in range(-offset, offset + 1):
        for dy in range(-offset, offset + 1):
            if dx == 0 and dy == 0:
                continue
                
            shifted = ImageChops.offset(img_work, dx, dy)
            
            # Fungsi Murni Pencarian Nilai Maksimum (Dilatasi) antar dua gambar
            dilated_img = ImageChops.lighter(dilated_img, shifted)
            
    if coldepth == 1:
        dilated_img = dilated_img.convert("1")
    return dilated_img  

def ImgOpening(img_input, coldepth, k_size=3, iterations=1):
    """Opening: Erosi sebanyak N kali, lalu Dilatasi sebanyak N kali"""
    # Ubah ke mode L agar perulangan dikonversi menjadi integer cepat
    img_current = img_input.convert("L")
    
    # 1. Jalankan Erosi berantai sebanyak jumlah iterasi dari GUI
    for _ in range(iterations):
        img_current = ImgErosion(img_current, coldepth, k_size)
        
    # 2. Jalankan Dilatasi berantai sebanyak jumlah iterasi dari GUI
    for _ in range(iterations):
        img_current = ImgDilation(img_current, coldepth, k_size)
        
    # 3. Kembalikan ke Color Depth asli di akhir proses
    if coldepth == 1:
        img_current = img_current.convert("1")
    elif coldepth == 8:
        img_current = img_current.convert("L")
    else:
        img_current = img_current.convert("RGB")
        
    return img_current


def ImgClosing(img_input, coldepth, k_size=3, iterations=1):
    """Closing: Dilatasi sebanyak N kali, lalu Erosi sebanyak N kali"""
    img_current = img_input.convert("L")
    
    # 1. Jalankan Dilatasi berantai sebanyak jumlah iterasi dari GUI
    for _ in range(iterations):
        img_current = ImgDilation(img_current, coldepth, k_size)
        
    # 2. Jalankan Erosi berantai sebanyak jumlah iterasi dari GUI
    for _ in range(iterations):
        img_current = ImgErosion(img_current, coldepth, k_size)
        
    if coldepth == 1:
        img_current = img_current.convert("1")
    elif coldepth == 8:
        img_current = img_current.convert("L")
    else:
        img_current = img_current.convert("RGB")
        
    return img_current