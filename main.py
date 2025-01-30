import json
import requests
import base64
import hashlib
import os
import re
import subprocess
from typing import Union
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

SECRET_KEY_STATIC = 'zthxw34cdp6wfyxmpad38v52t3hsz6c5'
BEARER_TOKEN = 'eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0.BeN5m3IfEOjBoc2NcHF8ThZ7r8xZO_xZycBfUsy64lyM0ePSupyN-w.gUz3KiNyppMTujGYnKRJYA.fuWx7ciwQ33JWENLKye3H0LRc22dkp0ot-kkPb2gbqVMpr0H7AIw1TP2Aq7o9ABN6MvcTJnwpSCu3YhzJk05B3kTxHb7esFMgHVDTHp55qBJey9FCZ613zGac6dIRriEan3UkXO4yx9NKCvO25675RPphUsRerXxeQhKnCdb8VTVD2lP50K8u9Q2hJZm2RbhyQjPs9ntANv76piNhFc90kB4vk9cX5aFlLTwJIIMSMk8hTGE2fMQc-B8AhDbm3FRRiuicse1Blhi3N0BSqteyw.2ZPwFWX4oU6wDBtT4vO36A'
VIU_URL = 'https://www.viu.com/ott/id/id/vod/2566357/Study-Group'

# Daftar proxy dengan autentikasi
PROXIES = [
    "198.23.239.134:6540:pmcyaxai:1t5295cjepoo",
    "207.244.217.165:6712:pmcyaxai:1t5295cjepoo",
    "107.172.163.27:6543:pmcyaxai:1t5295cjepoo",
    "64.137.42.112:5157:pmcyaxai:1t5295cjepoo",
    "173.211.0.148:6641:pmcyaxai:1t5295cjepoo",
    "161.123.152.115:6360:pmcyaxai:1t5295cjepoo",
    "23.94.138.75:6349:pmcyaxai:1t5295cjepoo",
    "154.36.110.199:6853:pmcyaxai:1t5295cjepoo",
    "173.0.9.70:5653:pmcyaxai:1t5295cjepoo",
    "173.0.9.209:5792:pmcyaxai:1t5295cjepoo"
]

def get_series_id(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
        'Accept': '*/*'
    }
    
    for proxy in PROXIES:
        ip, port, user, password = proxy.split(":")
        proxy_url = f"http://{user}:{password}@{ip}:{port}"
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
        
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            if response.status_code == 200:
                match = re.search(r'"series_id":\s*"(\d+)"', response.text)
                if match:
                    print(f"✅ Series ID ditemukan: {match.group(1)} menggunakan proxy {ip}")
                    return match.group(1)
            else:
                print(f"❌ Gagal mendapatkan Series ID, status {response.status_code} menggunakan proxy {ip}")
        except requests.RequestException as e:
            print(f"❌ Proxy {ip} gagal: {e}")

    return None  # Jika semua proxy gagal

def get_product_list(series_id):
    url = f'https://api-gateway-global.viu.com/api/mobile?platform_flag_label=web&area_id=1000&language_flag_id=8&platformFlagLabel=web&areaId=1000&languageFlagId=8&countryCode=ID&ut=0&r=%2Fvod%2Fproduct-list&os_flag_id=1&size=-1&sort=desc&series_id={series_id}'
    headers = {
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://www.viu.com/',
        'sec-ch-ua-mobile': '?1',
        'Authorization': f'Bearer {BEARER_TOKEN}',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua-platform': '"Android"',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(data)
        product_list = data.get('data', {}).get('product_list', [])
        if product_list:
            return product_list[0].get('ccs_product_id')
    return None

def get_stream_links(ccs_product_id):
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}', 'User-Agent': 'Mozilla/5.0'}
    params = {'ccs_product_id': ccs_product_id}
    response = requests.get('https://api-gateway-global.viu.com/api/playback/distribute', params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', {}).get('stream', {}).get('url', {})
    return None

def download_subtitle():
    subtitle_url = "https://downsub.com/example.srt"  # Ubah dengan URL subtitle asli
    subtitle_filename = "subtitle.srt"
    
    response = requests.get(subtitle_url)
    if response.status_code == 200:
        with open(subtitle_filename, 'wb') as file:
            file.write(response.content)
        print(f"✅ Subtitle downloaded: {subtitle_filename}")
        return subtitle_filename
    else:
        print("❌ Failed to download subtitle.")
        return None

def download_video(m3u8_url, subtitle_path, output_filename="video.mp4"):
    command = [
        "ffmpeg", "-i", m3u8_url,
        "-vf", f"scale=1920:1080,subtitles={subtitle_path}",
        "-r", "24",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-c:a", "aac", "-b:a", "160k", "-ac", "2", "-af", "volume=3.0",
        "-movflags", "+faststart", output_filename
    ]
    
    subprocess.run(command)
    print(f"✅ Video saved as {output_filename}")

# **Eksekusi Skrip**
while True:
    series_id = get_series_id(VIU_URL)
    if series_id:
        break  # Keluar dari loop jika berhasil mendapatkan series_id
    print("🔄 Mencoba lagi mendapatkan Series ID...")

ccs_product_id = get_product_list(series_id)
if ccs_product_id:
    stream_links = get_stream_links(ccs_product_id)
    if stream_links and "s1080p" in stream_links:
        m3u8_url = stream_links["s1080p"]
        print(f"🎥 Downloading from: {m3u8_url}")

        subtitle_path = download_subtitle()
        if subtitle_path:
            download_video(m3u8_url, subtitle_path)
        else:
            print("⚠️ Skipping subtitle embedding due to subtitle download failure.")
    else:
        print("⚠️ 1080p stream not available.")
else:
    print("❌ Failed to get CCS Product ID.")
