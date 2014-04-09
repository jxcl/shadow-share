import os
import pathlib
import json
import gnupg
from os import path

CONFIG_DIRECTORY = pathlib.Path(path.expanduser("~")) / ".config" / "shadow_share"

def load_or_create_config():

    if CONFIG_DIRECTORY.exists():
        config_file = CONFIG_DIRECTORY / "config.json"
        if config_file.exists():
            config = json.load(config_file.open('r'))
        else:
            config = new_config(CONFIG_DIRECTORY)
        return config

    else:
        CONFIG_DIRECTORY.mkdir(parents=True)
        return new_config(CONFIG_DIRECTORY)

def ask_for_key(gpg):
    private_keys = gpg.list_keys(True)

    if len(private_keys) == 0:
        print("There are no private keys in your keyring.\n",
              "We need to generate some.")
        name_real = input("Real name: ")
        name_email = input("Email address: ")
        key_length = 4096

        key_properties = gpg.gen_key_input(name_real=name_real,
                                             name_email=name_email,
                                             key_length=key_length)
        key = gpg.gen_key(key_properties)
        key_fingerprint = key.fingerprint
        key_id = gpg.list_keys(True)[0]['keyid']

        return (key_id, key_fingerprint)

    elif len(private_keys) == 1:
        print("We are automatically using the only private key you have.")
        key_fingerprint = gpg.list_keys(True)[0]['fingerprint']
        key_id = gpg.list_keys(True)[0]['keyid']
        return (key_id, key_fingerprint)

    else:
        print("You have more than one private key. Which one would you like"
              "to use with ShadowShare?")
        for i, key in enumerate(private_keys):
            print("{}. Name: {}\n   Fingerprint: {}".format(i,
                                                            key['uids'][0],
                                                            key['fingerprint']))
        selection = int(input("Selection: "))

        key_fingerprint = private_keys[selection]['fingerprint']
        key_id = private_keys[selection]['keyid']
        return (key_id, key_fingerprint)

def new_config(CONFIG_DIRECTORY):
    home_directory = pathlib.Path(path.expanduser("~"))
    config_file = CONFIG_DIRECTORY / "config.json"

    gpg_spiel = '''\
                   ShadowShare uses GPG blah blah blah.'''
    answer = input("Do you want to use your normal GPG keyring with ShadowShare? [y/N]")

    if answer.lower() == 'y':
        gnupg_home = home_directory / ".gnupg"
    else:
        gnupg_home = CONFIG_DIRECTORY / "gnupg"

    gpg = gnupg.GPG(gnupghome=str(gnupg_home))

    key_info = ask_for_key(gpg)

    config = {
        "gnupghome": str(gnupg_home),
        "key_id": key_info[0],
        "fingerprint": key_info[1]
              }

    with config_file.open('w') as fp:
        fp.write(json.dumps(config))

    return config

def add_user_name(user_name):
    config_file = CONFIG_DIRECTORY / "config.json"

    config = json.load(config_file.open("r"))
    config['user_name'] = user_name
    json.dump(config, config_file.open("w"))
