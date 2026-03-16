# BU MODÜLÜN AMACI:
# Kullanıcı arayüzünden girilen verilerin (Plaka, Marka, Model vb.)
# veritabanına kaydedilmeden önce doğruluğunu kontrol etmektir (Validation).
# Bu sayede sisteme hatalı veri girişi engellenmiş olur.

def plaka_kontrol(plaka):
    """
    Girilen araç plakasının standartlara (Örn: 34ABC123) uygun olup olmadığını denetler.

    Parametre: plaka (str)
    Dönüş: (True/False, "Hata Mesajı") şeklinde bir Tuple döndürür.
    """

    # 1. STANDARTLAŞTIRMA:
    # Kullanıcı " 34 abc 12 " şeklinde boşluklu veya küçük harfli girebilir.
    # upper(): Hepsini büyük harf yap (34 ABC 12)
    # strip(): Baştaki/sondaki boşlukları sil
    # replace(" ", ""): Kelime aralarındaki boşlukları sil (34ABC12)
    plaka = plaka.upper().strip().replace(" ", "")

    # 2. UZUNLUK KONTROLÜ:
    # Türkiye'de plakalar en az 7 (06AA123), en fazla 9 (06AAA1234) karakter olabilir.
    if len(plaka) < 7 or len(plaka) > 9:
        return False, "Plaka (boşluksuz) 7-9 karakter arasında olmalıdır."

    # 3. İL KODU KONTROLÜ (TİP):
    # Plakanın ilk iki karakteri mutlaka rakam olmalıdır (Örn: '34'IST...)
    if not plaka[0:2].isdigit():
        return False, "Plakanın ilk iki karakteri sayı (il kodu) olmalıdır."

    # 4. İL KODU KONTROLÜ (ARALIK):
    # Türkiye'de il kodları 01 ile 81 arasındadır.
    try:
        il_kodu = int(plaka[0:2])
        if il_kodu < 1 or il_kodu > 81:
            return False, "Geçersiz il kodu (01-81 arası olmalı)."
    except ValueError:
        return False, "İl kodu okunamadı."

    # 5. SON KARAKTER KONTROLÜ:
    # Standart sivil plakalar genelde rakamla biter.
    if not plaka[-1].isdigit():
        return False, "Plakanın son karakteri rakam olmalıdır."

    # Eğer tüm kontrollerden geçerse:
    return True, "Geçerli"


def metin_kontrol(metin, alan_adi):
    """
    Marka ve Model gibi metin alanlarının mantıklı girilip girilmediğini kontrol eder.
    Örneğin 'Marka' kısmına sadece sayı girilmesini engeller.

    Parametreler:
    - metin: Kontrol edilecek veri (Örn: "Fiat")
    - alan_adi: Hata mesajında kullanılacak başlık (Örn: "Marka")
    """
    metin = metin.strip()  # Gereksiz boşlukları temizle

    # 1. BOŞLUK KONTROLÜ:
    # Kullanıcı tek harf girdiyse veya boş bıraktıysa kabul etme.
    if len(metin) < 2:
        return False, f"{alan_adi} en az 2 karakter olmalıdır."

    # 2. SAYISAL KONTROL:
    # Marka veya Model ismi sadece rakamlardan oluşamaz (Örn: Marka="1234")
    if metin.isdigit():
        return False, f"{alan_adi} sadece rakamlardan oluşamaz."

    return True, "Geçerli"