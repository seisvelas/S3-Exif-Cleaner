import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bucket', default='flowcrypt-test', help='foo help')
parser.add_argument('-p', '--prefix', default='', help='foo help')
args = parser.parse_args()

print(args.bucket)