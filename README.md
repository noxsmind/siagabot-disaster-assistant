# 🚨 SiagaBot — Asisten AI Tanggap Darurat & Mitigasi Bencana

SiagaBot adalah chatbot berbasis **Large Language Model (Google Gemini)** yang membantu
masyarakat Indonesia mendapatkan panduan keselamatan bencana secara cepat, jelas, dan
mudah dipahami — mulai dari gempa bumi, banjir, kebakaran, hingga pertolongan pertama (P3K).

## 🎯 Use Case
**Domain-specific Assistant Bot — Disaster Preparedness & Emergency Response**

Chatbot ini menyasar skenario:
- Warga yang butuh panduan cepat saat/menjelang situasi darurat (gempa, banjir, kebakaran)
- Edukasi mitigasi (isi tas siaga bencana, rute evakuasi keluarga)
- Panduan P3K dasar sebelum bantuan medis tiba

## 🧠 Model & Teknologi
| Komponen | Detail |
|---|---|
| LLM | Google Gemini (via `langchain-google-genai`) |
| Framework orkestrasi | LangChain (`ChatPromptTemplate`, `MessagesPlaceholder`) |
| Frontend | Streamlit |
| Memory | Riwayat percakapan disimpan di `st.session_state` (context-aware, ingat percakapan sebelumnya dalam satu sesi) |

## 🎨 Parameter Kreatif yang Diterapkan
1. **Gaya bahasa**: Tenang, profesional, empatik, dan sangat instruktif — dirancang untuk
   situasi stres/darurat, bukan gaya santai biasa.
2. **Domain pengetahuan spesifik**: Kebencanaan Indonesia (gempa, banjir, kebakaran, P3K,
   mitigasi pasca-bencana).
3. **Fitur tambahan**:
   - 🧠 **Memory** — bot mengingat konteks percakapan dalam sesi yang sama.
   - ⚡ **Quick Topic Chips** — tombol topik cepat (Gempa, Banjir, Kebakaran, Tas Siaga,
     P3K, Rute Evakuasi) agar pengguna tidak perlu mengetik dari nol.
   - 📞 **Kontak Darurat Nasional** — ditampilkan permanen di sidebar (112, 119, 115, 117, 113, 110).
   - 📝 **Format terstruktur otomatis** — jawaban selalu dalam bentuk poin/numbering + emoji
     kontekstual agar mudah di-scan saat kondisi panik.

## ⚙️ Cara Menjalankan

### 1. Clone repository
\`\`\`bash
git clone https://github.com/noxsmind/siagabot-disaster-assistant.git
cd siagabot-disaster-assistant
\`\`\`

### 2. Install dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Jalankan aplikasi
\`\`\`bash
streamlit run app.py
\`\`\`

Saat aplikasi terbuka, masukkan **Google API Key** (didapat gratis di
[Google AI Studio](https://aistudio.google.com/app/apikey)) pada kolom di sidebar untuk
mengaktifkan chatbot.

## 📁 Struktur Proyek
```
.
├── app.py              # Kode utama chatbot (Streamlit + LangChain + Gemini)
├── requirements.txt    # Daftar dependency
├── README.md           # Dokumentasi ini
```

## 📞 Kontak Darurat Nasional (Indonesia)
| Layanan | Nomor |
|---|---|
| Panggilan Darurat | 112 |
| Ambulans / Kemenkes | 119 |
| Basarnas (SAR) | 115 |
| BNPB | 117 |
| Pemadam Kebakaran | 113 |
| Polisi | 110 |

---
© 2026 SiagaBot — AI Agent Project
