import os
import time

def embed_lsb(cover_audio_path, payload_path, output_path):

    total_start = time.perf_counter()

    # ==========================================================
    # 1. BACA PAYLOAD
    # ==========================================================
    payload_read_start = time.perf_counter()

    try:
        with open(payload_path, 'rb') as f:
            payload_data = f.read()
    except FileNotFoundError:
        print(f"[!] Payload {payload_path} tidak ditemukan.")
        return

    payload_read_end = time.perf_counter()

    payload_len = len(payload_data)
    print(f"[*] Ukuran Payload: {payload_len} bytes")

    # ==========================================================
    # 2. KONVERSI PAYLOAD KE BIT
    # ==========================================================
    bit_convert_start = time.perf_counter()

    payload_bits = []
    for byte in payload_data:
        for i in range(7, -1, -1):
            payload_bits.append((byte >> i) & 1)

    bit_convert_end = time.perf_counter()

    # ==========================================================
    # 3. BACA COVER AUDIO
    # ==========================================================
    audio_read_start = time.perf_counter()

    try:
        with open(cover_audio_path, 'rb') as f:
            audio_bytes = bytearray(f.read())
    except FileNotFoundError:
        print(f"[!] Cover audio {cover_audio_path} tidak ditemukan.")
        return

    audio_read_end = time.perf_counter()

    # ==========================================================
    # 4. HITUNG KAPASITAS
    # ==========================================================
    header_len = 44
    max_capacity = len(audio_bytes) - header_len

    print(f"[*] Kapasitas Audio: {max_capacity // 8} bytes")

    if len(payload_bits) > max_capacity:
        print("[!] Error: File audio terlalu kecil untuk menampung payload ini.")
        return

    print("[*] Memulai penyisipan LSB...")

    # ==========================================================
    # 5. PROSES EMBEDDING LSB
    # ==========================================================
    embed_start = time.perf_counter()

    for i in range(len(payload_bits)):
        audio_index = header_len + i

        audio_bytes[audio_index] = (
            audio_bytes[audio_index] & 0xFE
        ) | payload_bits[i]

    embed_end = time.perf_counter()

    # ==========================================================
    # 6. SIMPAN FILE STEGO
    # ==========================================================
    save_start = time.perf_counter()

    with open(output_path, 'wb') as f:
        f.write(audio_bytes)

    save_end = time.perf_counter()

    total_end = time.perf_counter()

    # ==========================================================
    # 7. HASIL
    # ==========================================================
    print("\n[+] Berhasil!")
    print(f"[+] File tersimpan di: {output_path}")
    print(f"[+] Ukuran Payload: {payload_len} bytes")

    print("\n================ PERFORMANCE RESULTS ================")
    print(f"Payload Read Time      : {(payload_read_end - payload_read_start):.4f} s")
    print(f"Bit Conversion Time    : {(bit_convert_end - bit_convert_start):.4f} s")
    print(f"Audio Read Time        : {(audio_read_end - audio_read_start):.4f} s")
    print(f"LSB Embedding Time     : {(embed_end - embed_start):.4f} s")
    print(f"Output Save Time       : {(save_end - save_start):.4f} s")
    print("----------------------------------------------------")
    print(f"Total Embedding Time   : {(total_end - total_start):.4f} s")
    print("====================================================")

    print("\n[+] PENTING: Catat ukuran payload untuk proses ekstraksi nanti.")


# ==========================================================
# KONFIGURASI FILE
# ==========================================================

embed_lsb(
    'music.wav',
    'payload.exe',
    'hidden.wav'
)