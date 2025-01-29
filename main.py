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

class CryptoJS:
    def _EVPKDF(self, password: Union[str, bytes, bytearray], salt: Union[bytes, bytearray], keySize=32, ivSize=16, iterations=1, hashAlgorithm="md5") -> tuple:
        if isinstance(password, str):
            password = password.encode("utf-8")
        final_length = keySize + ivSize
        key_iv = b""
        block = None
        while len(key_iv) < final_length:
            hasher = hashlib.new(hashAlgorithm)
            if block:
                hasher.update(block)
            hasher.update(password)
            hasher.update(salt)
            block = hasher.digest()
            for _ in range(1, iterations):
                block = hashlib.new(hashAlgorithm, block).digest()
            key_iv += block
        key, iv = key_iv[:keySize], key_iv[keySize:final_length]
        return key, iv

def get_series_id(url):
    headers = {
        'authority': 'www.viu.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': '_ottUID=9873719d-4227-4cd9-823a-d1d37382f44c; onboarding_date=2025-01-08; onboarding_session=f63c887c-791b-4334-a063-e234a0a381c1; areaId=1000; countryCode=id; platform=browser; app_language=id; account_type=1; user_id=1701173790; user_level=2; AWSALB=UIr/uXJWbPthvypb9IdNIyiguYrxfJL35V4UuyliDscqlEt026RW0MMvw7ulNw/aZNQYXJ3uljBPLdCzHkM74SvSyui0xiOIkDXe8m+kqpcY62zocDihshhH/BC/; AWSALBCORS=UIr/uXJWbPthvypb9IdNIyiguYrxfJL35V4UuyliDscqlEt026RW0MMvw7ulNw/aZNQYXJ3uljBPLdCzHkM74SvSyui0xiOIkDXe8m+kqpcY62zocDihshhH/BC/; token=eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0.BeN5m3IfEOjBoc2NcHF8ThZ7r8xZO_xZycBfUsy64lyM0ePSupyN-w.gUz3KiNyppMTujGYnKRJYA.fuWx7ciwQ33JWENLKye3H0LRc22dkp0ot-kkPb2gbqVMpr0H7AIw1TP2Aq7o9ABN6MvcTJnwpSCu3YhzJk05B3kTxHb7esFMgHVDTHp55qBJey9FCZ613zGac6dIRriEan3UkXO4yx9NKCvO25675RPphUsRerXxeQhKnCdb8VTVD2lP50K8u9Q2hJZm2RbhyQjPs9ntANv76piNhFc90kB4vk9cX5aFlLTwJIIMSMk8hTGE2fMQc-B8AhDbm3FRRiuicse1Blhi3N0BSqteyw.2ZPwFWX4oU6wDBtT4vO36A',
        'if-none-match': '"wrhsohnr3b3oit"',
        'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        match = re.search(r'"series_id":\s*"(\d+)"', response.text)
        if match:
            return match.group(1)
    
    return None


def get_product_list(series_id):
    url = f'https://api-gateway-global.viu.com/api/mobile?r=/vod/product-list&series_id={series_id}'
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
        'User-Agent': 'Mozilla/5.0'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
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
        print(f"Subtitle downloaded successfully: {subtitle_filename}")
        return subtitle_filename
    else:
        print("Failed to download subtitle.")
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
    print(f"Video saved as {output_filename}")

# **Eksekusi Skrip**
series_id = get_series_id(VIU_URL)
if series_id:
    ccs_product_id = get_product_list(series_id)
    if ccs_product_id:
        stream_links = get_stream_links(ccs_product_id)
        if stream_links and "s1080p" in stream_links:
            m3u8_url = stream_links["s1080p"]
            print(f"Downloading from: {m3u8_url}")
            
            subtitle_path = download_subtitle()
            if subtitle_path:
                download_video(m3u8_url, subtitle_path)
            else:
                print("Skipping subtitle embedding due to subtitle download failure.")
        else:
            print("1080p stream not available.")
    else:
        print("Failed to get CCS Product ID.")
else:
    print("Failed to get Series ID.")
