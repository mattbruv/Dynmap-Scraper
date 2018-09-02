# Dynmap Scraper
A set of scripts that will download images that are inside a user-defined area from a Dynmap server.

The purpose is for this script to run on a schedule, effectively creating many snapshots of the state of a world. The snapshots can be used to create a visual high-definition timelapse of the evolution of a server. The only limits are your hard-drive space.

## Example GIF of two frames
![Example](https://i.imgur.com/bSO72Os.gif)
This is an example of two scrapes taken one day apart at the start of a new server.


## How to use
1. Rename `config.default.yaml` to `config.yaml` and fill out appropriate settings.
If the a given bound falls outside of a natural image border, the view will be expanded to include all areas.
2. Run `python download.py`. This will scrape the dynmap and create a zip file (named with timestamp) of all the images in your defined area and save it in the current directory.
3. You can optionally create a composite image by unzipping a folder and running `python imgcompile.py [Name of folder]` to create a combined image from all the sub-images in that snapshot.
The code for `imgcompile.py` is hacky and needs to be refactored for serious use in the future.

## Contributing
I am happy to accept any contributions that improve these tools, so just submit a pull request if you're interested!

## TODO:
* Upload `.zip` file to cloud hosting (Google Drive?)
* Figure out how to host it somewhere else for free and forget about it while it runs forever