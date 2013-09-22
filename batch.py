'''
photoblog_tools - batch process methods

Created on Sep 15, 2013
@author: Ben Cowell-Thomas
contact: http://bct.me
'''
import flickr
import wordpress
import constants

def process(process_folder, flickrdownload=False, subfolders=True, post=True):
    
    # Get images from Flickr
    if flickrdownload:
        source_folder = flickr.get_photos(amount=0)
    else:
        source_folder = process_folder

    # Post images to wordpress
    if post: 
        wordpress.post(source_folder, subfolders)
    
if __name__ == '__main__':
    process(flickrdownload=True, subfolders=True, post=False)