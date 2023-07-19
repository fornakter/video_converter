import subprocess
import datetime
fileList = ['1', '2']

start = datetime.datetime.now()

try:
    for i in range(len(fileList)):
        subprocess.run(['ffmpeg', '-i', f'{fileList[i]}.mkv', '-codec', 'copy', f'{fileList[i]}.mp4'], check=True)
except Exception as e:
    print(e)
end = datetime.datetime.now()
print(end-start)