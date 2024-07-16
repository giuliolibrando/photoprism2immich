#!/usr/bin/python3

import requests
import os
from datetime import datetime
import argparse
from importlib.metadata import version

# Funzione per gestire l'upload dei file
def upload(file, api_key, base_url, log_file):
    print(f"Uploading file: {file}")
    stats = os.stat(file)

    headers = {
        'Accept': 'application/json',
        'x-api-key': api_key
    }

    data = {
        'deviceAssetId': f'{file}-{stats.st_mtime}',
        'deviceId': 'python',
        'fileCreatedAt': datetime.fromtimestamp(stats.st_mtime),
        'fileModifiedAt': datetime.fromtimestamp(stats.st_mtime),
        'isFavorite': 'false',
    }

    files = {
        'assetData': open(file, 'rb')
    }

    try:
        response = requests.post(
            f'{base_url}/assets', headers=headers, data=data, files=files)

        if response.status_code in [200, 201]:  # Success codes: 200 (OK), 201 (Created)
            print("Upload successful!")
            print(response.json())
            log_uploaded_file(file, log_file)
        else:
            print(f"Failed to upload asset: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Error uploading file: {file}")
        print(e)

# Funzione per registrare i file caricati nel log
def log_uploaded_file(file, log_file):
    with open(log_file, 'a') as log:
        log.write(file + '\n')

# Funzione per caricare i file già registrati dal log
def load_uploaded_files(log_file):
    uploaded_files = set()
    if os.path.exists(log_file):
        with open(log_file, 'r') as log:
            for line in log:
                uploaded_files.add(line.strip())
    return uploaded_files

# Funzione per caricare i file da una directory specificata
def upload_files_from_path(path, api_key, base_url, log_file):
    print(f"Scanning directory: {path}")
    uploaded_files = load_uploaded_files(log_file)

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path in uploaded_files:
                print(f"Skipping already uploaded file: {file_path}")
                continue
            file_extension = os.path.splitext(file)[1].lower()
            if file_extension in ['.jpg', '.jpeg', '.heic', '.mov', '.mp4', '.png', '.m4v']:
                upload(file_path, api_key, base_url, log_file)
            else:
                print(f"Skipping unsupported file type: {file_path}")

# Funzione principale del programma
def main():
    # Parsing degli argomenti da linea di comando
    parser = argparse.ArgumentParser(description='Tool to migrate Photoprism library to Immich.')
    parser.add_argument('--apikey', help='API key for Photoprism server', required=True)
    parser.add_argument('--baseapiurl', help='Base URL of the Photoprism server', required=True)
    parser.add_argument('--originals', help='Path to the originals folder', required=True)
    parser.add_argument('-l', '--log', help='Path to the log file', default='uploaded_files.log')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {version("photoprism2immich")}')
    args = parser.parse_args()

    # Verifica se i parametri obbligatori sono stati forniti
    if not (args.apikey and args.baseapiurl and args.originals):
        parser.error('The following arguments are required: --apikey, --baseapiurl, --originals')

    # Eseguire l'upload dei file dalla cartella originals
    upload_files_from_path(args.originals, args.apikey, args.baseapiurl, args.log)

if __name__ == "__main__":
    main()
