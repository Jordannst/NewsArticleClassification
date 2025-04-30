from flask import Flask, render_template, request  # Flask untuk membuat aplikasi web
import joblib  # Ganti pickle dengan joblib untuk memuat model
import re  # Untuk manipulasi teks menggunakan ekspresi reguler
import google.generativeai as genai  # Library untuk API Gemini generative AI
import nltk  # Library untuk pemrosesan bahasa alami
import string  # Untuk manipulasi string
from nltk.corpus import stopwords  # Stopwords untuk membuang kata-kata umum yang tidak relevan
from nltk.stem import PorterStemmer
from deep_translator import GoogleTranslator  # Library untuk menerjemahkan teks antar bahasa
from langdetect import detect  # Library untuk mendeteksi bahasa teks


# Inisialisasi Flask
app = Flask(__name__)

# Load model klasifikasi berita dari file yang telah disimpan sebelumnya menggunakan joblib
with open('model/news_classifier_model.pkl', 'rb') as f:
    model = joblib.load(f)  # Model klasifikasi berita

# Load vectorizer TF-IDF dari file menggunakan joblib
with open('model/tfidf_vectorizer.pkl', 'rb') as f:
    tfidf = joblib.load(f)  # TF-IDF vectorizer

# Konfigurasi API Gemini dengan API key
genai.configure(api_key="GEMINI_API_KEY") 
gemini_model = genai.GenerativeModel("gemini-1.5-flash")  # Memilih model generatif Gemini versi 1.5

# Daftar kategori berita yang tersedia
categories = ['BUSINESS', 'EDUCATION', 'ENTERTAIMENT', 'SPORTS', 'TECHNOLOGY']  # Daftar kategori berita
category_map = {0: 'BUSINESS', 1: 'EDUCATION', 2: 'ENTERTAIMENT', 3: 'SPORTS', 4: 'TECHNOLOGY'} # Daftar kategori berita}  # Peta kategori

# Mengunduh daftar stopwords (kata-kata umum) bahasa Inggris
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Fungsi untuk membersihkan teks

# Pastikan download stopwords terlebih dahulu
nltk.download("stopwords")

def clean_text(text):
    # Remove HTML tags
    html = re.compile('<.*?>')
    text = html.sub('', text)
    
    # Remove URLs
    url = re.compile(r'https?://\S+|www\.\S+')
    text = url.sub(r'', text)
    
    # Tokenize text into words
    token = re.findall("[\w']+", text)
    
    # Convert words to lowercase
    token = [word.lower() for word in token]
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    token = [word for word in token if word.lower() not in stop_words]
    
    # Remove punctuation
    token = [''.join(char for char in word if char not in string.punctuation) for word in token]
    
    # Remove numbers
    token = [''.join(char for char in word if char not in string.digits) for word in token if word]
    
    # Apply stemming
    porter_stemmer = PorterStemmer()
    token = [porter_stemmer.stem(word) for word in token]
    
    # Join words back into a sentence
    cleaned_text = ' '.join(token)
    
    return cleaned_text


# Fungsi untuk menerjemahkan teks ke bahasa Inggris
def translate_to_english(text):
    try:
        return GoogleTranslator(source='id', target='en').translate(text)  # Terjemahkan dari Indonesia ke Inggris
    except Exception as e:
        print("Translation error:", e)  # Log error jika terjadi
        return text  # Kembalikan teks asli jika gagal

# Fungsi untuk menangani deteksi dan terjemahan bahasa
def handle_language(text_input):
    try:
        detected_lang = detect(text_input)  # Deteksi bahasa teks
        if detected_lang == 'id':  # Jika bahasa adalah Indonesia
            print("Detected Indonesian, translating to English...")
            return translate_to_english(text_input)  # Terjemahkan ke Inggris
    except:
        pass  # Abaikan error
    return text_input  # Kembalikan teks asli jika bukan Indonesia

# Fungsi untuk mendapatkan kategori berita menggunakan API Gemini
def get_news_categories_with_gemini(text, temperature=0.7, max_categories=3):
    cleaned_text = clean_text(text)  # Membersihkan teks
    category_list = ", ".join(categories)  # Gabungkan daftar kategori sebagai string

    # Membuat prompt untuk AI Gemini
    prompt = f"""
    Tentukan hingga {max_categories} kategori yang paling relevan untuk teks berita berikut ini. Pilih kategori dari daftar berikut:
    {category_list}

    Jawabanmu harus berupa satu hingga tiga kategori dari daftar di atas, dipisahkan dengan koma.

    Berita:
    \"{cleaned_text}\" 
    """

    # Menggunakan model generatif Gemini untuk mendapatkan kategori
    response = gemini_model.generate_content(prompt, generation_config={"temperature": temperature})
    predicted_categories = response.text.strip().split(",")  # Memisahkan hasil kategori yang dihasilkan
    predicted_categories = [category.strip().upper() for category in predicted_categories]  # Bersihkan dan ubah ke huruf besar
    return predicted_categories[:max_categories]  # Kembalikan hingga maksimal 3 kategori

# Route utama untuk aplikasi web
@app.route('/', methods=['GET', 'POST'])
def index():
    predicted_categories = None  # Variabel untuk menyimpan kategori hasil prediksi

    if request.method == 'POST': 
        text_input = request.form['news_description']  # Ambil input teks dari form
        method = request.form['method']  # Ambil metode prediksi dari form

        if method == 'tfidf': 
            text_translated = handle_language(text_input)  # Deteksi dan terjemahkan jika perlu
            cleaned_text = clean_text(text_translated)  # Bersihkan teks
            vectorized_text = tfidf.transform([cleaned_text])  # Transformasi teks menggunakan TF-IDF vectorizer
            predicted_category_index = model.predict(vectorized_text)[0]  # Prediksi kategori dengan model (dalam angka)
            predicted_category = category_map.get(predicted_category_index, 'Unknown')  # Map angka ke kategori
            predicted_categories = [predicted_category]  # Simpan hasil prediksi

        elif method == 'gemini':  
            predicted_categories = get_news_categories_with_gemini(text_input)  # Prediksi dengan Gemini

        return render_template('index.html', predicted_categories=predicted_categories, input_text=text_input)  # Render hasil

    return render_template('index.html', predicted_categories=None)  # Render halaman awal

# Menjalankan aplikasi Flask
if __name__ == '__main__':
    app.run(debug=True)  # Jalankan aplikasi dengan debug mode
