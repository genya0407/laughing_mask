import cStringIO
import base64
from PIL import Image

with open('/Users/sangenya/Downloads/sample_old.png', 'rb') as f:
	b64 = base64.b64encode(f.read())
file = cStringIO.StringIO(base64.b64decode(b64))
file.read()
out = cStringIO.StringIO()
Image.open(file).save(out)