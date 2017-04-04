import json
import boto3
import os
import pprint
from PIL import Image
import base64

bucket_hidden = "hidden.waraiotoko"
s3 = boto3.client('s3')
rek = boto3.client('rekognition')

def upload(event, context):
    body = json.loads(event['body'])
    byte = base64.b64decode(body['image'])

    input_path = '/tmp/input.img'
    output_path = '/tmp/output.png'
    with open(input_path, 'wb') as input_file:
        input_file.write(byte)

    face_details = get_face_details_from_blob(byte)
    mount_laughing_face(input_path, output_path, face_details)

    with open(output_path, 'rb') as output_file:
        output_b64 = base64.b64encode(output_file.read())

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin' : '*'
        },
        'body': json.dumps({
            'image': output_b64
        })
    }

def get_face_details_from_blob(byte):
    response = rek.detect_faces(
        Image={
            'Bytes': byte
        }
    )

    return response['FaceDetails']

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

def mount_laughing_face(input_path, output_path, face_details):
    orig = Image.open(input_path)
    orig = orig.convert('RGBA')
    laugh = Image.open('laughing_man.gif')
    for face in face_details:
        warai_layer = Image.new('RGBA', orig.size, (255, 255,255, 0))
        warai_layer.paste(fit_laugh(face, laugh, orig), box=laugh_position(face, orig))
        orig = Image.alpha_composite(orig, warai_layer)
    orig.save(output_path)

