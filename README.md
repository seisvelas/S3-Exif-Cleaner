### Setup

```bash
git clone https://github.com/seisvelas/S3-Exif-Cleaner.git && cd S3-Exif-Cleaner
pip3 install -r requirements.txt
chmo
```

Note: Pillow dependency breaks on Apple Silicon, to make it work follow the instructions here:
https://github.com/python-pillow/Pillow/issues/5093

```bash
mv .env.example .env
```

Now put your AWS information into .env (`API_KEY_AWS_S3_ID` & `API_KEY_AWS_S3_SECRET`).

That's it, you're ready to start!

### Usage

```bash
alex@mac s3_exif_cleanser % python3 s3_cleanse.py -h
usage: s3_cleanse.py [-h] [-b BUCKET] [-p PREFIX]

optional arguments:
  -h, --help            show this help message and exit
  -b BUCKET, --bucket BUCKET
                        Name of S3 bucket
  -p PREFIX, --prefix PREFIX
                        (optional) Only wash images starting with this prefix
```

Let's say you want to wash images in a bucket called `myBusiness`, but only wanted to wash images in the `embarassingPhotos/` prefix. In that case, you'd invoke `s3_exif_cleanser` like so:

```bash
alex@mac s3_exif_cleanser % python3 s3_cleanse.py -b myBusiness -p 'embarassingPhotos'
Cleansing EXIF data on: embarassingPhotos/me_in_jamaica.jpg
Cleansing EXIF data on: embarassingPhotos/forgot_my_shirt_lol.jpg
Done! 2 images scrubbed.
```

Viola! The images are now EXIF free.
