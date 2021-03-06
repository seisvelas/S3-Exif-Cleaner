#!python3

import boto3
from os import environ
from io import BytesIO
from PIL import Image, ImageOps, UnidentifiedImageError
from getopt import getopt
import argparse

# Get bucket name and prefix from 
parser = argparse.ArgumentParser()
parser.add_argument(
    '-b', '--bucket', default='flowcrypt-test', 
    help='Name of S3 bucket')
parser.add_argument(
    '-p', '--prefix', default='', 
    help='(optional) Only wash images starting with this prefix')
parser.add_argument(
    '-i', '--interactive', action='store_true', 
    help='(optional) Ask user to confirm each object before altering it')
args = parser.parse_args()

try:
    print('loading credentials from default configuration file ($HOME/.aws/credentials)...')
    s3 = boto3.resource('s3',
        #aws_access_key_id=environ['API_KEY_AWS_S3_ID'],
        #aws_secret_access_key= environ['API_KEY_AWS_S3_SECRET']
    )
    print(s3.meta.client.head_bucket(Bucket=s3.name))
except AttributeError:
    print('failed, attempting to load from local directory .env file...')
    s3 = boto3.resource('s3',
        aws_access_key_id=environ['API_KEY_AWS_S3_ID'],
        aws_secret_access_key= environ['API_KEY_AWS_S3_SECRET']
    )

bucket = s3.Bucket(args.bucket)
scrubbed_files_count = 0

for obj in bucket.objects.filter(Prefix=args.prefix):
    if 'jpg' in obj.key:
        try:
            obj_url = f'https://{args.bucket}.s3.amazonaws.com/{obj.key}'
            if args.interactive:
                prompt = f'Replace object at {obj_url} with scrubbed version? (Y/n) '
                if input(prompt).lower() != 'y':
                    continue

            print(f'Cleansing EXIF data on: {obj_url}')

            # Download image as raw bytes
            img_bytes_exif = BytesIO()
            img_bytes_exif.seek(0)
            bucket.download_fileobj(obj.key, img_bytes_exif)

            # Transpose image per EXIF data, then scrub
            img_bytes_NO_exif = BytesIO()
            img_ops = Image.open(img_bytes_exif)
            # exif data includes orientation image
            # without which the image may end up rotated
            # incorrectly. So we rotate the image per
            # the exif data before scrubbing it.
            img_ops = ImageOps.exif_transpose(img_ops)
            # img_ops.save implicitly excludes EXIF data
            # unless you explicitly tell it not to via the
            # exif parameter
            img_ops.save(img_bytes_NO_exif, format='jpeg')

            # Overwrite original image w/ scrubbed version
            img_bytes_NO_exif.seek(0)
            s3.meta.client.upload_fileobj(img_bytes_NO_exif, args.bucket, obj.key)
            scrubbed_files_count += 1

        except UnidentifiedImageError:
            print(f'Malformed image: {obj.key}')

print(f'Done! {scrubbed_files_count} images scrubbed.')
