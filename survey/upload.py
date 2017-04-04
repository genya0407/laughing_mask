import urllib
import urllib2
import base64
import json

url = "https://2wm859rbjg.execute-api.us-west-2.amazonaws.com/dev/image"
with open('/Users/sangenya/Downloads/16807539_999755836823337_8544546211950702902_n.jpg', 'rb') as img:
	params = { 'image': base64.b64encode(img.read()) }

req = urllib2.Request(url)
req.add_header('Content-Type', 'application/json')
req.add_data(json.dumps(params))

res = urllib2.urlopen(req)
img = base64.b64decode(json.loads(res.read())['image'])

with open('output.png', 'wb') as img_file:
	img_file.write(img)