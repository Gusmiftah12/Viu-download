import subprocess

def download_video_with_headers(m3u8_url, output_filename="output.mp4"):
    # Headers yang ingin ditambahkan
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/vnd.apple.mpegurl',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Encoding': 'identity',
        'Connection': 'Keep-Alive'
    }
    
    # Format headers menjadi string yang dapat dipakai dalam ffmpeg
    headers_string = ' '.join([f"-headers \"{key}: {value}\"" for key, value in headers.items()])
    
    # Command ffmpeg untuk mengunduh dan menyimpan video
    command = f"ffmpeg -i \"{m3u8_url}\" {headers_string} -c copy {output_filename}"
    
    # Menjalankan perintah
    subprocess.run(command, shell=True)
    print(f"✅ Video saved as {output_filename}")

# Contoh pemanggilan fungsi
m3u8_url = "https://d1k2us671qcoau.cloudfront.net/vodapi/vuclip_bp.m3u8?vid=1166232457&layer=P2/video/6b6d01f2-072d-459f-990d-89295e3f5f16/vid_1080p_V20250126203418.m3u8&area_id=1000&lang_id=8&ts=202501310216&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9kMWsydXM2NzFxY29hdS5jbG91ZGZyb250Lm5ldC92b2RhcGkvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTczODI3ODk3Mn19fV19&Signature=ETnOGGFoP0d3AoSNYjm8RnHxccXbojBZTCruALKn32ver-EH0upAV3HkFeBq4nisTp8LxDimwJ5yV3abj4m-Yv3CHBbusbbdDyXx0RKSvWeoNMWnPksskGGa~eynvo3ao7YGRyH0wPCu~ibhwDeP0Ee6gGp0GRZ4O4N6U4o1WeExphZMpLlYRXzne0v2Teecwuj7TaDE8h5m-39G1N65V8tbRfbymfcj~tQqdVAq169l8QmmobJ2d0J6QN7KpBWVa7BzphWyuRcakQbpcWhk0xpas1VxwxDpdqToA587JN2uSk3mjidb0p5vjP5L8e4kFzOdv8EYet0WqccaJWfEvw__&Key-Pair-Id=APKAJ6Z4RF5IYK7Y3SQQ"
download_video_with_headers(m3u8_url)
