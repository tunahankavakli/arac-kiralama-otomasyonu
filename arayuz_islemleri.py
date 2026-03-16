import tkinter as tk
from tkinter import messagebox, Toplevel, Canvas
import islemler
import arac
import kontrol
import datetime


class OlayYonetici:
    """
    Bu sınıf, kullanıcı arayüzündeki (Butonlar, Listeler vb.) etkileşimleri yönetir.
    Backend (islemler.py) ile Frontend (main.py) arasındaki köprüdür (Controller).
    """

    def __init__(self, ana_uygulama):
        # Main.py'daki ana uygulama nesnesine erişim sağlıyoruz (Entry, Listbox vb. için)
        self.app = ana_uygulama

        # Veri tabanı işlemlerini yapan sınıfı başlatıyoruz
        self.yonetim = islemler.VeriYonetimi()

        # Program açıldığında araçları dosyadan (araclar.csv) hafızaya yüklüyoruz
        self.araclar = self.yonetim.araclari_yukle()

    def listeyi_guncelle(self):
        """
        Listbox'ı temizler ve filtreleme seçeneğine göre (Tümü, Müsait, Kirada)
        araçları yeniden listeler.
        """
        self.app.liste_kutusu.delete(0, tk.END)  # Mevcut listeyi temizle
        secili_filtre = self.app.filtre_var.get()  # Radiobutton'dan seçimi al

        # Backend'den filtrelenmiş listeyi getir
        gosterilecek = self.yonetim.filtrele(self.araclar, secili_filtre)

        for a in gosterilecek:
            # Durum sütununu daha okunaklı hale getir
            durum = "[MÜSAİT]"
            if a.durum == "kirada":
                durum = f"[KİRADA: {a.kiralayan}]"

            # ljust/rjust metotları ile metin hizalaması yapıyoruz (Tablo görünümü için)
            satir = f"{a.plaka.ljust(10)} | {a.marka.ljust(10)} | {a.model.ljust(10)} | {str(a.ucret).rjust(5)} TL | {durum}"
            self.app.liste_kutusu.insert(tk.END, satir)

    def formu_temizle(self):
        """Araç ekleme formundaki giriş kutularını (Entry) temizler."""
        self.app.ent_plaka.delete(0, tk.END)
        self.app.ent_marka.delete(0, tk.END)
        self.app.ent_model.delete(0, tk.END)
        self.app.ent_ucret.delete(0, tk.END)

    def secilen_araci_doldur(self, event):
        """
        Listeden bir satıra tıklandığında çalışır.
        Seçilen aracın bilgilerini bulur ve sağdaki giriş kutularına yazar.
        """
        secili = self.app.liste_kutusu.curselection()
        if not secili:
            return  # Seçim yoksa işlem yapma

        # Seçili satırdan plakayı çek
        satir = self.app.liste_kutusu.get(secili[0])
        plaka = satir.split("|")[0].strip()

        # Bu plakaya sahip aracı bul
        secili_arac = None
        for a in self.araclar:
            if a.plaka == plaka:
                secili_arac = a
                break

        if secili_arac:
            # Önce kutuları temizle
            self.formu_temizle()

            # Sonra bilgileri doldur
            self.app.ent_plaka.insert(0, secili_arac.plaka)
            self.app.ent_marka.insert(0, secili_arac.marka)
            self.app.ent_model.insert(0, secili_arac.model)
            self.app.ent_ucret.insert(0, str(secili_arac.ucret))

    def arac_ekle(self):
        """
        Eğer plaka zaten varsa özelliklerini günceller, yoksa yeni ekler.
        """
        # Verileri al
        plaka = self.app.ent_plaka.get()
        marka = self.app.ent_marka.get()
        model = self.app.ent_model.get()
        ucret = self.app.ent_ucret.get()

        # --- VALIDASYON ---
        plaka_sonuc = kontrol.plaka_kontrol(plaka)
        if plaka_sonuc[0] == False:
            messagebox.showerror("Hata", plaka_sonuc[1])
            return

        if len(marka) < 2 or len(model) < 2:
            messagebox.showerror("Hata", "Marka ve Model en az 2 harf olmalı.")
            return

        if not ucret.isdigit():
            messagebox.showerror("Hata", "Ücret kısmına sadece sayı giriniz.")
            return

        # Plakayı temizle
        temiz_plaka = plaka.upper().replace(" ", "")

        # --- MANTIK KISMI (GÜNCELLEME Mİ, EKLEME Mİ?) ---
        arac_bulundu = False

        # Listeyi tara, bu plaka var mı bak
        for a in self.araclar:
            if a.plaka == temiz_plaka:
                # ARAÇ ZATEN VAR -> GÜNCELLE
                a.marka = marka
                a.model = model
                a.ucret = ucret
                arac_bulundu = True
                mesaj = "Araç bilgileri güncellendi."
                break

        # Eğer döngü bitti ve araç bulunamadıysa -> YENİ EKLE
        if not arac_bulundu:
            yeni_arac = arac.Arac(temiz_plaka, marka, model, ucret)
            self.araclar.append(yeni_arac)
            mesaj = "Yeni araç eklendi."

        # Dosyayı kaydet ve ekranı yenile
        self.yonetim.araclari_kaydet(self.araclar)
        self.listeyi_guncelle()
        self.formu_temizle()
        messagebox.showinfo("İşlem Başarılı", mesaj)

    def arac_sil(self):
        """Seçili aracı listeden ve dosyadan siler."""
        secili = self.app.liste_kutusu.curselection()

        # Eğer listeden seçim yapılmadıysa uyar
        if not secili:
            messagebox.showwarning("Uyarı", "Lütfen listeden silinecek aracı seçin.")
            return

        # Seçili satırdan plakayı ayrıştır
        satir = self.app.liste_kutusu.get(secili[0])
        plaka = satir.split("|")[0].strip()

        # Kullanıcıdan son onay al
        cevap = messagebox.askyesno("Silme Onayı", f"{plaka} plakalı araç silinsin mi?")
        if cevap:
            # Listeyi dolaş, plakası eşleşen aracı bul ve sil
            for i, a in enumerate(self.araclar):
                if a.plaka == plaka:
                    del self.araclar[i]
                    break

            self.yonetim.araclari_kaydet(self.araclar)
            self.listeyi_guncelle()
            messagebox.showinfo("Bilgi", "Araç başarıyla silindi.")

    def kiralama_penceresi_ac(self):
        """Kiralama işlemi için yeni bir pencere (Pop-up) açar."""
        secili = self.app.liste_kutusu.curselection()
        if not secili:
            messagebox.showwarning("Uyarı", "Lütfen kiralanacak aracı seçin.")
            return

        satir = self.app.liste_kutusu.get(secili[0])
        plaka = satir.split("|")[0].strip()

        # Aracı listeden bul
        secili_arac = None
        for a in self.araclar:
            if a.plaka == plaka:
                secili_arac = a
                break

        # Araç zaten kiradaysa işlem yapma
        if secili_arac.durum != "musait":
            messagebox.showerror("Hata", "Bu araç şu an kirada! Tekrar kiralanamaz.")
            return

        # --- YENİ PENCERE (TOPLEVEL) OLUŞTURMA ---
        pencere = Toplevel(self.app.root)
        pencere.title("Kiralama İşlemi")
        pencere.geometry("300x400")

        tk.Label(pencere, text=f"Seçilen Araç: {plaka}", font=("Arial", 12, "bold"), fg="blue").pack(pady=10)

        tk.Label(pencere, text="Müşteri Adı Soyadı:").pack()
        ent_mus = tk.Entry(pencere)
        ent_mus.pack()

        # Başlangıç tarihine bugünün tarihini otomatik yaz
        bugun = datetime.date.today().strftime("%Y-%m-%d")
        tk.Label(pencere, text="Başlangıç Tarihi (Yıl-Ay-Gün):").pack()
        ent_bas = tk.Entry(pencere)
        ent_bas.insert(0, bugun)
        ent_bas.pack()

        tk.Label(pencere, text="Bitiş Tarihi (Yıl-Ay-Gün):").pack()
        ent_bit = tk.Entry(pencere)
        ent_bit.pack()

        # Onaylama butonu için iç fonksiyon
        def onayla():
            # Tarih farkını hesapla (Gün sayısı)
            gun_sayisi = self.yonetim.gun_farki_hesapla(ent_bas.get(), ent_bit.get())

            if gun_sayisi <= 0:
                messagebox.showerror("Hata", "Tarihler hatalı! Bitiş tarihi başlangıçtan sonra olmalı.")
                return

            # Toplam tutar hesabı
            toplam_tutar = gun_sayisi * int(secili_arac.ucret)

            # Nesneyi güncelle
            secili_arac.durum = "kirada"
            secili_arac.kiralayan = ent_mus.get()
            secili_arac.baslangic = ent_bas.get()
            secili_arac.bitis = ent_bit.get()

            # Kaydet ve Güncelle
            self.yonetim.araclari_kaydet(self.araclar)

            # Gelir raporu için geçmiş dosyasına yaz
            self.yonetim.gecmise_ekle(secili_arac.plaka, secili_arac.marka, secili_arac.kiralayan, toplam_tutar,
                                      ent_bas.get())

            self.listeyi_guncelle()

            mesaj = f"Kiralama Başarılı!\n\nToplam Süre: {gun_sayisi} Gün\nÖdenecek Tutar: {toplam_tutar} TL"
            messagebox.showinfo("İşlem Tamam", mesaj)
            pencere.destroy()

        tk.Button(pencere, text="KİRALAMAYI ONAYLA", bg="green", fg="white", command=onayla).pack(pady=20)

    def iade_al(self):
        """Kiradaki aracı tekrar müsait duruma getirir."""
        secili = self.app.liste_kutusu.curselection()
        if not secili:
            messagebox.showwarning("Uyarı", "Lütfen teslim alınacak aracı seçin.")
            return

        satir = self.app.liste_kutusu.get(secili[0])
        plaka = satir.split("|")[0].strip()

        for a in self.araclar:
            if a.plaka == plaka:
                if a.durum == "musait":
                    messagebox.showinfo("Bilgi", "Bu araç zaten galeride (müsait).")
                else:
                    # Aracı sıfırla
                    eski_musteri = a.kiralayan
                    a.durum = "musait"
                    a.kiralayan = "-"
                    a.baslangic = "-"
                    a.bitis = "-"

                    self.yonetim.araclari_kaydet(self.araclar)
                    self.listeyi_guncelle()
                    messagebox.showinfo("Bilgi", f"Araç başarıyla teslim alındı.\nMüşteri: {eski_musteri}")
                break

    def gecmisi_temizle(self):
        """Tüm geçmiş ve gelir kayıtlarını siler (Riskli işlem)."""
        cevap = messagebox.askyesno("Dikkat", "Tüm geçmiş kayıtlar ve gelir bilgisi silinecek!\nEmin misiniz?")
        if cevap:
            self.yonetim.gecmisi_sifirla()
            messagebox.showinfo("Bilgi", "Geçmiş temizlendi.")

    def tarih_arama_penceresi(self):
        """Geçmiş kayıtları tarih aralığına göre arayan pencere."""
        pencere = Toplevel(self.app.root)
        pencere.title("Geçmiş Araması")
        pencere.geometry("400x400")

        tk.Label(pencere, text="Başlangıç Tarihi:").pack(pady=5)
        ent_bas = tk.Entry(pencere)
        ent_bas.pack()

        tk.Label(pencere, text="Bitiş Tarihi:").pack(pady=5)
        ent_bit = tk.Entry(pencere)
        ent_bit.pack()

        liste = tk.Listbox(pencere, width=60, height=15)
        liste.pack(pady=10)

        def ara():
            liste.delete(0, tk.END)
            # Backend'den sonuçları iste
            sonuclar = self.yonetim.tarih_araliginda_bul(ent_bas.get(), ent_bit.get())

            if sonuclar is None:
                messagebox.showerror("Hata", "Tarih formatı YYYY-AA-GG olmalı.")
            elif len(sonuclar) == 0:
                liste.insert(tk.END, "Bu tarihlerde kayıt bulunamadı.")
            else:
                for s in sonuclar:
                    liste.insert(tk.END, s)

        tk.Button(pencere, text="ARA", bg="orange", command=ara).pack()

    def grafik_rapor_penceresi(self):
        """
        Tkinter Canvas ile dinamik Pasta Grafiği çizer.
        """
        pencere = Toplevel(self.app.root)
        pencere.title("Grafiksel Rapor")
        pencere.geometry("600x500")

        # İstatistikleri getir
        gelir, en_cok_marka, marka_dagilimi = self.yonetim.istatistikleri_getir()

        lbl_info = tk.Label(pencere, text=f"TOPLAM CİRO: {gelir} TL\nEN POPÜLER MARKA: {en_cok_marka}",
                            font=("Arial", 12, "bold"), fg="darkblue")
        lbl_info.pack(pady=10)

        # Çizim alanı (Tuval)
        c = Canvas(pencere, bg="white", width=400, height=300)
        c.pack()

        if not marka_dagilimi:
            c.create_text(200, 150, text="Henüz yeterli veri yok.")
            return

        # Pasta Grafiği Matematiksel Hesaplaması
        toplam_kira_sayisi = sum(marka_dagilimi.values())
        baslangic_acisi = 0

        renkler = ["red", "blue", "green", "yellow", "orange", "purple", "cyan", "magenta"]
        yazi_y = 20

        for i, (marka, sayi) in enumerate(marka_dagilimi.items()):
            # Her markanın pastadaki payını (açısını) hesapla
            dilim_acisi = (sayi / toplam_kira_sayisi) * 360
            renk = renkler[i % len(renkler)]

            # Dilimi çiz (Arc)
            c.create_arc(50, 50, 250, 250, start=baslangic_acisi, extent=dilim_acisi, fill=renk)
            baslangic_acisi += dilim_acisi

            # Yan tarafa lejant (açıklama) ekle
            c.create_rectangle(280, yazi_y, 295, yazi_y + 15, fill=renk)
            c.create_text(300, yazi_y + 8, text=f"{marka} (%{int((sayi / toplam_kira_sayisi) * 100)})", anchor="w")
            yazi_y += 25

        c.create_text(150, 270, text="Markalara Göre Dağılım", font=("Arial", 10, "bold"))