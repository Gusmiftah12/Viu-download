import subprocess

url = "https://d1k2us671qcoau.cloudfront.net/vodapi/vuclip_bp.m3u8?vid=1166232456&layer=P2/video/60da9093-8a93-45ab-81b3-129414d84c08/vid_1080p_V20250126203408.m3u8&area_id=1000&lang_id=8&ts=202501310316&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9kMWsydXM2NzFxY29hdS5jbG91ZGZyb250Lm5ldC92b2RhcGkvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTczODI4MjU4OX19fV19&Signature=fiku1s1L6XyWqdAFOMlda4ZRRtOGK1lLHFMqv6dTb~eJUVDRshqrFU1DdcKJCroicEl7rdiZl5DBnWTJE0lLM5vt9uHC8lPqWZGFBcCrV9qf3olnab-MW0FN4WxwGME7Cty1jIATgNzcrcZD9VYWnaechJ5t5Ums3rhn7ae8Z673xxObRIqlB1mTDqXq8OKTP9InMIiyum8UCTVuohRXuIHlw4FrDVk5UlC0BiAye9nJltuWdpoWxyI6qDsS5JGtga9IE6Vqcrf2sSPlH957fDNLLASypd-f3raF35Idgw~f9YvHItVgyNEBhCOPRzFSj2oN~YE9oBCJpvtzunE5vw__&Key-Pair-Id=APKAJ6Z4RF5IYK7Y3SQQ"
output_file = "file.mp4"

command = [
    "ffmpeg", 
    "-i", url,
    "-bsf:a", "aac_adtstoasc",
    "-vcodec", "copy",
    "-c", "copy",
    "-crf", "50",
    output_file
]

# Execute the command
subprocess.run(command)
