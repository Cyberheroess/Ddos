# Dokumentasi Script Serangan DDoS & Bypass WAF

## Deskripsi Umum
Script ini adalah alat pengujian keamanan yang mencakup berbagai teknik serangan untuk menguji ketahanan web server dan WAF (Web Application Firewall). Fitur utamanya meliputi **brute force proxy**, **bypass WAF**, serta serangan multi-vector berupa **TCP flood** dan **UDP flood**.

## Fitur Utama
1. **Proxy Brute Force**  
   Menggunakan daftar proxy acak untuk menguji validitas koneksi ke target.

2. **Bypass WAF**  
   Payload dienkode dengan metode Base64 untuk menghindari filter WAF.

3. **Multi-vector Attack**  
   - **TCP Flood**: Membanjiri server dengan koneksi TCP socket.  
   - **UDP Flood**: Mengirimkan paket UDP dummy secara berulang.

4. **Logging**  
   Semua aktivitas serangan dicatat secara otomatis dalam file log.

---

## Struktur Fungsi

### 1. `start_attack(target_url)`
- Fungsi utama untuk mengatur serangan.  
- Langkah-langkah:  
   1. Mengambil hostname dari URL target.  
   2. Melakukan bypass WAF hingga berhasil.  
   3. Menjalankan brute force proxy untuk mencari proxy valid.  
   4. Melakukan serangan **TCP Flood** dan **UDP Flood** menggunakan **ThreadPoolExecutor**.

---

### 2. `generate_proxy()`
- Membuat proxy acak dalam format `IP:Port`.  
- Menghasilkan IP acak dan port antara `1080` hingga `65535`.

---

### 3. `test_proxy(proxy, target_url, log_file)`
- Menguji apakah proxy dapat mengakses target URL.  
- Log hasil proxy (valid atau tidak) ke dalam file log.

---

### 4. `attempt_bypass_waf(target_url, log_file)`
- Mencoba bypass WAF dengan mengirimkan payload dienkode Base64.  
- Berulang hingga bypass berhasil.

**Helper Function:**
- `generate_encoded_payload(payload)`  
  Mengekode payload menjadi format Base64.  
- `test_waf_bypass(target_url, payload, log_file)`  
  Mengirimkan payload ke server untuk menguji bypass.

---

### 5. `tcp_flood(target_ip, target_port, log_file)`
- Membuat koneksi TCP ke target IP dan port.  
- Mengirimkan paket HTTP dummy melalui socket.

---

### 6. `udp_flood(target_ip, target_port, log_file)`
- Mengirimkan paket UDP dummy ke target IP dan port secara terus-menerus.

---

### 7. `brute_force_proxy(proxy_list, target_url, log_file)`
- Menggunakan **ThreadPoolExecutor** untuk menguji banyak proxy secara paralel.

---

### 8. `create_log_file()`
- Membuat direktori `logs` (jika belum ada).  
- Menghasilkan file log dengan format nama file berdasarkan **timestamp**.

---

## Eksekusi Script

### Input
Pengguna akan diminta untuk memasukkan URL target, contoh:

Masukkan URL target (misalnya http://example.com):

### Output
- Log hasil serangan disimpan di direktori **logs/**.  
- Aktivitas serangan ditampilkan dalam terminal saat script berjalan.

---

## Struktur Direktori

|-- main.py                 # Script utama |-- logs/                   # Direktori penyimpanan file log |-- ddos_attack_<timestamp>.log  # Log aktivitas serangan

---

## Catatan Keamanan
- Script ini dibuat untuk **pengujian keamanan** dan **tujuan edukasi**.  
- **Penggunaan script untuk menyerang sistem tanpa izin** melanggar hukum dan etika.  
- Pengguna bertanggung jawab penuh atas penyalahgunaan script ini.

---

## Teknologi yang Digunakan
- **Python 3.11**  
- Library utama:  
  - `socket`  
  - `requests`  
  - `base64`  
  - `threading`  
  - `concurrent.futures`  

---

## Cara Menjalankan Script
1. Pastikan Python sudah diinstal di sistem.  
2. Simpan script sebagai `main.py`.  
3. Jalankan script menggunakan terminal:  
   ```bash
   python3 main.py

4. Masukkan URL target saat diminta.




---
