class Arac:
    """
    Araç Kiralama Otomasyonu için 'Araç' nesnesini modelleyen sınıf.
    Bu sınıf, bir aracın plaka, marka, model gibi temel özelliklerini
    ve kiralama durumunu (kimde, ne zaman) bir arada tutar.
    """

    def __init__(self, plaka, marka, model, ucret, durum="musait", kiralayan="-", baslangic="-", bitis="-"):
        # Yapıcı Metot (Constructor): Nesne ilk oluşturulduğunda çalışır.
        # Gelen parametreleri nesnenin özelliklerine (attribute) atıyoruz.

        # Temel Araç Bilgileri
        self.plaka = plaka  # Aracın plakası (Benzersiz kimlik)
        self.marka = marka  # Aracın markası (Örn: Toyota)
        self.model = model  # Aracın modeli (Örn: Corolla)
        self.ucret = ucret  # Günlük kiralama ücreti

        # Durum Bilgileri (Varsayılan olarak 'musait' başlar)
        self.durum = durum  # Aracın anlık durumu: 'musait' veya 'kirada'

        # Kiralama Detayları
        # (Eğer araç müsaitse, müşteri ve tarih bilgileri boş '-' olarak tutulur)
        self.kiralayan = kiralayan  # Aracı kiralayan müşterinin adı
        self.baslangic = baslangic  # Kiralama başlangıç tarihi
        self.bitis = bitis  # Kiralama bitiş tarihi

    def __str__(self):
        """
        Özel Metot (__str__): Nesneyi string (metin) formatına çevirir.

        Amaç: Bu nesneyi dosyaya kaydederken CSV (Comma Separated Values) formatına
        uygun hale getirmektir. Tüm özellikleri aralarına virgül koyarak birleştirir.
        Örnek Çıktı: "34ABC12,Fiat,Egea,1000,musait,-,-,-"
        """
        return self.plaka + "," + self.marka + "," + self.model + "," + str(
            self.ucret) + "," + self.durum + "," + self.kiralayan + "," + self.baslangic + "," + self.bitis