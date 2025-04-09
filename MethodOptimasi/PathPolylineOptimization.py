import numpy as np
import pandas as pd
import math

class NodeCut:
    def supercover_line(awal, akhir):
        x1, y1 = awal
        x2, y2 = akhir

        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        x, y = x1, y1
        xstep = 1 if x2 > x1 else -1
        ystep = 1 if y2 > y1 else -1

        ddy = 2 * dy
        ddx = 2 * dx

        points.append((x, y))

        if ddx >= ddy:  # First octant (0 <= slope <= 1)
            errorprev = error = dx  
            for _ in range(dx):
                x += xstep
                error += ddy
                if error > ddx:
                    y += ystep
                    error -= ddx
                    if error + errorprev < ddx:
                        points.append((x, y - ystep))
                    elif error + errorprev > ddx:
                        points.append((x - xstep, y))
                    else:
                        points.append((x, y - ystep))
                        points.append((x - xstep, y))
                points.append((x, y))
                errorprev = error
        else:  # Second octant (1 < slope)
            errorprev = error = dy
            for _ in range(dy):
                y += ystep
                error += ddx
                if error > ddy:
                    x += xstep
                    error -= ddy
                    if error + errorprev < ddy:
                        points.append((x - xstep, y))
                    elif error + errorprev > ddy:
                        points.append((x, y - ystep))
                    else:
                        points.append((x - xstep, y))
                        points.append((x, y - ystep))
                points.append((x, y))
                errorprev = error

        return points
    
    def lompatanAman(awal, akhir, peta):
        """Check if any node in the path is an obstacle (1)."""
        nodes = NodeCut.supercover_line(awal, akhir)
        if(any(peta[y][x] == 1 for x, y in nodes)):
            return False
        else:
            return True

    def is_one_point_move(awal, akhir):
        x1, y1 = awal
        x2, y2 = akhir
        if (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) <= 1.5):
            return True
        else:
            return False
        
    def is_45_degree(awal, akhir):
        x1, y1 = awal
        x2, y2 = akhir
        
        if x2 - x1 == 0:  # Menghindari pembagian dengan nol (garis vertikal)
            return False
        slope = (y2 - y1) / (x2 - x1)
        return slope == 1 or slope == -1

    def prunning(jalur, peta):
        awal = 0
        akhir = 1
        awal_t = awal
        akhir_t = akhir
        jalur_prunning = [jalur[awal]]
        while True:
            while akhir <= len(jalur)-1:
                if not (NodeCut.lompatanAman(jalur[awal], jalur[akhir], peta)):
                    # print(f"Dari awal {jalur[awal]} dan akhir {jalur[akhir]} tidak aman!")
                    if (NodeCut.is_45_degree(jalur[awal], jalur[akhir])):
                        akhir += 1
                        break
                    elif akhir == len(jalur):
                        jalur_prunning.append(jalur[akhir])
                        break
                    else:
                        jalur_prunning.append(jalur[akhir-1])
                        awal = akhir - 1
                        break
                else:
                    # print(f"Dari awal {jalur[awal]} dan akhir {jalur[akhir]} aman!")
                    akhir += 1
            if (awal_t == awal and akhir_t == akhir):
                break
            awal_t = awal
            akhir_t = akhir
        jalur_prunning.append(jalur[len(jalur)-1])
        return jalur_prunning


# # Example usage:
# from main import utama

# peta, jalur = utama()

# peta_ori = peta

# print(peta_ori)

# # Cetak jalur
# if jalur:
#     print("Jalur ditemukan:", jalur)

#     for titik in jalur:
#         peta[titik[1], titik[0]] = 7  # Tandai jalur dengan nilai 7
    
#     # Ubah nilai dalam array sesuai permintaan
#     peta = np.where(peta == 0, '.', peta)  # 0 menjadi titik (.)
#     peta = np.where(peta == '1', '#', peta)  # 1 menjadi halangan (#)
#     peta = np.where(peta == '2', '#', peta)  # 2 menjadi halangan (#)
#     peta = np.where(peta == '7', '@', peta)  # 7 menjadi jalur (*)

#     # Konversi peta ke pandas DataFrame untuk visualisasi yang lebih baik
#     df = pd.DataFrame(peta)
#     print("Peta dengan Jalur (direpresentasikan oleh 2):")
#     print(df)
# else:
#     print("Tidak ada jalur yang ditemukan")

# print("Jalur sebelumnya ", jalur)
# print("Jalur Setelah Prunning ", NodeCut.prunning(jalur, peta_ori))
