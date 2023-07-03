import subprocess

try:
    subprocess.run(['ffmpeg', '-i', 'w.mkv', '-codec', 'copy', 'w.mp4'], check=True)
except Exception as e:
    print(e)
