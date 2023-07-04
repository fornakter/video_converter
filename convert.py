import subprocess
import datetime

start = datetime.datetime.now()
try:
    subprocess.run(['ffmpeg', '-i', 'w.mkv', '-codec', 'copy', 'w.mp4'], check=True)
except Exception as e:
    print(e)
end = datetime.datetime.now()
print(end-start)