class BRC:
    def barrierRaster(awal, akhir, peta):
        jumlah = 0
        x1, y1 = awal
        x2, y2 = akhir

        for i in range(y1, y2):
            for j in range(x1, x2):
                if peta[i][j] == 1:
                    jumlah += 1
                    
        lebar = x2 - x1
        tinggi = y2 - y1
        luas = lebar * tinggi
        koeficien = jumlah / luas
        return koeficien
    
    # def barrierRasterLib(self):
    #     sub_peta = self.peta[self.awal[1]:self.akhir[1], self.awal[0]:self.akhir[0]]
    #     self.jumlah = np.jumlah_nonzero(sub_peta == 1)
    #     return self.jumlah
