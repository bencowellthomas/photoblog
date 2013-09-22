'''
photoblog_tools - wordpress methods

Created on Sep 15, 2013
@author: Ben Cowell-Thomas
contact: http://bct.me
'''

import os
import pyexiv2
from datetime import datetime

# Package imports
import lib
import constants

class Blogpost():
    '''
    Class to contain all the data required for Blog posts
    When instantiated using an image file the class automatically extracts all the EXIF and IPTC data
    '''
    def __init__(self, filename, foldername):
        self.filename = filename
        self.foldername = foldername
        self.filepath = os.path.join(self.foldername, self.filename)
        self.post_title = self.get_clean_title()
        self.post_date = self.get_date_taken()
        if self.post_date == None:
            self.post_date = self.get_date_from_folder()
        self.terms = {}
        for each_taxonomy in constants.CUSTOM_TAXONOMYS:
            self.terms[each_taxonomy['taxonomy']] = self.get_metadata_from_file(each_taxonomy)
        
    def get_clean_title(self):
        '''
        Use name of JPEG file to create blog post title (without any numbers or special chars)
        '''
        no_extension = os.path.splitext(self.filename)[0]
        clean_title = []
        i = 0
        for char in no_extension:
            if (char.isdigit() == False):
                clean_title += char
                i += 1
        if (clean_title[0] == '_' or clean_title[0] == ' '):
            clean_title.pop(0)
        clean_title[0] = str(clean_title[0]).upper() #Title case
        clean_title = "".join(clean_title)
        clean_title = clean_title.replace("_", " ")
        return clean_title

    def get_date_taken(self):
        '''
        Returns the EXIF date taken value
        '''
        metadata = pyexiv2.ImageMetadata(self.filepath)
        metadata.read()
        try:
            # Try and get the time Photo was taken
            date = metadata['Exif.Photo.DateTimeOriginal'].value
        except:
            try:
                # If fail then get the last modified
                date = metadata['Exif.Image.DataTime'].value
            except:
                # Finally try and make date from folder name
                date = self.get_date_from_folder()
        return date

    def get_date_from_folder(self):
        ''' 
        Return the date from the folder name (a fail safe technique in case no EXIF is found).
        my JPEGs are arranged in folders named YYYY_MM format, so this may not work for you.
        '''
        date_from_folder = str(os.path.split(self.foldername)[1])
        date_array = date_from_folder.split('_')
        date = date_array[0] + '-' + date_array[1] + '-01 09:00:00'
        date_object = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        return date_object
    
    def get_metadata_from_file(self, taxonomy):
        '''
        Returns the specified taxonomy data from a file, returns none if Empty
        '''
        file_metadata = pyexiv2.ImageMetadata(os.path.join(self.foldername, self.filename))
        file_metadata.read()
        try:
            metadata = file_metadata[taxonomy['metadata']].value
        except:
            metadata = None
        # Strip out any newline escape characters
        if (metadata != None):
            metadata = [each_element.strip('\n') for each_element in metadata]
        return metadata
    
def post(source_folder,  subfolders=True, debug=False):
    '''
    Posts an folder full of images to Wordpress
    '''
    # Get images from folder
    if os.path.isdir(source_folder):
        print 'INFO: Posting to Wordpress'
        print 'INFO: Processing images from: ' + source_folder
        images = lib.get_from_folder(source_folder, subfolders, debug) 
        
        # Upload images to blog
        if (images != None):
            print 'INFO: Posting to: ' + constants.URL
            counter = 0
            if not debug:
                for each_image in images:
                    counter += 1
                    print 'INFO: Image ' + str(counter) + ' of ' + str(len(images))
                    lib.post_to_blog(each_image)
                print 'INFO: Upload complete. Uploaded ' + str(counter) + ' images'
    else:
        print 'ERROR: Folder does not exist'