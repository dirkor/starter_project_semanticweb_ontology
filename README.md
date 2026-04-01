# Starter Project Semantic Web and Ontology Topic

This is a starter project for the Ontology and Semantic Web Topic in the Special Topics in Informatics course in the Informatics Engineering Study Program, Sam Ratulangi University.

Topic by: Dirko G. S. Ruindungan, S.T., M.Eng.

This app read `.owl` file from Protégé.

[Download Protégé](https://protege.stanford.edu/software.php#desktop-protege) (Gunakan Versi Terakhir / 5.5.0 / 5.0.0 / 4.3)

## Fitur
1. Cari mata kuliah berdasarkan dosen
2. Lihat prasyarat mata kuliah (langsung)
3. **✨ Lihat prasyarat hasil penalaran / Inferred (langsung & tidak langsung)**
4. Lihat daftar mata kuliah berdasarkan semester
5. Menampilkan query SPARQL yang dijalankan

## Struktur Folder
- `app.py` : backend Flask
- `demo_inference.py` : Skrip demonstrasi eksekusi penalaran (inferensi) OWL-RL
- `data/academic_ontology_v1.owl` : file OWL utama yang memuat relasi dasar dan logika penalaran
- `templates/` : halaman HTML
- `static/style.css` : stylesheet
- `requirements.txt` : dependensi Python (termasuk Flask, rdflib, dan owlrl)

## Cara Menjalankan
1. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
2. Jalankan aplikasi:
   ```bash
   python app.py
   ```
3. Buka browser ke:
   ```bash
   http://127.0.0.1:5000
   ```

## Mengganti dengan File OWL Hasil Protégé
1. Ganti file `data/academic_ontology_v1.owl` dengan file OWL Anda.
2. Periksa namespace di Protégé. Jika berbeda dari:
   `http://example.org/akademik#`
   maka ubah:
   ```python
   BASE = Namespace("http://example.org/akademik#")
   ```
   di `app.py`.
3. Sesuaikan nama class dan property jika berbeda, misalnya:
   - `Dosen`
   - `MataKuliah`
   - `mengampu`
   - `memilikiPrasyarat`
   - `ditawarkanPadaSemester`

## Catatan Penting
- File OWL dari Protégé umumnya bisa langsung diparse oleh RDFLib.
- Jika file Anda memakai format RDF/XML, RDFLib biasanya dapat mendeteksinya otomatis.
- Jika struktur ontologi berubah, query SPARQL juga perlu ikut diperbarui.

## Ide Pengembangan
- Tambah route untuk mendemonstrasikan hasil *Inverse Property* di Web.
- Ganti `owlrl` dengan antarmuka ke *reasoner* eksternal skala besar menggunakan Apache Jena Fuseki atau GraphDB.