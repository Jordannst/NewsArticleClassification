# 📰 Project: Klasifikasi Berita Menggunakan Model Naive Bayes

Proyek ini bertujuan untuk membangun model klasifikasi teks yang dapat memprediksi kategori berita berdasarkan konten teks menggunakan **Multinomial Naive Bayes**.

## 🔍 Langkah-Langkah

1. **Pengumpulan Data**  
   Dataset berita dibaca dari file CSV untuk kategori seperti:
   - Business
   - Education
   - Entertainment
   - Sports
   - Technology

2. **Preprocessing Teks**  
   Teks dibersihkan dengan tahapan berikut:
   - Menghapus tag HTML dan URL
   - Tokenisasi dan konversi huruf kecil
   - Menghapus stopwords, angka, dan tanda baca
   - Stemming menggunakan *PorterStemmer*

3. **Transformasi Teks**  
   Teks diubah menjadi representasi numerik menggunakan **TF-IDF (Term Frequency-Inverse Document Frequency)** untuk mengukur pentingnya kata dalam dokumen.

4. **Pelatihan Model**  
   Model klasifikasi dibangun menggunakan algoritma **Multinomial Naive Bayes** yang dilatih dengan data teks yang telah diproses.

5. **Evaluasi Model**  
   Kinerja model dievaluasi menggunakan metrik:
   - Accuracy
   - Precision (Macro)
   - Recall (Macro)
   - F1 Score (Macro)  
   Selain itu, **confusion matrix** divisualisasikan untuk memeriksa distribusi kesalahan klasifikasi.

6. **Prediksi Kategori Berita**  
   Model digunakan untuk memprediksi kategori berita berdasarkan teks input pengguna. Jika teks berbahasa Indonesia, akan diterjemahkan ke bahasa Inggris terlebih dahulu sebelum diprediksi.

## 🧰 Tools dan Library yang Digunakan

- [Python](https://www.python.org/)
- [Pandas](https://pandas.pydata.org/)
- [Scikit-learn](https://scikit-learn.org/)
- [NLTK](https://www.nltk.org/)
- [Seaborn](https://seaborn.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
- [TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [MultinomialNB](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html)
- [Joblib](https://joblib.readthedocs.io/en/latest/)

---

🎯 **Tujuan akhir proyek ini** adalah menciptakan sistem yang dapat secara otomatis mengklasifikasikan berita ke dalam kategori yang sesuai berdasarkan isi teks.
