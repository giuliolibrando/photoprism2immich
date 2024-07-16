# photoprism2immich
`photoprism2immich` is a tool to migrate medial libraries from Photoprism to Immich.
The tools scan the original photoprism files folders and upload all the images and videos on Immich using API calls.

It has a built-in feature for skipping already uploaded files in case something goes wrong during upload, avoiding duplicates.  



# Usage
```
(photoprism-env) root@localhost:/photoprism2immich# photoprism2immich -h
usage: photoprism2immich [-h] --apikey APIKEY --baseapiurl BASEAPIURL --originals ORIGINALS [-l LOG] [-v]

Tool to migrate Photoprism library to Immich.

options:
  -h, --help            show this help message and exit
  --apikey APIKEY       API key for Photoprism server
  --baseapiurl BASEAPIURL
                        Base URL of the Photoprism server
  --originals ORIGINALS
                        Path to the originals folder
  -l LOG, --log LOG     Path to the log file
  -v, --version         show program's version number and exit
```


# Installation
```
pip install photoprism2immich
```
Example command:
```
photoprism2immich --apikey "aaaaaaaaaaaaaa" --baseapiurl "http://192.168.1.5:2283/api" --originals "/photoprism-originals"
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
