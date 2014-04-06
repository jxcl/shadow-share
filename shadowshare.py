#!/usr/bin/env python3.4

from client import client
import argparse


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='command')

parser_store = subparsers.add_parser('store')
parser_store.add_argument('user_name')
parser_store.add_argument('file_name')

parser_retrieve = subparsers.add_parser('retrieve')
parser_retrieve.add_argument('user_name')

parser_register = subparsers.add_parser('register')
parser_register.add_argument('user_name')

parser_get_key = subparsers.add_parser('get_key')
parser_get_key.add_argument('user_name')
args = parser.parse_args()

if args.command == "store":
    client.store(args.user_name, args.file_name)
elif args.command == "retrieve":
    client.retrieve(args.user_name)
elif args.command == "register":
    client.register(args.user_name)
elif args.command == "get_key":
    client.get_key(args.user_name)
