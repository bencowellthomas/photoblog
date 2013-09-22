Photoblog
=========

A Python package with various tools for downloading images from flickr and posting them to a Photoblog running on Wordpress.

- Author: Ben Cowell-Thomas
- Contact: http://bct.me
- Created: 18/08/2013
- Updated: 20/09/2013

Dependencies:
-------------
- The metadata functions require the [pyexiv2](http://tilloy.net/dev/pyexiv2/)  library for Python. Some tips for compiling the library can be found [here](http://bct.me/tutorials/using-python-to-migrate-from-flickr-to-wordpress/#pyexiv2)
- The flickr download function requires the [flickrapi by Sybren Stüvel](http://stuvel.eu/flickrapi) library for Python

Usage:
------
- Add your Wordpress address, username, post type and taxonomy etc in the userinfo.py file
- Get an API key from Flickr [API key](http://www.flickr.com/services/api/misc.api_keys.html)
- Fill in the taxonomy information (see below)
- Import the `photoblog` package into Python

Taxonomy information:
---------------------
In the constants module you'll find a section for taxonomy information. This tells the module how the meta data between flickr, files and wordpress is related.
For example if you'd like flickr 'tags' to be stored in each jpeg file as IPTC 'keywords' and then posted via a custom taxonomy 'labels' you would add an array element like this:

    CUSTOM_TAXONOMYS = [{'name': 'label', 'taxonomy': 'labels', 'metadata': 'Iptc.Application2.Keywords', 'flickr': 'tag'}]

You can add as many of these structs as you like. Add the value 'None' for the flickr keyword if you don't want to associate the taxonomy with flickr (currently there's only support for flickr tags)
For example this is how my photoblog is set up :

    CUSTOM_TAXONOMYS = [{'name': 'label', 'taxonomy': 'photo_label', 'metadata': 'Iptc.Application2.Keywords', 'flickr': 'tag'},
                       {'name': 'set', 'taxonomy': 'photo_set', 'metadata': 'Iptc.Application2.Caption', 'flickr': None },
                       {'name': 'favourite', 'taxonomy':'photo_favourite', 'metadata': 'Iptc.Application2.SpecialInstructions', 'flickr': None}]

Modules:
--------
1. flickr.download()

	Downloads all photographs from a particular Flickr user and embeds flickr meta into the file meta data
	
	- Returns a folder name where the images have been saved.
	
	Arguments:
	- download folder (path) - folder in which to save images
	
	Optional:
	- amount (int) - max amount of images to retrieve. Set to 0 for all (default)

2. files.organize()

	Organises a folder filled with images, movies and thumbnails into dated folders (YYYY_MM). 
	This is especially useful for sorting out images from data cards etc.
	
	Arguments:
	- source folder (path) - folder to organise
	
	Optional:
	- debug (bool) - will analyse folder without moving images (default = False)
	
	**NOTE: Be careful this module will MOVE files, always make a backup first**

3. wordpress.post()

	Uploads a folder of images and creates individual blog posts for each, uses file meta data to create wordpress taxonomy.
	Use the constants module to set how you want the match file metadata with Wordpress taxonomy.
	
	Arguments:
	- source_folder (path) - folder to retrieve images from
	
	Optional Arguments:
	- subfolders (bool) - whether to process subfolders (default = True)
	- debug (bool) - if set to True will not post to Wordpress (default = False)
	
	**NOTE: Be careful this module could very quickly post hundreds of images to your blog. 
	Backup your Wordpress database BEFORE attempting to post.**

4. batch.process()

	For batch processing images from flickr to Wordpress
	
	Optional Arguments:
	- flickr (bool) - get images from flickr
	- subfolders (bool) - include subfolders
	- post (bool) - upload images to Wordpress

Notes:
------
- If you chose to first grab images from flickr then it'll first ask for your permission to authenticate (read only privs) with flickr
- My images are organised into dated folders in the format YYYY_MM so if no date is found in the EXIF the folder name will be used as a fallback

Todo:
-----
- ??

