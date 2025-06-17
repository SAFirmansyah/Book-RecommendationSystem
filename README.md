# Laporan Proyek Machine Learning - Satria Adi Firmansyah
## Project Overview

**Latar Belakang**
Seiring dengan meroketnya eksistensi platform streaming seperti Netflix, YouTube, Spotify, dan sebagainya, komunitas pecinta semakin nampak semakin terlepas dari perhatian. Platform besar yang disebutkan tadi memiliki sistem rekomendasi yang mampu memberikan rekomendasi bagi para penggunanya, dan sistem rekomendasi serupa mampu diaplikasikan untuk buku. Tidak hanya untuk komunitas pembaca, namun juga untuk para penulis muda yang ide kreatifnya tak terjamah oleh khalayak luas. Maka dari itu, dikembangkanlah suatu sistem rekomendasi berbasis **Content-Based Filtering** menggunakan **Cosine Similarity**. Sistem ini bertujuan memberikan rekomendasi yang relevan berdasarkan preferensi pengguna, serta kemiripan antar buku.

Sistem ini memanfaatkan informasi seperti skor rating, penulis, serta bahasa dari tiap karya buku untuk menghasilkan rekomendasi yang personal. Dengan sistem ini, platform streaming buku diharapkan mampu membantu pecinta buku menjumpai lebih banyak buku seperti kesukaan mereka, meningkatkan popularitas buku yang belum terkenal, dan mendukung pertumbuhan komunitas dan bisnis.

## Business Understanding
Proyek ini diharapkan dapat memberi dampak signifikan bagi komunitas pecinta buku dan penulis. Dalam sudut pandang bisnis, diharapkan proyek ini dapat mendongkrak popularitas buku, terutama buku yang berkualitas baik namun belum terlalu populer, yang kemudian berpotensi meningkatkan penjualan buku tersebut. Dalam sudut pandang komunitas pecinta buku, proyek ini dapat membantu komunitas menemukan buku-buku yang *underrated*, 

### Problem Statement
1. Bagaimana mengembangkan algoritma rekomendasi buku yang mudah diimplementasikan namun tetap efektif dalam memberikan hasil yang relevan?
2. Bagaimana membantu kemunitas menemukan buku yang sesuai dengan preferensi mereka?

### Goals
1. Mengembangkan algoritma rekomendasi buku yang efektif memberikan hasil yang relevan
2.Mengimplementasikan content-based filtering agar mudah dan efisien

## Data Understanding
Dalam membangun sistem rekomendasi ini, dataset yang digunakan adalah dataset Goodreads-books oleh Soumik yang didapatkan dari tautan  [berikut](https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks)

Dataset dipilih karena jumlah fitur yang dinilai cukup untuk membangun suatu sistem rekomendasi buku. Seleksi dataset dilakukan setelah melakukan evaluasi terhadap beberapa dataset yang tersedia di Kaggle.

Terdapat **11123** baris data, dengan 11 kolom. Menurut informasi dari sumber data, berikut adalah detail dari isi tiap kolom:

1. `bookID`: Identifikasi unik tiap buku
2. `title`: Judul dari tiap buku
3. `authors`: Penulis dari tiap buku. Pada beberapa baris data, terdapat lebih dari dua penulis buku.
4. `isbn`: Nomor ISBN tiap buku, mirip seperti bookID, namun lebih seperti nomor serial.
5. `isbn13`: Nomor ISBN, namun dalam 13 digit
6. `language_code`: Bahasa dari karya buku yang dituliskan.
7. `num_pages`: Jumlah halaman dari tiap buku
8. `ratings_count`: Jumlah rating yang diterima tiap buku
9. `text_reviews_count`: Jumlah review dalam bentuk teks yang diterima tiap buku
10. `publication_date`: Tanggal terbitnya tiap buku
11. `publisher`: Penerbit buku

## Data Preparation
1. Mengubah tipe data dari fitur `publication_date` menjadi `datetime`
2. Menghapus baris yang memiliki kolom bernilai `null`, yaitu di kolom `publication_date` 
3. Mengubah isi kolom `authors` menjadi bentuk list dengan separator '/'
4. Lakukan penskalaan dengan MinMaxScaler ke fitur `average_rating`
5. Lakukan encoding dengan LabelEncode ke fitur `language_code`
6. Lakukan konversi dengan MultiLabelBinarizer ke fitur `authors`
7. Persiapkan matriks fitur. Matriks fitur berisikan fitur `authors`, `avergae_rating`, dan `language_code` yang sudah di encode. 

## Modelling
### Content-Based Filtering
-  Menggunakan **Cosine Similarity** untuk menghitung kesamaan antar anime berdasarkan fitur-fitur utama.
- Memberikan rekomendasi berdasarkan skor kesamaan tertinggi..

### Cosine-Similarity
- Kesamaan antar buku dihitung menggunakan **Cosine Similarity**, yang mengukur kesamaan antar vektor berdasarkan sudut kosinus di antara keduanya.
- Memberikan rekomendasi berdasarkan skor kesamaan tertinggi.

Cosine Similarity adalah algoritma yang mengukur kesamaan antar vektor berdasarkan sudut kosinus di antara keduanya. Vektor ini, adalah berupa vektor matriks fitur yang sudah dibuat sebelumnya
Alasan menggunakan **Cosine Similarity** adalah, **Cosine Similarity** efektif untuk menangkap hubungan antar fitur numerik dan biner. Tidak terpengaruh oleh besaran fitur, sehingga cocok untuk data yang telah dinormalisasi.

### Top-N Recommendation
Berikut adalah hasil Top 10 Reocmmendation, berdasarkan buku **The Road to Dune**.
| title | average_rating | language_code | authors |
|---|---|---|---|
| The Battle Of Corrin (Legends of Dune #3) | 3.74 | eng | (Brian Herbert, Kevin J. Anderson) |
| House Corrino (Prelude to Dune #3) | 3.68 | eng | (Brian Herbert, Kevin J. Anderson) |
| House Harkonnen (Prelude to Dune #2) | 3.67 | eng | (Brian Herbert, Kevin J. Anderson) |
| Hunters of Dune (Dune Chronicles #7) | 3.65 | eng | (Brian Herbert, Kevin J. Anderson) |
| Sandworms of Dune (Dune Chronicles #8) | 3.64 | eng | (Doug Stanton,) |
| Dune Messiah (Dune Chronicles #2) | 3.88 | eng | (Frank Herbert,) |
| Heretics of Dune (Dune Chronicles #5) | 3.86 | eng | (Frank Herbert,) |
| Heretics of Dune (Dune Chronicles #5) | 3.86 | eng | (Frank Herbert,) |
| Chapterhouse: Dune (Dune Chronicles #6) | 3.91 | eng | (Frank Herbert,) |
| God Emperor of Dune (Dune Chronicles #4) | 3.84 | eng | (Frank Herbert,) |

Terlihat sistem rekomendasi berhasil memberikan 10 rekomendasi buku yang sesuai dan mirip dengan buku **The Road to Dune**. Bisa diperhatikan, beberapa kesamaan yang terlihat adalah dari skor yang sama, penulis yang sama, serta bahasa karya yang sama.

## Evaluasi
### 1. **Precision**
**Precision** mengukur proporsi rekomendasi yang relevan terhadap total rekomendasi:

Precision = Jumlah Rekomendasi Relevan/Jumlah Total Rekomendasi

Sistem menghasilkan **Precision = 1.00** untuk berdasarkan bahasa karya, dan **Precision = 0.90**, untuk berdasarkan penulis. Berarti semua rekomendasi sesuai dengan preferensi pengguna. Contoh, untuk anime *The Road to Dune*:
- 10/10 rekomendasi memiliki bahasa serupaa.
- 9/10 rekomendasi datang dari penulis serupa.
- Rekomendasi yang disajikan memiliki skor rating yang tidak terpaut jauh dari **The Road to Dune**

#### Kaitan dengan Problem Statements:
1. **Membantu komunitas menemukan buku yang sesuai dengan preferensi mereka:**  
   Precision tinggi menunjukkan sistem berhasil memberikan rekomendasi relevan berdasarkan fitur utama seperti bahasa, skor, dan penulis.
2. **Merancang sistem rekomendasi yang mudah diimplementasikan:**  
   Pendekatan berbasis *Content-Based Filtering* terbukti sederhana namun tetap memberikan hasil akurat.

---

### 2. **Dampak Evaluasi terhadap Goals**

-  Goal 1: **Mengimplementasikan content-based filtering agar mudah dan efisien**  
Sistem menggunakan fitur dasar seperti bahasa karya, penulis, dan skor rating untuk memberikan rekomendasi yang relevan tanpa memerlukan data kompleks, seperti riwayat pengguna.

- Goal 2: **Menggunakan pendekatan dasar seperti content-based filtering**  
Pendekatan ini mudah diimplementasikan karena hanya memerlukan perhitungan *Cosine Similarity* pada matriks fitur sederhana, yang memastikan efisiensi dalam integrasi dengan platform.

---

### 3. **Dampak Bisnis**

1. **Efisiensi Implementasi:**  
   Sistem berbasis *Content-Based Filtering* mudah diintegrasikan dengan platform tanpa memerlukan data tambahan yang kompleks.
2. **Ketercapaian Goals:**  
   Sistem memenuhi tujuannya untuk memberikan solusi sederhana, relevan, dan efisien dalam membantu komunitas pecinta buku menemuka buku buku baru sesuai prefrensi mereka.
3. **Potensi Peningkatan Popularitas**
    Dengan adanya sistem ini, buku yang sebelumnya tidak terlalu populer namun sebenearnya berkualitas baik, mampu terdongkrak popularitasnya dan penjualannya.

## Kesimpulan

Sistem rekomendasi berbasis *Content-Based Filtering* ini:
1. Membantu komunitas menemukan buku yang sesuai dengan preferensi mereka.
2. Mudah diimplementasikan dan relevan dengan tujuan bisnis.
3. Memberikan hasil evaluasi yang sangat baik (**Precision = 0.90 - 1.00**), menunjukkan sistem efektif dan efisien.

Sistem ini dapat diandalkan dan berpotensi dikembangkan lebih lanjut dengan fitur tambahan seperti *community feedback* atau integrasi hybrid filtering.
