
# 🎮 CapMan

CapMan, Pygame Zero kullanılarak Python diliyle geliştirilmiş, retro esintili bir mini arcade oyunudur.  
Oyuncu, düşman tanklara karşı reflekslerini kullanarak mücadele eder ve mümkün olduğunca uzun süre hayatta kalmaya çalışır.

---

## 🚀 Nasıl Oynanır?

- ← / → tuşları: Karakteri sağa ve sola hareket ettirir.  
- Boşluk (Space): Mermi fırlatır.  
- Start Game butonuna basarak oyunu başlatabilirsin.  
- Düşman tanklara mermi isabet ettirerek yok edebilirsin:
  - 🪖 Zayıf Tank: 5 mermide yok olur  
  - 🛡️ Güçlü Tank: 10 mermide yok olur  
- Eğer tank sana çarparsa... **Game Over!**  
  Ekranda yanıp sönen "GAME OVER" yazısı belirir ve game_over müziği çalar.

---

## 🖼️ Ekran Görüntüsü

> Oyun menüsü, karakter, düşman tanklar ve ses efektleri ile zenginleştirilmiştir.  
> Görseller `images/`, sesler ise `sounds/` klasöründe yer almaktadır.

---

## 📁 Proje Yapısı

CapMan/  
├── images/        # Karakter ve tank görselleri (.png)  
├── sounds/        # Oyun müzikleri ve ses efektleri (.wav)  
├── main.py        # Oyun kodlarının bulunduğu dosya  
└── README.md      # Bu açıklama dosyası

---

## 💻 Gerekenler

Bu proje yalnızca aşağıdaki Python modüllerini kullanır:

- `pgzero`  
- `random`  
- `math`  

🚫 **pygame** gibi ek kütüphaneler kullanılmamıştır.

---

## 🔧 Kurulum:

1. Python 3 yüklü değilse [buradan indir](https://www.python.org/downloads/).  
2. Terminal veya Komut İstemcisi aç ve şunu çalıştır:
   ```bash
   pip install pgzero
   ```

---

## 📄 Lisans

Bu proje eğitsel amaçlarla oluşturulmuştur. İzin almadan ticari amaçlarla kullanılması uygun değildir.

---

## 🙋‍♂️ İletişim

Projeyle ilgili öneri veya geri bildiriminiz varsa bana ulaşabilirsiniz:  
📧 [E-mail](mailto:yavuz.colak@live.com)  
💻 [GitHub](https://github.com/yavuzcancolak)  
🔗 [LinkedIn](https://www.linkedin.com/in/yavuzcan-colak)
