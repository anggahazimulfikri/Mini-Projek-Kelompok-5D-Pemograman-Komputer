import csv

file_csv = "Nutrisi_pangan_Indonesia.csv"

#AKG = [(Umur),(Berat Badan),(Kalori),(Protein)]
#Sumber: jurnal PERMENKES no 28 Tahun 2019 tentang Angka Kecukupan Gizi (AKG) untuk masyarakat Indonesia
AKG_LAKI = [[15, 50, 2400, 70], [18, 60, 2650, 75], [29, 60, 2650, 65], [49, 60, 2550, 65],
            [64, 60, 2150, 65], [80, 58, 1800, 64], [200, 58, 1600, 64]]
AKG_PEREMPUAN = [[15, 48, 2050, 65], [18, 52, 2100, 65], [29, 55, 2250, 60], [49, 56, 2150, 60],
                 [64, 56, 1800, 60], [80, 53, 1550, 58], [200, 53, 1400, 58]]

def baca_data(file_csv):    
    data_valid = []
    tidak_valid = 0
    try:
        with open(file_csv, 'r', encoding='utf-8') as file:
            for baris in csv.DictReader(file):
                try:
                    nama = baris["name"].strip()
                    kalori = float(baris["calories"])
                    protein = float(baris["proteins"])
                    lemak = float(baris["fat"])
                    karbo = float(baris["carbohydrate"])
                except (ValueError, KeyError):
                    tidak_valid += 1
                    continue
                total = protein + lemak + karbo
                if nama == "" or kalori <= 0 or total <= 0 or total > 100.5:
                    tidak_valid += 1
                else:
                    data_valid.append([nama, kalori, protein, lemak, karbo])
    except FileNotFoundError:
        print("Error: File", file_csv, "tidak ditemukan.")
    return data_valid, tidak_valid

def input_data(pesan, minimal, maksimal):
    while True:
        try:
            angka = float(input(pesan))
            if minimal <= angka <= maksimal:
                return angka
        except ValueError:
            pass
        print("Input tidak valid. Masukkan angka", minimal, "sampai", maksimal)

def hitung_kebutuhan(jenis_kelamin, usia, berat_badan):
    if jenis_kelamin == "L":
        tabel = AKG_LAKI
    else:
        tabel = AKG_PEREMPUAN
    for baris in tabel:
        if usia <= baris[0]:                  #Sumber baris : AKG_LAKI dan AKG_PEREMPUAN
            break
    faktor = berat_badan / baris[1]           #Sumber: Jurnal Profil Asupan dan Status Gizi pada Responden yang Memiliki Kebiasaan Menonton Video Mukbang
    energi_harian = baris[2] * faktor
    protein_harian = baris[3] * faktor
    return energi_harian, protein_harian

def nilai_kesehatan(kalori, protein, lemak, karbo, energi_harian, protein_harian):
    rincian = []
    skor = 0

    persen_energi = kalori / energi_harian * 100        
    persen_protein = protein / protein_harian * 100
    rasio = persen_protein / persen_energi * 100
    if rasio < 90:
        status = "KURANG"
    else:
        status = "NORMAL"
        skor += 1
    rincian.append(["Protein", f"{rasio:.0f}% dari kebutuhan", "90%+", status])

    total_energi = 4 * protein + 9 * lemak + 4 * karbo        #Sumber: Modul Sumber, Fungsi, dan Kecukupan Komsumsi Zat Gizi
    persen_lemak = 9 * lemak / total_energi * 100
    persen_karbo = 4 * karbo / total_energi * 100

    if persen_lemak < 20:                                     #Sumber: Jurnal Profil Asupan dan Status Gizi pada Responden yang Memiliki Kebiasaan Menonton Video Mukbang
        status = "KURANG"
    elif persen_lemak <= 30:
        status = "NORMAL"
        skor += 1
    else:
        status = "LEBIH"
    rincian.append(["Lemak", f"{persen_lemak:.0f}% energi", "20-30%", status])

    if persen_karbo < 45:
        status = "KURANG"
    elif persen_karbo <= 60:
        status = "NORMAL"
        skor += 1
    else:
        status = "LEBIH"
    rincian.append(["Karbohidrat", f"{persen_karbo:.0f}% energi", "45-60%", status])

    if skor == 3:
        kategori = "SEHAT"
    elif skor == 2:
        kategori = "CUKUP SEHAT"
    else:
        kategori = "KURANG SEHAT"
    return skor, kategori, rincian

data_valid, tidak_valid = baca_data(file_csv)
if len(data_valid) == 0:
    print("Program dihentikan karena tidak ada data.")
else:
    print("=== ANALISIS GIZI MAKANAN & REKOMENDASI KESEHATAN ===")
    print("Dataset dimuat:", len(data_valid), "makanan (data tidak valid:", tidak_valid, ")\n")
    print("L = Laki-laki, P = Perempuan")

    LEBAR = 25

    jenis_kelamin = ""
    while jenis_kelamin != "L" and jenis_kelamin != "P":
        jenis_kelamin = input(f"{'Jenis kelamin (L/P)':<{LEBAR}}: ").strip().upper()
    usia = input_data(f"{'Usia (tahun, 13-100)':<{LEBAR}}: ", 13, 100)
    berat_badan = input_data(f"{'Berat badan (kg)':<{LEBAR}}: ", 30, 200)
    
    energi_harian, protein_harian = hitung_kebutuhan(jenis_kelamin, usia, berat_badan)
    print(f"\n{'Kebutuhan sehari Anda':<{LEBAR}}: {energi_harian:.0f} kkal, {protein_harian:.0f} g protein\n")

    lanjut = "y"
    while lanjut == "y":

        hasil = []
        while len(hasil) == 0:
            kata = input(f"{'Nama makanan':<{LEBAR}}: ").strip().lower()
            for m in data_valid:
                if kata != "" and kata in m[0].lower() and len(hasil) < 10:
                    hasil.append(m)
            if len(hasil) == 0:
                print("  Makanan tidak ditemukan. Coba kata kunci lain.")

        print("  Hasil pencarian:")
        for i in range(len(hasil)):
            print(f"{i + 1}. {hasil[i][0]}")
        nomor = int(input_data(f"{'Pilih nomor makanan':<{LEBAR}}: ", 1, len(hasil)))
        makanan = hasil[nomor - 1]
        gram = input_data(f"{'Berat porsi (gram)':<{LEBAR}}: ", 1, 2000)

        faktor = gram / 100                          
        kalori = makanan[1] * faktor                 #Sumber baris : data_valid (data CSV Nutrisi_pangan_Indonesia.csv)
        protein = makanan[2] * faktor
        lemak = makanan[3] * faktor
        karbo = makanan[4] * faktor

        skor, kategori, rincian = nilai_kesehatan(kalori, protein, lemak, karbo, energi_harian, protein_harian)

        print("\n" + "=" * 56)
        print(f"HASIL ANALISIS: {makanan[0]} ({gram:g} g)")
        print("=" * 56)
        print(f"Kalori       : {kalori:.1f} kkal ({kalori / energi_harian * 100:.0f}% kebutuhan sehari)")
        print(f"Protein      : {protein:.1f} g ({protein / protein_harian * 100:.0f}% kebutuhan sehari)")
        print(f"Lemak        : {lemak:.1f} g")
        print(f"Karbohidrat  : {karbo:.1f} g")
        print("-" * 56)
        for nama, nilai, acuan, status in rincian:
            print(f"{nama:<12} : {nilai:<18} (acuan {acuan:<7}) [{status}]")
        print("-" * 56)
        print(f"KATEGORI     : {kategori} (skor {skor}/3)")

        print("\nREKOMENDASI:")
        for nama, nilai, acuan, status in rincian:
            if status == "LEBIH":
                print(f"- Kandungan {nama.lower()} tinggi; kurangi atau seimbangkan dengan makanan lain.")
            elif status == "KURANG":
                print(f"- Kandungan {nama.lower()} rendah; tambahkan makanan sumber {nama.lower()}.")
        if kategori == "SEHAT":
            print("- Makanan ini sudah sesuai kebutuhan Anda. Pertahankan!")
        else:
            print("- Contoh makanan yang lebih seimbang (per 100 g):")
            jumlah = 0
            for m in data_valid:
                if jumlah < 3 and m[0] != makanan[0] and 50 <= m[1] <= 300 and "mentah" not in m[0].lower():
                    s, k, r = nilai_kesehatan(m[1], m[2], m[3], m[4], energi_harian, protein_harian)
                    if s == 3:
                        print(f"    * {m[0]} ({m[1]:.0f} kkal)")
                        jumlah += 1
        print("Catatan: rekomendasi bersifat umum, bukan pengganti konsultasi tenaga kesehatan.")


        lanjut = input(f"\n{'Cek makanan lain? (y/n)':<{LEBAR}}: ").strip().lower()

    print("Terima kasih telah menggunakan program ini.")
