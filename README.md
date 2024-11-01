![PyPI Downloads](https://static.pepy.tech/badge/photoprism2immich)

# photoprism2immich
`photoprism2immich` is a tool to migrate media libraries and albums from Photoprism to Immich.
The tools scan the original photoprism files folders and upload all the images and videos on Immich using API calls. It also query Photoprism API to retrieve albums photo and create the albums on Immich.

It has a built-in feature for skipping already uploaded files and albums in case something goes wrong during upload, avoiding duplicates.  

The `migrate-album` and `migrate-favorites` features draws heavy inspiration from  [ppim-migrator](https://github.com/v411e/ppim-migrator) by user [v411e](https://github.com/v411e)

# Usage
```
(photoprism-env) root@pve:/localhost# photoprism2immich -h
usage: photoprism2immich [-h] {migrate-library,migrate-album,migrate-favorites} ...

Tool to manage Photoprism library with Immich.

positional arguments:
  {migrate-library,migrate-album,migrate-favorites}
                        Sub-command to execute
    migrate-library     Migrate Photoprism library and albums to Immich.
    migrate-album       Migrate a specific album to Immich.
    migrate-favorites   Migrate favorite photos to Immich.

options:
  -h, --help            show this help message and exit
```
migrate-library help:
```
(photoprism-env) root@pve:/localhost# photoprism2immich migrate-library -h
usage: photoprism2immich migrate-library [-h] --apikey APIKEY --baseapiurl BASEAPIURL --originals ORIGINALS [-l LOG]

options:
  -h, --help            show this help message and exit
  --apikey APIKEY       API key for Immich server
  --baseapiurl BASEAPIURL
                        Base URL of the Immich server
  --originals ORIGINALS
                        Path to the originals folder
  -l LOG, --log LOG     Path to the log file
```
migrate-album help:
```
(photoprism-env) root@pve:/localhost# photoprism2immich migrate-album -h
usage: photoprism2immich migrate-album [-h] --photoprism_url PHOTOPRISM_URL --photoprism_user PHOTOPRISM_USER --photoprism_password PHOTOPRISM_PASSWORD
                                       --immich_url IMMICH_URL --immich_api IMMICH_API [--album ALBUM] [-l LOG]

options:
  -h, --help            show this help message and exit
  --photoprism_url PHOTOPRISM_URL
                        URL of the Photoprism server
  --photoprism_user PHOTOPRISM_USER
                        Username for Photoprism
  --photoprism_password PHOTOPRISM_PASSWORD
                        Password for Photoprism
  --immich_url IMMICH_URL
                        Base URL of the Immich server
  --immich_api IMMICH_API
                        API key for Immich server
  --album ALBUM         Specific album to migrate
  -l LOG, --log LOG     Path to the log file
```

# Installation
```
pip install photoprism2immich
```
# Usage
Example command for migrating library:
```
photoprism2immich migrate-library --apikey "aaaaaaaaaaaaaa" --baseapiurl "http://immich.local:2283/api" --originals "/photoprism-originals"
```
**IMPORTANT**: **if you want to import albums and favorites, first change the default Immich path library from /YYYY/MM/DD to /YYYY/MM**

Example command for migrating ALL albums  (if you want to migrate one album only specify here):
```
photoprism2immich migrate-album --photoprism_url="http://photoprism.local:20800/" --photoprism_user="user" --photoprism_password="password" --immich_url="http://immich.local:2283" --immich_api="aaaaaaaaaaaaaa" --album ALL
```

Example command for migrating favorites:
```
photoprism2immich migrate-favorites --photoprism_url="http://photoprism.local:20800/" --photoprism_user="user" --photoprism_password="password" --immich_url="http://immich.local:2283" --immich_api="aaaaaaaaaaaaaa"
```

# Build yourself

Clone the repo
```
git clone https://github.com/giuliolibrando/photoprism2immich.git
```
enter into the folder
```
cd photoprism2immich
```
source the virtualenv
```
source photoprism-env/bin/activate
```
install via pip
```
pip install .
