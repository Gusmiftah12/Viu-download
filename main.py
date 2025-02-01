import json
import requests
import re
import subprocess
from typing import Optional

SECRET_KEY_STATIC = 'zthxw34cdp6wfyxmpad38v52t3hsz6c5'
BEARER_TOKEN = 'eyJhbGciOiJBMTI4S1ciLCJlbmMiOiJBMTI4Q0JDLUhTMjU2In0.BeN5m3IfEOjBoc2NcHF8ThZ7r8xZO_xZycBfUsy64lyM0ePSupyN-w.gUz3KiNyppMTujGYnKRJYA.fuWx7ciwQ33JWENLKye3H0LRc22dkp0ot-kkPb2gbqVMpr0H7AIw1TP2Aq7o9ABN6MvcTJnwpSCu3YhzJk05B3kTxHb7esFMgHVDTHp55qBJey9FCZ613zGac6dIRriEan3UkXO4yx9NKCvO25675RPphUsRerXxeQhKnCdb8VTVD2lP50K8u9Q2hJZm2RbhyQjPs9ntANv76piNhFc90kB4vk9cX5aFlLTwJIIMSMk8hTGE2fMQc-B8AhDbm3FRRiuicse1Blhi3N0BSqteyw.2ZPwFWX4oU6wDBtT4vO36A'
VIU_URL = 'https://www.viu.com/ott/id/id/vod/2566357/Study-Group'

PROXIES = [
    "161.123.152.115:6360:pmcyaxai:1t5295cjepoo",
    "23.94.138.75:6349:pmcyaxai:1t5295cjepoo",
    "154.36.110.199:6853:pmcyaxai:1t5295cjepoo",
    "173.0.9.70:5653:pmcyaxai:1t5295cjepoo",
    "173.0.9.209:5792:pmcyaxai:1t5295cjepoo"
]

def get_product_and_series_id(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K)'}
    for proxy in PROXIES:
        ip, port, user, password = proxy.split(":")
        proxy_url = f"http://{user}:{password}@{ip}:{port}"
        proxies = {"http": proxy_url, "https": proxy_url}
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            if response.status_code == 200:
                series_match = re.search(r'"series_id":\s*"(\d+)"', response.text)
                product_match = re.search(r'"product_id":\s*"(\d+)"', response.text)
                if series_match and product_match:
                    return series_match.group(1), product_match.group(1)
        except requests.RequestException:
            pass
    return None, None

def get_ccs_product_id(product_id, series_id):
    url = f'https://api-gateway-global.viu.com/api/mobile?r=/vod/product-list&product_id={product_id}&series_id={series_id}&size=1000&platform_flag_label=phone&language_flag_id=8&ut=2&area_id=1000&os_flag_id=2&countryCode=ID'
    headers = {
        'Authorization': f'Bearer {BEARER_TOKEN}',
        'User-Agent': 'okhttp/4.12.0',
        'platform': 'android',
        'content-type': 'application/json'
    }
    for proxy in PROXIES:
        ip, port, user, password = proxy.split(":")
        proxy_url = f"http://{user}:{password}@{ip}:{port}"
        proxies = {"http": proxy_url, "https": proxy_url}
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            if response.status_code == 200:
                data = response.json()
                product_list = data.get('data', {}).get('product_list', [])
                if product_list:
                    return product_list[0].get('ccs_product_id')
        except requests.RequestException:
            pass
    return None

def get_stream_links(ccs_product_id):
    headers = {'Authorization': f'Bearer {BEARER_TOKEN}', 'User-Agent': 'Mozilla/5.0'}
    params = {'ccs_product_id': ccs_product_id}
    response = requests.get('https://api-gateway-global.viu.com/api/playback/distribute', params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get('data', {}).get('stream', {}).get('url', {})
    return None

def download_video(m3u8_url: str, output_filename="video.mp4"):
    headers = [
        "-headers", 
        "User-Agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36\r\n"
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\n"
        "Accept-Language: id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7\r\n"
        "Cache-Control: max-age=0\r\n"
        "Sec-Ch-Ua: \"Not A(Brand\";v=\"8\", \"Chromium\";v=\"132\"\r\n"
        "Sec-Ch-Ua-Mobile: ?1\r\n"
        "Sec-Ch-Ua-Platform: \"Android\"\r\n"
        "Sec-Fetch-Dest: document\r\n"
        "Sec-Fetch-Mode: navigate\r\n"
        "Sec-Fetch-Site: none\r\n"
        "Sec-Fetch-User: ?1\r\n"
        "Upgrade-Insecure-Requests: 1\r\n"
    ]

    ffmpeg_command = [
        "ffmpeg", "-y", "-loglevel", "info",
        "-i", m3u8_url, *headers,
        "-c", "copy", output_filename
    ]

    subprocess.run(ffmpeg_command)

# Proses utama
while True:
    series_id, product_id = get_product_and_series_id(VIU_URL)
    if series_id and product_id:
        break

ccs_product_id = get_ccs_product_id(product_id, series_id)
if ccs_product_id:
    stream_links = get_stream_links(ccs_product_id)
    if stream_links and "s1080p" in stream_links:
        m3u8_url = stream_links["s1080p"]
        print(f"Downloading from: {m3u8_url}\n")
        download_video(m3u8_url)
else:
    print("Gagal mendapatkan video link.")
