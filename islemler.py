import os
from datetime import datetime
import arac  # Araç nesnesini kullanmak için kendi modülümüzü çağırıyoruz


class VeriYonetimi:
    """
    Bu sınıf projenin 'Backend' (Veri Yönetimi) kısmıdır.
    Dosya okuma/yazma, istatistik hesaplama, tarih işlemleri ve
    filtreleme gibi mantıksal işlemler burada yapılır.
    """

    def __init__(self):
        # Dosya isimlerini tanımlıyoruz (Veritabanı yerine CSV kullanıyoruz)
        self.dosya_araclar = "araclar.csv"  # Araçların güncel durumu
        self.dosya_gecmis = "gecmis.csv"  # Geçmiş kiralama kayıtları (Log)

        # Sınıf başlatıldığında dosyaların var olup olmadığını kontrol et
        self.dosya_kontrol()

    def dosya_kontrol(self):
        """
        Program çalıştırıldığında gerekli dosyalar yoksa hata vermemesi için
        boş dosyalar oluşturur. (os modülü kullanılarak)
        """
        if not os.path.exists(self.dosya_araclar):
            with open(self.dosya_araclar, "w", encoding="utf-8") as f:
                pass  # Dosya oluşturulur ve hemen kapatılır

        if not os.path.exists(self.dosya_gecmis):
            with open(self.dosya_gecmis, "w", encoding="utf-8") as f:
                pass

    def araclari_yukle(self):
        """
        araclar.csv dosyasını okur, her satırı bir 'Arac' nesnesine çevirir
        ve bunları bir liste olarak döndürür.
        """
        arac_listesi = []
        # 'r' modu ile okuma yapıyoruz
        with open(self.dosya_araclar, "r", encoding="utf-8") as dosya:
            satirlar = dosya.readlines()
            for satir in satirlar:
                satir = satir.strip()  # Satır sonundaki boşlukları ve \n karakterini temizle
                if len(satir) > 0:
                    # CSV formatı olduğu için virgüllerden ayırıyoruz
                    veri = satir.split(",")

                    # Veri bütünlüğü kontrolü (Eksik bilgi var mı?)
                    if len(veri) >= 8:
                        # Listeden gelen verilerle Nesne (Object) oluşturuyoruz
                        yeni_arac = arac.Arac(veri[0], veri[1], veri[2], veri[3], veri[4], veri[5], veri[6], veri[7])
                        arac_listesi.append(yeni_arac)
        return arac_listesi

    def araclari_kaydet(self, arac_listesi):
        """
        Listedeki güncel araç durumlarını dosyaya kaydeder.
        'w' modu kullandığımız için dosya her seferinde silinip baştan yazılır.
        """
        with open(self.dosya_araclar, "w", encoding="utf-8") as dosya:
            for a in arac_listesi:
                # Nesnenin __str__ metodunu kullanarak stringe çevirip yazıyoruz
                dosya.write(str(a) + "\n")

    def gecmise_ekle(self, plaka, marka, musteri, tutar, tarih):
        """
        Yapılan kiralama işlemini geçmiş dosyasına ekler.
        'a' (append) modu kullandığımız için eski kayıtlar silinmez, altına eklenir.
        """
        with open(self.dosya_gecmis, "a", encoding="utf-8") as dosya:
            satir = f"{plaka},{marka},{musteri},{tutar},{tarih}\n"
            dosya.write(satir)

    def istatistikleri_getir(self):
        """
        Geçmiş dosyasını okuyarak Toplam Gelir ve En Çok Kiralanan Markayı hesaplar.
        """
        toplam_gelir = 0
        marka_sayilari = {}  # Hangi markadan kaç tane kiralandığını tutacak sözlük (Dictionary)

        with open(self.dosya_gecmis, "r", encoding="utf-8") as dosya:
            satirlar = dosya.readlines()
            for satir in satirlar:
                veri = satir.strip().split(",")
                if len(veri) >= 5:
                    try:
                        # 3. indekste tutar bilgisi var, int'e çevirip topluyoruz
                        tutar = int(veri[3])
                        toplam_gelir += tutar
                    except:
                        pass  # Eğer sayısal bir hata varsa o satırı atla

                    # Marka sayımı
                    marka = veri[1]
                    if marka in marka_sayilari:
                        marka_sayilari[marka] += 1
                    else:
                        marka_sayilari[marka] = 1

        # En çok kiralanan markayı bulma algoritması
        en_cok_marka = "Yok"
        max_sayi = 0
        for m, sayi in marka_sayilari.items():
            if sayi > max_sayi:
                max_sayi = sayi
                en_cok_marka = m

        return toplam_gelir, en_cok_marka, marka_sayilari

    def tarih_araliginda_bul(self, bas_tarih, bit_tarih):
        """
        Verilen iki tarih arasındaki işlemleri bulur.
        datetime kütüphanesi ile tarih karşılaştırması yapılır.
        """
        format = "%Y-%m-%d"
        bulunanlar = []
        try:
            # String tarihleri datetime objesine çeviriyoruz
            d1 = datetime.strptime(bas_tarih, format)
            d2 = datetime.strptime(bit_tarih, format)

            with open(self.dosya_gecmis, "r", encoding="utf-8") as dosya:
                for satir in dosya:
                    veri = satir.strip().split(",")
                    if len(veri) >= 5:
                        islem_tarihi_str = veri[4]  # İşlem tarihi sütunu
                        d_islem = datetime.strptime(islem_tarihi_str, format)

                        # Zincirleme karşılaştırma (Tarih aralıkta mı?)
                        if d1 <= d_islem <= d2:
                            bulunanlar.append(satir.strip())
        except:
            return None  # Tarih formatı hatalıysa None döndür

        return bulunanlar

    def gun_farki_hesapla(self, baslangic, bitis):
        """İki tarih arasındaki gün farkını hesaplar."""
        format = "%Y-%m-%d"
        try:
            d1 = datetime.strptime(baslangic, format)
            d2 = datetime.strptime(bitis, format)
            return (d2 - d1).days  # timedelta nesnesinden gün sayısını al
        except:
            return -1  # Hata durumunda -1 döndür

    def filtrele(self, arac_listesi, durum_filtresi):
        """
        Arayüzden gelen filtre seçimine (Müsait, Kirada) göre
        listeyi süzer ve yeni bir liste döndürür.
        """
        if durum_filtresi == "Tümü": return arac_listesi

        # Arayüzdeki "Müsait" yazısını veritabanındaki "musait" ile eşleştiriyoruz
        aranan = "musait" if durum_filtresi == "Müsait" else "kirada"

        filtrelenmis = []
        for a in arac_listesi:
            if a.durum == aranan:
                filtrelenmis.append(a)
        return filtrelenmis

    def gecmisi_sifirla(self):
        """
        Geçmiş kayıtları tamamen siler.
        'w' modu ile açıp hiçbir şey yazmadan kapatmak dosya içeriğini temizler.
        """
        with open(self.dosya_gecmis, "w", encoding="utf-8") as dosya:
            pass