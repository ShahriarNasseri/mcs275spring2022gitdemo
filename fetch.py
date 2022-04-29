#!/usr/bin/env python3
"Retrieve a URL, displaying in terminal or saving to a file"
# MCS 275 Spring 2022 David Dumas
from urllib.request import urlopen
import argparse

parser = argparse.ArgumentParser("Retrieve a URL, displaying in terminal or saving to a file")
parser.add_argument("-o","--output",help="Output filename (default is to print to terminal)")
parser.add_argument("-v","--verbose",action="store_true",help="Verbose messages")
parser.add_argument("--no-default-http",action="store_true",help="Don't add http:// to URL without a protocol")
parser.add_argument("url",help="URL to retrieve")

args = parser.parse_args()

if '://' not in args.url:
    # Looks like URL has no protocol specifier
    if args.no_default_http:
        # Do not add http://
        if args.verbose:
            print("Warning: URL seems to have no protocol, and none will be assumed since --no-default-http was given.")
    else:
        # Add http://
        if args.verbose:
            print("Warning: URL seemed to have no protocol, so adding http:// prefix.")
            print("URL is is now:",args.url)
        args.url = 'http://' + args.url
        
if args.verbose:
    print("Retrieving URL '{}'".format(args.url))

# Retrieve
with urlopen(args.url) as res:
    data = res.read()
    if args.verbose:
        print("Received status code {} with body of size {} bytes.".format(
            res.status,
            len(data)
        ))
    if args.output is None:
        # Write to terminal
        cs = res.headers.get_content_charset()
        if cs:
            if args.verbose:
                print("Character set is '{}'".format(cs))
            s = data.decode(cs)
        else:
            if args.verbose:
                print("No character set specified in HTTP response")
            s = data.decode()
        if args.verbose:
            print("Printing response to terminal:")
        print(s)
    else:
        # Write to file
        if args.verbose:
            print("Saving response body to '{}'".format(args.output))
        with open(args.output,"wb") as fp:
            fp.write(data)
