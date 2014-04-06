#!/usr/bin/env python
import gnupg
import argparse
import sys

def clean_keys(gpg):
    secret_key = gpg.list_keys(True)[0]
    secret_key_uid = secret_key['uids'][0]

    for key in gpg.list_keys():
        if key['uids'][0] != secret_key_uid:
            gpg.delete_keys(key['fingerprint'])

def list_keys(gpg, private):
    print(gpg.list_keys(private))

if __name__ == "__main__":
    gpg = gnupg.GPG(gnupghome="gnupg")
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    parser_clean = subparsers.add_parser('clean')
    parser_list = subparsers.add_parser('list')
    parser_list.add_argument("--priv", action="store_true")

    parser_sign = subparsers.add_parser('sign')
    parser_sign.add_argument("key_id")

    args = parser.parse_args()

    if args.command == "clean":
        clean_keys(gpg)
    if args.command == "list":
        list_keys(gpg, args.priv)
    if args.command == "sign":
        sign_key(gpg, args.key_id)
