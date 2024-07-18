#!/usr/bin/python3
import os
import argparse
from photoprism2immich.migrator import Migrator
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

        if response.status_code in [200, 201]:
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
    # Parsing degli argomenti da linea di comando con subcommands
    parser = argparse.ArgumentParser(description='Tool to manage Photoprism library with Immich.')
    subparsers = parser.add_subparsers(dest='command', required=True, help='Sub-command to execute')

    # Comando migrate-library
    migrate_parser = subparsers.add_parser('migrate-library', help='Migrate Photoprism library and albums to Immich.')
    migrate_parser.add_argument('--apikey', help='API key for Immich server', required=True)
    migrate_parser.add_argument('--baseapiurl', help='Base URL of the Immich server', required=True)
    migrate_parser.add_argument('--originals', help='Path to the originals folder', required=True)
    migrate_parser.add_argument('-l', '--log', help='Path to the log file', default='uploaded_files.log')

    # Comando migrate-album
    album_parser = subparsers.add_parser('migrate-album', help='Migrate a specific album to Immich.')
    album_parser.add_argument('--photoprism_url', help='URL of the Photoprism server', required=True)
    album_parser.add_argument('--photoprism_user', help='Username for Photoprism', required=True)
    album_parser.add_argument('--photoprism_password', help='Password for Photoprism', required=True)
    album_parser.add_argument('--immich_url', help='Base URL of the Immich server', required=True)
    album_parser.add_argument('--immich_api', help='API key for Immich server', required=True)
    album_parser.add_argument('--album', help='Specific album to migrate', default='ALL')
    album_parser.add_argument('-l', '--log', help='Path to the log file', default='uploaded_albums.log')

    # Parsing degli argomenti
    args = parser.parse_args()

    if args.command == 'migrate-library':
        upload_files_from_path(args.originals, args.apikey, args.baseapiurl, args.log)
    if args.command == 'migrate-album':
        migrator = Migrator(args.photoprism_url, args.photoprism_user, args.photoprism_password, args.immich_url, args.immich_api)
        migrator.migrate_album(args.album)

if __name__ == "__main__":
    main()
