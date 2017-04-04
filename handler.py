import json
import boto3
import os
import pprint
from PIL import Image

bucket_hidden = "hidden.waraiotoko"
s3 = boto3.client('s3')
rek = boto3.client('rekognition')

def hello(event, context):
    for record in event['Records']:
        face_details = get_face_details(record)
        img_path = download_img(record)
        mount_laughing_face(img_path, face_details)
        s3.upload_file(img_path, bucket_hidden, os.path.basename(img_path))

def get_face_details(record):
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    response = rek.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        }
    )

    return response['FaceDetails']

def download_img(record):
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    img_path = '/tmp/' + key
    s3.download_file(bucket, key, img_path)

    return img_path

def laugh_size(face, orig):
    laugh_height = 530.
    laugh_width = 580.
    face_size = max(face['BoundingBox']['Width'] * orig.size[0], face['BoundingBox']['Height'] * orig.size[1])
    width = face_size * laugh_width / laugh_height
    height = face_size
    return (int(width), int(height))

def laugh_position(face, orig):
    left = face['BoundingBox']['Left'] * orig.size[0]
    top = face['BoundingBox']['Top'] * orig.size[1]

    return (int(left), int(top))

def laugh_crop_size(face, orig):
    left, top = laugh_position(face, orig)
    width, height = laugh_size(face, orig)

    # When a face is placed at the edge of the original image,
    # the laughing-face will be placed at out-of-range area.
    # Following code will avoid it.
    if (left + width) > orig.size[0]:
        width = orig.size[0] - left
    if (top + height) > orig.size[1]:
        height = orig.size[1] - top

    return (0, 0, int(width), int(height))

def fit_laugh(face, laugh, orig):
    return laugh.resize(laugh_size(face, orig)).crop(laugh_crop_size(face, orig))

def mount_laughing_face(img_path, face_details):
    orig = Image.open(img_path)
    orig = orig.convert('RGBA')
    laugh = Image.open('laughing_man.gif')
    for face in face_details:
        warai_layer = Image.new('RGBA', orig.size, (255, 255,255, 0))
        warai_layer.paste(fit_laugh(face, laugh, orig), box=laugh_position(face, orig))
        orig = Image.alpha_composite(orig, warai_layer)
    orig.save(img_path)


