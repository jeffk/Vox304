#!/usr/bin/env python

#./proxy.py
#cp MacOS753.backup MacOS753
#BasiliskII.app/Contents/MacOS/BasiliskII --config ./basilisk_ii_prefs 
#sleep 10
#screencapture -l$(./GetWindowID BasiliskII "Basilisk II") BasiliskII.png
#kill Basilisk
#post tweet

from twython import Twython
from PIL import Image
from subprocess import Popen, PIPE, STDOUT
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

print "Drive replaced."

proxy = Popen(['python','-u','proxy.py'], stdin=PIPE, stdout=PIPE, stderr=STDOUT)
flags = fcntl(proxy.stdout, F_GETFL) # get current p.stdout flags
fcntl(proxy.stdout, F_SETFL, flags | O_NONBLOCK)

sleep(1)

basiliskII = Popen(['./BasiliskII.app/Contents/MacOS/BasiliskII','--config','./basilisk_ii_prefs'], stdout=PIPE, stderr=PIPE)

sleep(12)
screencaprm = Popen(['/bin/rm -f BasiliskII.png'], shell=True)
screencaprm.wait()
screencap = Popen(['/usr/sbin/screencapture -l$(./GetWindowID BasiliskII "Basilisk II") BasiliskII.png'], shell=True)
screencap.wait()
text = read(proxy.stdout.fileno(), 640)
print text

img = Image.open("BasiliskII.png")
# image is 752 x 614, should be 640x480
img2 = img.crop((56, 54, 696, 534))
img2.save("screenshot.png")

print "Done!"
data = {}
for line in text.split("\n"):
	try:
		key, value = line.split(" ", 1)
		data[key] = value
	except:
		pass

print "Author: %s" % data['AUTHOR']

status = "%s by %s on %s\n%s" % (data['HEADLINE'], data['AUTHOR'], data['TWITTER'], data['HEADLINE_URL'])
photo = open('screenshot.png', 'rb')
response = twitter.upload_media(media=photo)
twitter.update_status(status=status, media_ids=[response['media_id']])

proxy.terminate()

os.killpg(os.getpgid(basiliskII.pid), signal.SIGKILL)
