face_records = {u'FaceRecords': [{u'Face': {u'BoundingBox': {u'Height': 0.4109131395816803,
                                              u'Left': 0.36222222447395325,
                                              u'Top': 0.36302894353866577,
                                              u'Width': 0.4099999964237213},
                             u'Confidence': 99.69052124023438,
                             u'FaceId': u'1e76864a-5150-5ef1-9121-871559e867b5',
                             u'ImageId': u'9be9cbc9-1083-5b77-84bb-240350ebb008'},
                   u'FaceDetail': {u'BoundingBox': {u'Height': 0.4109131395816803,
                                                    u'Left': 0.36222222447395325,
                                                    u'Top': 0.36302894353866577,
                                                    u'Width': 0.4099999964237213},
                                   u'Confidence': 99.69052124023438,
                                   u'Landmarks': [{u'Type': u'eyeLeft',
                                                   u'X': 0.5256969928741455,
                                                   u'Y': 0.5180707573890686},
                                                  {u'Type': u'eyeRight',
                                                   u'X': 0.6495776176452637,
                                                   u'Y': 0.5229045152664185},
                                                  {u'Type': u'nose',
                                                   u'X': 0.6235997080802917,
                                                   u'Y': 0.6144701242446899},
                                                  {u'Type': u'mouthLeft',
                                                   u'X': 0.5251087546348572,
                                                   u'Y': 0.682335376739502},
                                                  {u'Type': u'mouthRight',
                                                   u'X': 0.6212663054466248,
                                                   u'Y': 0.6802090406417847}],
                                   u'Pose': {u'Pitch': -6.336112976074219,
                                             u'Roll': -0.2622215747833252,
                                             u'Yaw': 30.7182674407959},
                                   u'Quality': {u'Brightness': 44.108238220214844,
                                                u'Sharpness': 99.99671173095703}}}],
 u'OrientationCorrection': u'ROTATE_0',
 'ResponseMetadata': {'HTTPHeaders': {'connection': 'keep-alive',
                                      'content-length': '986',
                                      'content-type': 'application/x-amz-json-1.1',
                                      'date': 'Tue, 04 Apr 2017 11:46:25 GMT',
                                      'x-amzn-requestid': '542bee6a-192c-11e7-ae23-7d85e378e2dc'},
                      'HTTPStatusCode': 200,
                      'RequestId': '542bee6a-192c-11e7-ae23-7d85e378e2dc',
                      'RetryAttempts': 0}}

from PIL import Image

def laugh_size(face, orig):
	laugh_height = 530.
	laugh_width = 580.
	face_size = max(face['BoundingBox']['Width'] * orig.size[0], face['BoundingBox']['Height'] * orig.size[1])
	width = face_size * laugh_width / laugh_height
	height = face_size
	return (int(width), int(height))

def laugh_box(face, orig):
	left = face['BoundingBox']['Left'] * orig.size[0]
	top = face['BoundingBox']['Top'] * orig.size[1]
	width, height = laugh_size(face, orig)
	return (int(left), int(top), int(left + width), int(top + height))

def mount_laughing_face(img_path, face_records):
	orig = Image.open(img_path)
	laugh = Image.open('laughing_man.gif')
	for face_record in face_records['FaceRecords']:
		face = face_record['Face']
		warai_layer = Image.new('RGBA', orig.size, (255, 255,255, 0))
		warai_layer.paste(laugh.resize(laugh_size(face, orig)), box=laugh_box(face, orig))
		orig = Image.alpha_composite(orig, warai_layer)
	orig.save(img_path)

mount_laughing_face('sample.png', face_records)










