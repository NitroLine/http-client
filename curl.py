import client
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("url", type=str, help="url for request",
                    metavar="URL")
parser.add_argument("method", type=str, help="request method", choices=['GET', 'POST'],
                    metavar="METHOD")
parser.add_argument("-t", "--timeout", type=float, default=2, metavar='TIME', required=False,
                    help="wait answer timeout in seconds (default=2)")
args = parser.parse_args()

client = client.Client(args.url)
if args.method == 'POST':
    response = client.POST()
elif args.method == 'GET':
    response = client.GET()

client.close()
print(response)