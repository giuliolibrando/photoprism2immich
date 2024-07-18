from photoprism2immich.photoprism_api import PhotoprismApi
from photoprism2immich.immich_api import ImmichApi
import click
import os

class Migrator:
    def __init__(self, photoprism_url, photoprism_user, photoprism_password, immich_url, immich_api, log_folder=None):
        self.pp_api = PhotoprismApi(photoprism_url, photoprism_user, photoprism_password)
        self.im_api = ImmichApi(immich_url, immich_api)
        self.log_folder = log_folder or '.'  # Use current directory if log_folder is not specified
        os.makedirs(self.log_folder, exist_ok=True)  # Ensure log_folder exists

    def migrate_album(self, album='ALL'):
        click.echo(f"Migrating album: {album if album != 'ALL' else 'ALL'}")

        if album == 'ALL':
            albums_data = self.pp_api.get_all_albums_data()
            for album_data in albums_data:
                if not self.album_already_migrated(album_data):
                    self._migrate_single_album(album_data)
        else:
            album_data = self.pp_api.get_album_data(album)
            if album_data:
                if not self.album_already_migrated(album_data):
                    self._migrate_single_album(album_data)
                else:
                    click.echo(f"Album '{album_data.get('Title')}' (UID: {album}) already migrated to Immich.")
            else:
                click.echo(f"Album with id {album} not found in Photoprism.")

        click.echo("Migration complete.")

    def album_already_migrated(self, album_data):
        album_uid = album_data.get("UID")
        album_title = album_data.get("Title")
        log_file = os.path.join(self.log_folder, 'migrated_albums.log')

        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                migrated_albums = f.read().splitlines()
                if f'{album_uid}-{album_title}' in migrated_albums:
                    return True

        return False

    def _migrate_single_album(self, album_data):
        album_uid = album_data.get("UID")
        album_title = album_data.get("Title")

        click.echo(f"Migrating album '{album_title}' (UID: {album_uid})")

        # Step 1: Retrieve photos in the album from Photoprism
        photo_file_list = self.pp_api.get_photo_files_in_album(album_uid)

        # Step 2: Match photos in Immich
        matching_uids = self._get_matching_uids(photo_file_list)

        matches_uids = matching_uids.get("uids")
        files_not_found = matching_uids.get("files_not_found")

        self._summary(matches_uids, files_not_found)

        # Step 3: Create album in Immich and assign assets
        self.im_api.create_album(album_title, matches_uids)

        # Step 4: Log the migrated album
        self.log_migrated_album(album_uid, album_title)

    def log_migrated_album(self, album_uid, album_title):
        log_file = os.path.join(self.log_folder, 'migrated_albums.log')
        with open(log_file, 'a') as f:
            f.write(f"{album_uid}-{album_title}\n")

    def _get_matching_uids(self, photo_file_list):
        matches_uids = []
        files_not_found = []

        for photo_file in photo_file_list:
            uri_components = photo_file.split("/")
            filename = uri_components[-1]
            search_result = self.im_api.search_metadata(originalFileName=filename)

            items = search_result.get("assets", {}).get("items", [])

            matches_paths = []

            if len(items) == 0:
                files_not_found.append(photo_file)
                click.echo(f"No match: {photo_file} in Immich")
            else:
                for item in items:
                    if self._is_same_path_ending(uri_components, item.get("originalPath").split("/")):
                        matches_uids.append(item.get("id"))
                        matches_paths.append(item.get("originalPath"))

                if len(matches_paths) == 1:
                    click.echo(f"Added a match: {filename} (pp: {photo_file}, im: {matches_paths[0]})")
                elif len(matches_paths) > 1:
                    click.echo(f"Added {len(matches_paths)} matches for {filename} in Immich")
                    click.echo(f"Original path in Photoprism: {photo_file}")
                    click.echo("Possible matches in Immich:")
                    for match in matches_paths:
                        click.echo(f" - {match}")
                else:
                    files_not_found.append(photo_file)
                    click.echo(f"No match: {photo_file} in Immich")

        return {
            "uids": matches_uids,
            "files_not_found": files_not_found,
        }

    def _is_same_path_ending(self, pp_path, im_path):
        pp_path_depth = len(pp_path)
        im_path_depth = len(im_path)
        min_path_depth = min(pp_path_depth, im_path_depth)

        pp_path_components = pp_path[-min_path_depth:]
        im_path_components = im_path[-min_path_depth:]

        return pp_path_components == im_path_components

    def _summary(self, matches_uids, files_not_found):
        if files_not_found:
            click.echo(f"Images found in Immich: {len(matches_uids)}")
            click.echo("Images not found in Immich:")
            for file in files_not_found:
                click.echo(f" - {file}")
        else:
            click.echo("Migration successful!")
            click.echo(f"All images found in Immich: {len(matches_uids)}")
