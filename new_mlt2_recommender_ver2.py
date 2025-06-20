# -*- coding: utf-8 -*-
"""New_MLT2_Recommender.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1fT8IsyaLdmBrLEOgaP6VYT0lEZmWkFD2

# Sistem Rekomendasi Buku berbasis *Content-Based Filtering* dengan *Cosine Similarity*

Seiring dengan meroketnya eksistensi platform streaming seperti Netflix, YouTube, Spotify, dan sebagainya, komunitas pecinta semakin nampak semakin terlepas dari perhatian. Platform besar yang disebutkan tadi memiliki sistem rekomendasi yang mampu memberikan rekomendasi bagi para penggunanya, dan sistem rekomendasi serupa mampu diaplikasikan untuk buku. Tidak hanya untuk komunitas pembaca, namun juga untuk para penulis muda yang ide kreatifnya tak terjamah oleh khalayak luas. Maka dari itu, dikembangkanlah suatu sistem rekomendasi berbasis **Content-Based Filtering** menggunakan **Cosine Similarity**. Sistem ini bertujuan memberikan rekomendasi yang relevan berdasarkan preferensi pengguna, serta kemiripan antar buku.

Sistem ini memanfaatkan informasi seperti skor rating, penulis, serta bahasa dari tiap karya buku untuk menghasilkan rekomendasi yang personal. Dengan sistem ini, platform streaming buku diharapkan mampu membantu pecinta buku menjumpai lebih banyak buku seperti kesukaan mereka, meningkatkan popularitas buku yang belum terkenal, dan mendukung pertumbuhan komunitas dan bisnis.

## Import Library yang Dibutuhkan
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import precision_score, recall_score, confusion_matrix
from sklearn.preprocessing import MultiLabelBinarizer,MinMaxScaler, OneHotEncoder, LabelEncoder
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import warnings
import re
warnings.filterwarnings('ignore')

"""## Data Loading & Understanding

### Download Data

Langkah pertama adalah mengunduh data. Namun sebelum mengunduh data, kita perlu mengunggah kredensial akun Kaggle kita sebagai sumber dataset yang kita gunakan, agar kita bisa mengambil data dari Kaggle
"""

from google.colab import files
files.upload()

!pip install kaggle

!mkdir ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

"""Setelah itu, barulah kita bisa mengunduh dan membuka dataset dari Kaggle ini. Dataset didapat dari link [berikut](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)"""

!kaggle datasets download -d jealousleopard/goodreadsbooks

!unzip goodreadsbooks.zip

"""Hanya ada 1 file dalam dataset, yaitu **books.csv**

### Load Data

**Intip isi dataset**
"""

book = pd.read_csv('books.csv', on_bad_lines='skip')
book.head()

"""**Periksa isi dataset, jumlah, serta tipe datanya**"""

book.info()

"""Terdapat **11123** baris data, dengan 11 kolom. Menurut informasi dari sumber data, berikut adalah detail dari isi tiap kolom:

1. `bookID`: Identifikasi unik tiap buku
2. `title`: Judul dari tiap buku
3. `authors`: Penulis dari tiap buku. Pada beberapa baris data, terdapat lebih dari dua penulis buku.
4. `average_rating`: skor rating rerata dari tiap buku
5. `isbn`: Nomor ISBN tiap buku, mirip seperti bookID, namun lebih seperti nomor serial.
6. `isbn13`: Nomor ISBN, namun dalam 13 digit
7. `language_code`: Bahasa dari karya buku yang dituliskan.
8. `num_pages`: Jumlah halaman dari tiap buku
9. `ratings_count`: Jumlah rating yang diterima tiap buku
10. `text_reviews_count`: Jumlah review dalam bentuk teks yang diterima tiap buku
11. `publication_date`: Tanggal terbitnya tiap buku
12. `publisher`: Penerbit buku

Jika diperhatikan, `publication_date` masih dalam tipe data yang keliru. Sebelumnya, kita ubah dahulu ke format `datetime`
"""

book['publication_date'] = pd.to_datetime(book['publication_date'], errors = 'coerce')
book['publication_date'].info()

"""### Pemeriksaan Data *Null* dan *Duplicate*

Selanjutnya, kita periksa baris yang bervalue *null*

Proses pengecekan nilai yang hilang dibutuhkan agar mengetahui berapa banyak jumlah nilai yang tidak ada di dalam dataset, hal ini berfungsi sebagai langkah awal dalam melakukan pembersihan data (data cleaning). Dengan mengetahui jumlah nilai yang hilang, kita dapat memutuskan langkah selanjutnya, seperti:

- Menghapus baris atau kolom yang memiliki nilai yang hilang jika jumlahnya sangat besar dan tidak relevan dengan analisis.
- Mengisi nilai yang hilang dengan nilai pengganti seperti rata-rata (mean), median, modus, atau menggunakan teknik imputasi lain yang sesuai dengan jenis data dan tujuan analisis.
- Menangani nilai yang hilang secara selektif berdasarkan pentingnya kolom atau baris tertentu, terutama jika data tersebut diperlukan untuk model prediksi.
"""

book.isnull().sum()

"""Ada dua baris dengan value *null* di `publication_date`. Karena sangat sedikit, kita bisa hapus saja baris tersebut.

Namun sebelumnya, kita periksa dulu apakah ada value yang duplikat.
"""

book.duplicated().sum()

"""Ternyata tidak ada value duplikat. Maka, kita bisa lanjut ke menghapus value yang null tadi."""

book.dropna(inplace=True)
book.isnull().sum()

"""Sudah tidak ada value yang *null*

### Exploratory Data Analysis

Kita coba lihat statistika dari data numerikal yang ada.
"""

book.describe()

"""**Melihat distribusi rating buku**

Pengecekan distribusi rating buku penting untuk memahami bagaimana pengguna memberikan penilaian, mendeteksi bias atau ketidakseimbangan dalam penilaian, serta menemukan outliers yang dapat memengaruhi akurasi sistem rekomendasi.
"""

book['average_rating'].value_counts()

plt.figure(figsize=(10, 6))
book['average_rating'].astype(float).plot(kind='hist', bins=20, edgecolor='black')
plt.title('Distribusi Rating Buku')
plt.xlabel('Skor rating')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

"""Data Skor rating memiliki **Distribusi Normal**, dalam grafik diatas, skor buku yang paling banyak berada di antara skor antara 3.5 hingga 4.5. Banyak buku yang mendapatkan skor di atas rerata yaitu 3.93

**Melihat Distribusi jumlah karya buku berdasarkan Penulis**

Pengecekan distribusi jumlah karya buku berdasarkan penulis penting untuk melihat seberapa banyak jumlah penulis yang ada dalam dataset, serta jumlah karyanya masing-masing.
"""

book['authors'].value_counts()

"""Karena ada terlalu banyak penulis dalam dataset, serta adanya 2 hingga 3 penulis dalam satu karya, maka dipisahkan terlebih dahulu kolom penulis ini ke dalam bentuk list. Kemudian, kita bisa lihat lebih jelas distribusinya dengan mengambil 50 penulis dengan karya terbanyak."""

from collections import Counter
author_list = book['authors'].dropna().str.split('/').sum()
author_counts = Counter(author_list).most_common(50)
author, counts = zip(*author_counts)
plt.figure(figsize=(10, 6))
plt.bar(author, counts)
plt.title("Top 50 Penulis")
plt.xlabel("Penulis")
plt.ylabel("Frequency")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

"""**Melihat Distribusi jumlah karya buku berdasarkan Penerbit**

Pengecekan distribusi jumlah karya buku berdasarkan penulis penting untuk melihat seberapa banyak jumlah penerbit yang ada dalam dataset, serta jumlah karya yang diterbitkan oleh tiap penerbit.
"""

book['publisher'].value_counts()

"""Mirip seperti jumlah penulis yang terlalu banyak, maka kita ambil 50 penerbit dengan karya terbitan terbanyak."""

plt.figure(figsize=(10, 6))
book['publisher'].value_counts().head(50).plot(kind='bar')
plt.title('Top 50 Penerbit berdasarkan Karya')
plt.xlabel('Penerbit')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

"""**Melihat Distribusi jumlah karya buku berdasarkan Bahasa Karya**

Pengecekan distribusi jumlah karya buku berdasarkan Bahasa penting untuk melihat seberapa banyak Bahasa buku yang ada dalam dataset, serta jumlah bahasa dari karya yang diterbitkan.
"""

book['language_code'].value_counts()

plt.figure(figsize=(10, 6))
book['language_code'].value_counts().plot(kind='bar')
plt.title('Distribusi Bahasa Karya')
plt.xlabel('Bahasa')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

"""Berbeda dari yang lain, jumlah bahasa karya tidak terlalu banyak, jadi kita bisa plot distribusinya semua. Bisa dilihat, mayoritas bahasa hasil karya ada dalam bahasa Inggris UK, bahasa Inggris USA, serta bahasa Spanyol.

## Data Preparation

Data hilang sudah dibersihkan di awal, namun masih diperlukan pemisahan nama dalam karya yang ditulis oleh lebih dari satu orang.

Maka dari itu, dilakukanlah pemisahan nama ini menjadi dalam bentuk list, dari isi yang awalnya diberi separator '/'
"""

book['authors'] = book['authors'].str.split('/')
book.head(5)

"""Setelah itu, dilakukan penskalaan skor rating karya buku dengan MinMax Scaler"""

mmscaler = MinMaxScaler()

book['average_rating'] = mmscaler.fit_transform(book[['average_rating']])
book.head(5)

"""Setelah itu, dilakukanlah LabelEncode terhadap data `language_code`"""

le = LabelEncoder()
language_encoded = le.fit_transform(book[['language_code']])
book.head(5)

"""Terakhir, menggunakan **MultiLabelBinarizer** untuk mengonversi data penulis buku yang berupa list menjadi format biner yang dapat digunakan untuk analisa lebih lanjut"""

mlb = MultiLabelBinarizer()
authors_encoded = mlb.fit_transform(book['authors'])

print(mlb.classes_)
print(authors_encoded[:5])

"""Setelah persiapan data selesai, dilakukanlah langkah terakhir yaitu penggabungan fitur-fitur tertentu menjadi fitur yang digunakan untuk menghasilkan rekomendasi."""

average_rating_2d = book['average_rating'].values.reshape(-1, 1)
language_encoded_2d = language_encoded.reshape(-1, 1)

fitur_matriks = np.hstack(
    [authors_encoded, language_encoded_2d, average_rating_2d]
)

print(fitur_matriks[:5])

"""## Modelling

Setelah fitur Matriks sudah mencakup berbagai informasi yang dapat digunakan, langkah selanjutnya adalah menghitung cosine similarity antar buku.
"""

# Menghitung Cosine Similarity dari matrix fitur
combined_similarity = cosine_similarity(fitur_matriks)

print(combined_similarity[:5])

"""Fungsi berikut dibuat agar bisa mencari rekomendasi berdasarkan fitur-fitur dalam matriks, dan sesuai yang ada dalam judul buku yang dicari."""

def recommend_books_multi_feature(book_name, top_n=10):
  index = book[book['title'] == book_name].index[0]

  similarity_scores = list(enumerate(combined_similarity[index]))
  similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
  similar_book_indices = [i[0] for i in similarity_scores[1:top_n+1]]
  return book.iloc[similar_book_indices][['title', 'average_rating', 'language_code', 'authors']]

"""## Mencari Top - N Rekomendasi

"""

multi_feature_recommended_book = recommend_books_multi_feature("The Road to Dune", top_n=10)

similar_book_indices = multi_feature_recommended_book.index

normalized_ratings = multi_feature_recommended_book[['average_rating']].values
normalized_authors = multi_feature_recommended_book['authors'].values
normalized_language = multi_feature_recommended_book['language_code'].values

# Apply the inverse transform to get original ratings
original_ratings = mmscaler.inverse_transform(normalized_ratings).flatten()
original_authors = mlb.inverse_transform(authors_encoded[similar_book_indices])
original_language = le.inverse_transform(language_encoded[similar_book_indices])

# Update the 'average_rating' column in the DataFrame with the original values
multi_feature_recommended_book['average_rating'] = original_ratings
multi_feature_recommended_book['authors'] = original_authors
multi_feature_recommended_book['language_code'] = original_language

from IPython.display import display
display(multi_feature_recommended_book)

"""Terlihat sistem rekomendasi berhasil memberikan 10 rekomendasi buku yang sesuai dan mirip dengan buku **The Road to Dune**. Bisa diperhatikan, beberapa kesamaan yang terlihat adalah dari skor yang sama, penulis yang sama, serta bahasa karya yang sama.

## Metrik Evaluasi

Dalam Sistem Rekomendasi ini, Evaluasi akan dilakukan berdasarkan data tipe yang dihasilkan dari sistem rekomendasi menggunakan metrik tertentu

#### Precision
1. **Precision**  
   Mengukur proporsi dari anime yang direkomendasikan yang relevan berdasarkan ground truth.

   $$
   \text{Precision} = \frac{\text{Jumlah rekomendasi yang relevan}}{\text{Jumlah total rekomendasi}}
   $$


Berikut adalah blok kode untuk mencari nilai Precision
"""

def calculate_precision(input_book_name, recommended_books_df):
  # Get the features of the input book
  input_book = book[book['title'] == input_book_name].iloc[0]
  input_authors = set([author.strip() for sublist in input_book['authors'] for author in (sublist.split('/') if isinstance(sublist, str) else sublist)])
  input_language = input_book['language_code']
  input_rating = input_book['average_rating']

  relevant_count = 0
  total_recommendations = len(recommended_books_df)

  # Iterate through recommended books to check for relevance
  for index, row in recommended_books_df.iterrows():
    recommended_authors = set([author.strip() for sublist in row['authors'] for author in (sublist.split('/') if isinstance(sublist, str) else sublist)])
    recommended_language = row['language_code']
    recommended_rating = row['average_rating']

    # Define relevance: shares an author or has the same language
    if input_authors.intersection(recommended_authors) or input_language == recommended_language:
       relevant_count += 1

  precision = relevant_count / total_recommendations if total_recommendations > 0 else 0
  return precision

# Get recommendations for a book
input_book_title = "The Road to Dune"
recommended_books = recommend_books_multi_feature(input_book_title, top_n=10)

# Calculate and print precision
precision_score = calculate_precision(input_book_title, recommended_books)
print(f"Precision for '{input_book_title}': {precision_score:.2f}")

"""Adapun untuk buku yang ingin dicari rekomendasinya, **The Road to Dune** ditulis oleh Frank Herbert, Brian Herbert, dan Kevin J. Anderson. Memiliki skor rating 3,88 dan berbahasa Inggris. Presisi yang didapatkan adalah (10/10) =  1, atau 100% Presisi, karena sistem berhasil memberikan rekomendasi yang relevan terhadap buku."""

