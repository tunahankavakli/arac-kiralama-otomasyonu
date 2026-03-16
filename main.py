import tkinter as tk
import arayuz_islemleri  # Mantıksal işlemleri ve buton olaylarını yöneten modülümüz


class AracKiralamaUygulamasi:
    """
    Uygulamanın Ana Penceresi (GUI).
    Bu sınıf sadece görsel öğeleri (Butonlar, Kutular, Listeler) oluşturur ve ekrana yerleştirir.
    Tıklama olayları ve veri işlemleri 'arayuz_islemleri.py' dosyasında yönetilir.
    """

    def __init__(self, root):
        self.root = root
        # Pencere Başlığı ve Boyut Ayarları
        self.root.title("Araç Kiralama Otomasyonu")
        self.root.geometry("950x600")  # Genişlik x Yükseklik
        self.root.resizable(False, False)  # Kullanıcı pencere boyutunu değiştiremesin

        self.root.configure(bg="white")  # Arka planı temiz bir beyaz yap

        # Olay Yöneticisini (Controller) başlatıyoruz.
        # 'self' parametresi göndererek, bu sınıftaki elemanlara (Entry, Listbox vb.)
        # diğer dosyadan erişilmesini sağlıyoruz.
        self.olaylar = arayuz_islemleri.OlayYonetici(self)

        # Arayüzü çizdiren fonksiyonu çağır
        self.arayuz_olustur()
        # Program açılır açılmaz listeyi güncel verilerle doldur
        self.olaylar.listeyi_guncelle()

    def arayuz_olustur(self):
        """
        Pencere üzerindeki tüm görsel bileşenleri (Widget) oluşturur ve yerleştirir.
        """

        # --- 1. ÜST BAŞLIK (HEADER) ---
        # Sayfanın en üstünde koyu mavi bir şerit
        baslik_frame = tk.Frame(self.root, bg="darkblue", height=70)
        baslik_frame.pack(fill="x")  # Yatayda (x ekseni) tam kapla

        # Başlık yazısı
        lbl_baslik = tk.Label(baslik_frame, text="ARAÇ KİRALAMA SİSTEMİ",
                              font=("Arial", 20, "bold"), fg="white", bg="darkblue")
        # place ile ortalayarak yerleştiriyoruz
        lbl_baslik.place(relx=0.5, rely=0.5, anchor="center")

        # --- 2. SOL PANEL (LİSTE VE FİLTRELEME) ---
        # Araçların listelendiği geniş alan (x=10 konumunda)
        sol_liste_frame = tk.Frame(self.root, bg="white")
        sol_liste_frame.place(x=10, y=80, width=600, height=500)

        # Filtreleme Seçenekleri (Radio Buttonlar)
        filtre_frame = tk.Frame(sol_liste_frame, bg="white")
        filtre_frame.pack(fill="x", pady=5)  # Listenin hemen üstüne yerleşir

        tk.Label(filtre_frame, text="Filtrele:", bg="white", font=("Arial", 10, "bold")).pack(side="left")

        # Filtreleme değişkeni (String tutar)
        self.filtre_var = tk.StringVar(value="Tümü")

        # Döngü ile radio butonları oluşturuyoruz (Kod tekrarını önlemek için)
        for text in ["Tümü", "Müsait", "Kirada"]:
            tk.Radiobutton(filtre_frame, text=text, variable=self.filtre_var, value=text,
                           bg="white", command=self.olaylar.listeyi_guncelle).pack(side="left", padx=10)

        # Araç Listesi (Listbox) Alanı
        list_frame = tk.Frame(sol_liste_frame)
        list_frame.pack(fill="both", expand=True)

        # Tablo başlıkları (Görsel amaçlı Label)
        tk.Label(list_frame, text="Plaka       | Marka      | Model      | Ücret   | Durum",
                 font=("Courier", 10, "bold"), bg="lightgray", anchor="w").pack(fill="x")

        # Liste kutusu (Veriler burada görünecek)
        self.liste_kutusu = tk.Listbox(list_frame, font=("Courier", 10), height=18)
        self.liste_kutusu.pack(side="left", fill="both", expand=True)

        # --- YENİ EKLENEN SATIR ---
        # Listeden bir şeye tıklandığında 'secilen_araci_doldur' fonksiyonunu çalıştır
        self.liste_kutusu.bind('<<ListboxSelect>>', self.olaylar.secilen_araci_doldur)

        # Kaydırma Çubuğu (Scrollbar)
        scrol = tk.Scrollbar(list_frame)
        scrol.pack(side="right", fill="y")
        # Listbox ile Scrollbar'ı birbirine bağlıyoruz
        self.liste_kutusu.config(yscrollcommand=scrol.set)
        scrol.config(command=self.liste_kutusu.yview)

        # Kiralama Butonları (Listenin Altında)
        aksiyon_frame = tk.Frame(sol_liste_frame, bg="white")
        aksiyon_frame.pack(fill="x", pady=10)

        # Kiralama Başlat Butonu (Mavi)
        tk.Button(aksiyon_frame, text="KİRALAMA BAŞLAT", bg="blue", fg="white", font=("Arial", 11, "bold"),
                  height=2, width=25, command=self.olaylar.kiralama_penceresi_ac).pack(side="left", padx=5)

        # İade Al Butonu (Sarı)
        tk.Button(aksiyon_frame, text="ARACI İADE AL", bg="gold", fg="black", font=("Arial", 11, "bold"),
                  height=2, width=25, command=self.olaylar.iade_al).pack(side="right", padx=5)

        # --- 3. SAĞ PANEL (VERİ GİRİŞ VE İŞLEMLER) ---
        # Veri girişi ve kontrol butonlarının olduğu alan (x=620 konumunda)
        sag_giris_frame = tk.Frame(self.root, bg="lightgray", bd=2, relief="groove")
        sag_giris_frame.place(x=620, y=80, width=320, height=500)

        tk.Label(sag_giris_frame, text="ARAÇ İŞLEMLERİ", font=("Arial", 12, "bold"),
                 bg="lightgray", fg="black").pack(pady=10)

        # Giriş Formu (Grid Yöntemi ile Düzenli Yerleşim)
        form_frame = tk.Frame(sag_giris_frame, bg="lightgray")
        form_frame.pack(pady=5)

        # Plaka Girişi
        tk.Label(form_frame, text="Plaka:", bg="lightgray").grid(row=0, column=0, sticky="e", pady=5)
        self.ent_plaka = tk.Entry(form_frame, width=20)
        self.ent_plaka.grid(row=0, column=1, pady=5, padx=5)

        # Marka Girişi
        tk.Label(form_frame, text="Marka:", bg="lightgray").grid(row=1, column=0, sticky="e", pady=5)
        self.ent_marka = tk.Entry(form_frame, width=20)
        self.ent_marka.grid(row=1, column=1, pady=5, padx=5)

        # Model Girişi
        tk.Label(form_frame, text="Model:", bg="lightgray").grid(row=2, column=0, sticky="e", pady=5)
        self.ent_model = tk.Entry(form_frame, width=20)
        self.ent_model.grid(row=2, column=1, pady=5, padx=5)

        # Ücret Girişi
        tk.Label(form_frame, text="Ücret:", bg="lightgray").grid(row=3, column=0, sticky="e", pady=5)
        self.ent_ucret = tk.Entry(form_frame, width=20)
        self.ent_ucret.grid(row=3, column=1, pady=5, padx=5)

        # İşlem Butonları (Kaydet, Sil, Temizle)
        btn_frame = tk.Frame(sag_giris_frame, bg="lightgray")
        btn_frame.pack(pady=15, fill="x", padx=20)

        tk.Button(btn_frame, text="KAYDET", bg="green", fg="white", font=("Arial", 10, "bold"),
                  command=self.olaylar.arac_ekle).pack(fill="x", pady=5)

        tk.Button(btn_frame, text="SEÇİLİ ARACI SİL", bg="red", fg="white", font=("Arial", 10, "bold"),
                  command=self.olaylar.arac_sil).pack(fill="x", pady=5)

        tk.Button(btn_frame, text="TEMİZLE", bg="gray", fg="white",
                  command=self.olaylar.formu_temizle).pack(fill="x", pady=5)

        # --- RAPORLAR BÖLÜMÜ ---
        tk.Label(sag_giris_frame, text="--- RAPORLAR ---", bg="lightgray", fg="black").pack(pady=(20, 5))

        # Grafik Rapor Butonu
        tk.Button(sag_giris_frame, text="Grafiksel Rapor", bg="lightblue",
                  command=self.olaylar.grafik_rapor_penceresi).pack(fill="x", padx=20, pady=2)

        # Geçmiş Kayıtlar Butonu
        tk.Button(sag_giris_frame, text="Geçmiş Kayıtlar", bg="orange", fg="black",
                  command=self.olaylar.tarih_arama_penceresi).pack(fill="x", padx=20, pady=2)

        # Geçmişi Sıfırlama Butonu (Tehlikeli işlem -> Kırmızı)
        tk.Button(sag_giris_frame, text="Geçmişi Sıfırla", bg="red", fg="white",
                  command=self.olaylar.gecmisi_temizle).pack(fill="x", padx=20, pady=2)


# Programın ana çalışma bloğu
if __name__ == "__main__":
    root = tk.Tk()  # Ana pencereyi oluştur
    app = AracKiralamaUygulamasi(root)  # Uygulama sınıfını başlat
    root.mainloop()  # Pencereyi ekranda tut (Döngüye gir)