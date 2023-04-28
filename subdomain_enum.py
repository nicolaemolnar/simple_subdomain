# Imports
import sys
import requests

import argparse

VERSION = 0.1

def parse_args():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description="Subdomain Enumerator")
    parser.add_argument("-d", "--domain", help="Domain to enumerate subdomains for", required=True)
    parser.add_argument("-v", "--version", help="Retrieve the version of the actual script", action="store_true", required=False)
    return parser.parse_args()

def get_subdomains_crt(domain):
    url = 'https://crt.sh/?q=%25.{}&output=json'.format(domain)
    subdomains = set()
    try:
        r = requests.get(url)
        if r.status_code == 200:
            for subdomain in r.json():
                subdomains.add(subdomain['name_value'].split('\n')[0])
            return subdomains
    except Exception as e:
        print("Unexpected error while obtaining subdomains for {}: {}".format(domain, e))
        sys.exit(1)

if __name__ == '__main__':
    args = parse_args()
    
    if args.v:
        print(VERSION)
        exit(0)
    
    try:
        subdomains = get_subdomains_crt(args.domain)
        if subdomains:
            for subdomain in subdomains:
                print(subdomain)
        else:
            print("No subdomains found for {}".format(args.domain))
        
        print("Script finshed successfully. Found {} subdomains".format(len(subdomains)))
    except Exception as e:
        print("Unexpected error: {}".format(e))
        sys.exit(1)
