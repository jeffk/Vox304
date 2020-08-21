#!/usr/bin/env python3

#./proxy.py
#cp MacOS753.backup MacOS753
#BasiliskII.app/Contents/MacOS/BasiliskII --config ./basilisk_ii_prefs 
#sleep 10
#screencapture -l$(./GetWindowID BasiliskII "Basilisk II") BasiliskII.png
#kill Basilisk
#post tweet

from twython import Twython
from PIL import Image
from subprocess import Popen, PIPE, STDOUT, check_output
from time import sleep
import signal
import os
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read
import json

CREDS = json.loads(open("creds.json").read())

twitter = Twython(CREDS['CONSUMER_KEY'], CREDS['CONSUMER_SECRET'],
                  CREDS['ACCESS_TOKEN'], CREDS['ACCESS_TOKEN_SECRET'])

process = Popen('cp MacOS753.backup MacOS753', shell=True)

process.wait()

print("Drive replaced.")
errors = open('run.errors','w')
proxy = Popen(['/usr/bin/python','-u','proxy.py'], stdin=PIPE, stdout=PIPE, stderr=errors)
flags = fcntl(proxy.stdout, F_GETFL) # get current p.stdout flags
fcntl(proxy.stdout, F_SETFL, flags | O_NONBLOCK)

sleep(1)

basiliskII = Popen(['./BasiliskII.app/Contents/MacOS/BasiliskII','--config','./basilisk_ii_prefs'], stdout=PIPE, stderr=STDOUT)
sleep(10)
screencaprm = Popen(['/bin/rm -f BasiliskII.png'], shell=True)
screencaprm.wait()
screencap = Popen(['/usr/sbin/screencapture -o -l$(./GetWindowID BasiliskII "Basilisk II") ./BasiliskII.png'], shell=True, stdout=PIPE, stderr=STDOUT)
screencap.wait()
text = read(proxy.stdout.fileno(), 640).decode('utf-8')
#print text

img = Image.open("BasiliskII.png")
# image is 752 x 614, should be 640x480
img2 = img.crop((0, 44, 1280, 1004))
img2.save("screenshot.png")


data = {}
print(text)
for line in text.split("\n"):
	try:
		key, value = line.split(" ", 1)
		data[key] = value
	except:
		pass

print(data)
if data.get('AUTHOR_TWITTER'):
	data['AUTHOR'] = data['AUTHOR_TWITTER']

status = "%s by %s on %s\n%s" % (data['HEADLINE'], data['AUTHOR'], data.get('TWITTER', data['SITE']), data['HEADLINE_URL'])
photo = open('screenshot.png', 'rb')
response = twitter.upload_media(media=photo)
twitter.update_status(status=status, media_ids=[response['media_id']])

sleep(5)
proxy.terminate()

os.killpg(os.getpgid(basiliskII.pid), signal.SIGKILL)

os.system("killall -KILL BasiliskII")
os.system("ps ax | grep [p]roxy.py | awk '{print $1}' |xargs kill")
print("Done!")
