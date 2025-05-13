import cv2
import cv2.aruco as aruco
import os
import numpy as np

# Tentukan dictionary marker ArUco
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# Buat folder output jika belum ada
output_folder = "./ControlRobot/Marker/markers"
os.makedirs(output_folder, exist_ok=True)

# Jumlah marker yang ingin dibuat
jumlah_marker = 10  # Ganti sesuai kebutuhan

# Ukuran marker dalam pixel
marker_size = 200  # Ukuran area hitam-putih dari marker (isi)

# Ketebalan stroke putih di sekeliling marker (padding)
stroke_thickness = 10  # dalam pixel

# Loop untuk membuat beberapa marker
for id in range(jumlah_marker):
    # Buat marker
    marker_img = aruco.generateImageMarker(aruco_dict, id, marker_size)

    # Tambahkan padding putih
    marker_with_stroke = cv2.copyMakeBorder(
        marker_img,
        top=stroke_thickness,
        bottom=stroke_thickness,
        left=stroke_thickness,
        right=stroke_thickness,
        borderType=cv2.BORDER_CONSTANT,
        value=[255, 255, 255]  # Warna putih
    )

    # Simpan hasilnya
    filename = f"{output_folder}/aruco_marker_{id}.png"
    cv2.imwrite(filename, marker_with_stroke)
    print(f"Marker ID {id} disimpan ke {filename}")
