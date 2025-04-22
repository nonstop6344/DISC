import tkinter as tk
from tkinter import ttk, messagebox
from jinja2 import Template
from weasyprint import HTML
import tempfile
import os
from datetime import datetime

# ------------------ SORULAR ------------------ #
SORULAR = [
    {"soru": "1. Aşağıdakilerden hangisi sizi en iyi tanımlar?", "secenekler": ["Kararlı", "Eğlenceli", "Sabırlı", "Dikkatli"]},
    {"soru": "2. Baskı altında nasıl davranırsınız?", "secenekler": ["Hızlı karar alırım", "Mizah yaparım", "Sakin kalırım", "Analiz ederim"]},
    {"soru": "3. Bir ekipte hangi rol size daha uygundur?", "secenekler": ["Liderlik", "Motivasyon", "Destek", "Planlama"]},
    {"soru": "4. İş yerinde başarıyı ne belirler?", "secenekler": ["Sonuçlar", "İlişkiler", "İstikrar", "Kurallar"]},
    {"soru": "5. Yeni bir işe başladığınızda ne yaparsınız?", "secenekler": ["Hemen sorumluluk alırım", "Herkesle tanışırım", "Ortamı gözlemlerim", "Kuralları öğrenirim"]},
    {"soru": "6. Zor kararlar alırken neye odaklanırsınız?", "secenekler": ["Sonuç", "İnsanlar", "Uyum", "Veri"]},
    {"soru": "7. İletişim tarzınız nasıldır?", "secenekler": ["Direkt", "Canlı", "Sakin", "Düşünceli"]},
    {"soru": "8. Takım arkadaşınızın sizden en çok beklediği nedir?", "secenekler": ["Hedefe ulaşmak", "Moral vermek", "Sadakat", "Titizlik"]},
    {"soru": "9. Sizi ne motive eder?", "secenekler": ["Başarı", "Sosyal çevre", "Güvence", "Kalite"]},
    {"soru": "10. Kriz anlarında nasıl davranırsınız?", "secenekler": ["Yönlendiririm", "Morali yüksek tutarım", "Destek olurum", "Strateji kurarım"]},
    {"soru": "11. Hedeflerinize ulaşmak için ne yaparsınız?", "secenekler": ["Risk alırım", "İkna ederim", "Destek isterim", "Plan yaparım"]},
    {"soru": "12. Yeni fikirleri nasıl karşılarsınız?", "secenekler": ["Uygulamak isterim", "Paylaşırım", "Düşünürüm", "Sorgularım"]},
    {"soru": "13. Ne tür ortamlarda verimli çalışırsınız?", "secenekler": ["Hızlı ve dinamik", "Eğlenceli", "Sakin", "Düzenli"]},
    {"soru": "14. İş yerinde sizi ne rahatsız eder?", "secenekler": ["Yavaşlık", "Soğuk ortam", "Gerginlik", "Belirsizlik"]},
    {"soru": "15. Bir projeye nasıl yaklaşırsınız?", "secenekler": ["Hemen başlarım", "Destek toplarım", "Uyum sağlarım", "Araştırırım"]},
    {"soru": "16. Eleştiri aldığınızda ne yaparsınız?", "secenekler": ["Kabul ederim", "Savunurum", "Üzülürüm", "Değerlendiririm"]},
    {"soru": "17. İdeal yöneticiniz nasıl biri olmalı?", "secenekler": ["Kararlı", "İlham verici", "Destekleyici", "Organize"]},
    {"soru": "18. Gününüzü nasıl planlarsınız?", "secenekler": ["Hedef odaklı", "Doğal akışta", "İnsanlarla birlikte", "Listelerle"]},
    {"soru": "19. Başarıyı neye borçlusunuz?", "secenekler": ["İrade", "İletişim", "Sadakat", "Disiplin"]},
    {"soru": "20. Sizi en çok ne tatmin eder?", "secenekler": ["Zafer", "Takdir", "İlişkiler", "Doğruluk"]},
]

SECENEK_TIPLERI = ["D", "I", "S", "C"]

# ------------------ UYGULAMA ------------------ #
class KisilikTesti:
    def __init__(self, root):
        self.root = root
        self.root.title("DiSC Kişilik Testi")
        self.root.geometry("550x450")
        self.root.configure(bg="#e0f7fa")
        self.index = 0
        self.puanlar = {"D": 0, "I": 0, "S": 0, "C": 0}
        self.kullanici = {}
        self.cevaplar = []
        self.giris_ekrani()

    def giris_ekrani(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="DiSC Kişilik Testi", font=("Helvetica", 20, "bold"), bg="#e0f7fa", fg="#00796b").pack(pady=10)

        form_frame = tk.Frame(self.root, bg="#e0f7fa")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Ad Soyad:", bg="#e0f7fa").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.ad_entry = tk.Entry(form_frame, width=30)
        self.ad_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Doğum Yılı:", bg="#e0f7fa").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.yil_var = tk.StringVar()
        self.yil_combo = ttk.Combobox(form_frame, textvariable=self.yil_var, values=[str(y) for y in range(1950, datetime.now().year + 1)], state="readonly")
        self.yil_combo.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Cinsiyet:", bg="#e0f7fa").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.cinsiyet_var = tk.StringVar()
        self.cinsiyet_combo = ttk.Combobox(form_frame, textvariable=self.cinsiyet_var, values=["Kadın", "Erkek", "Diğer"], state="readonly")
        self.cinsiyet_combo.grid(row=2, column=1, pady=5)

        ttk.Style().configure("TButton", font=("Helvetica", 12))
        ttk.Button(self.root, text="Teste Başla", command=self.sorulara_basla).pack(pady=20)

    def sorulara_basla(self):
        ad = self.ad_entry.get().strip()
        yil = self.yil_var.get()
        cinsiyet = self.cinsiyet_var.get()

        if not ad or not yil or not cinsiyet:
            messagebox.showwarning("Eksik Bilgi", "Lütfen tüm alanları doldurun.")
            return

        self.kullanici = {"ad": ad, "yil": yil, "cinsiyet": cinsiyet}
        self.soru_ekrani()

    def soru_ekrani(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.soru_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#e0f7fa")
        self.soru_label.pack(pady=10)

        self.secenek_var = tk.StringVar()
        self.secenekler = []
        for i in range(4):
            rb = tk.Radiobutton(self.root, text="", variable=self.secenek_var, value="", font=("Arial", 12), bg="#e0f7fa")
            rb.pack(anchor="w", padx=20)
            self.secenekler.append(rb)

        self.ileri_button = tk.Button(self.root, text="İleri", command=self.sonraki_soru)
        self.ileri_button.pack(pady=20)

        self.guncelle()

    def guncelle(self):
        soru = SORULAR[self.index]
        self.soru_label.config(text=soru["soru"])
        self.secenek_var.set(None)
        for i, secenek in enumerate(soru["secenekler"]):
            self.secenekler[i].config(text=secenek, value=secenek)

    def sonraki_soru(self):
        secim = self.secenek_var.get()
        if not secim:
            messagebox.showwarning("Uyarı", "Lütfen bir seçenek seçin.")
            return
        secenek_index = SORULAR[self.index]["secenekler"].index(secim)
        secenek_tipi = SECENEK_TIPLERI[secenek_index]
        self.puanlar[secenek_tipi] += 1
        self.index += 1
        if self.index < len(SORULAR):
            self.guncelle()
        else:
            self.rapor_ekrani()

    def rapor_ekrani(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Kişilik analiz testiniz bitmiştir.", font=("Arial", 14), bg="#e0f7fa").pack(pady=20)
        tk.Label(self.root, text="Sonuçları görmek için PDF'e kaydet butonuna basınız.", font=("Arial", 12), bg="#e0f7fa").pack(pady=10)
        tk.Button(self.root, text="PDF'e Kaydet", command=self.raporu_kaydet).pack(pady=20)

    def raporu_kaydet(self):
        with open("report_template_piechart.html", "r", encoding="utf-8") as f:
            template = Template(f.read())

        veri = self.puanlar.copy()
        veri.update(self.kullanici)

        html_icerik = template.render(**veri)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            HTML(string=html_icerik).write_pdf(tmp_pdf.name)
            os.startfile(tmp_pdf.name)

# ------------------ BAŞLAT ------------------ #
if __name__ == "__main__":
    root = tk.Tk()
    app = KisilikTesti(root)
    root.mainloop()