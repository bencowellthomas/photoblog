'''
photoblog_tools - flickr methods

Created on Sep 15, 2013
@author: Ben Cowell-Thomas
contact: http://bct.me
'''

# Python imports
import os
import re
import sys
import flickrapi 
import urllib

# Package imports
import lib, constants, userinfo


class Flickr_photo():
    '''
    Class for flickr photographs and metadata
    '''
    def __init__(self, id, title, server, farm, secret):
        self.id = id
        self.title = title
        self.server = server
        self.farm = farm
        self.secret = secret
        self.orig_secret = None
        self.meta = []
        self.get_photo_info()
        self.url = self.get_url()
    

    def get_photo_info(self):
        '''
        Returns the original secret value
        '''
        flickr = flickrapi.FlickrAPI(userinfo.FLICKR_API_KEY, userinfo.FLICKR_API_SECRET)
        photo_xml = flickr.photos_getInfo(api_key = userinfo.FLICKR_API_KEY, photo_id = self.id)
        
        # Get Original Secret
        for child in photo_xml:
            self.orig_secret = child.get('originalsecret')
        
        # Get metadata
        for each_taxonomy in userinfo.CUSTOM_TAXONOMYS:
            if each_taxonomy['flickr'] != None:
                self.meta_temp = {'metadata': each_taxonomy['metadata']}
                self.raw_data = photo_xml.findall('.//' + each_taxonomy['flickr'])
                self.temp_list = []
                for each_element in self.raw_data:
                    self.temp_list.append(each_element.get('raw'))
                #self.meta_temp['value'] = (",".join(self.temp_list))
                self.meta_temp['value'] = ((self.temp_list))
                self.meta.append(self.meta_temp)        

    def get_url(self):   
        '''
        Returns a url for a given Flickr_photo object in the format :
        http://farm{farm-id}.staticflickr.com/{server-id}/{id}_{secret}.jpg
        '''
        url = 'http://farm' + str(self.farm) + '.staticflickr.com/' + str(self.server) + '/' + str(self.id) + '_' + str(self.orig_secret) + '_o.jpg'
        return url


def get_photos(download_folder, amount=0):
    '''
    Download images from Flickr and place into a folder
    '''
    # Authenticate the Flickr account  
    sys.stdout.write( 'INFO: Getting images from Flickr\n')
    flickr = flickrapi.FlickrAPI(userinfo.FLICKR_API_KEY, userinfo.FLICKR_API_SECRET)
    (token, frob) = flickr.get_token_part_one(perms='read')
    if not token: 
        print 'A browser window will open to allow you to authorise this application.' 
        raw_input("Press ENTER after you authorized this program")
    flickr.get_token_part_two((token, frob))
    
    # Get the photos
    photos = flickr.people_getPhotos(user_id = userinfo.FLICKR_ID)
    total_pages = int(photos.find('photos').attrib['pages'])
    total_number = int(photos.find('photos').attrib['total'])
    sys.stdout.write(  'INFO: Found ' +str(total_number) + ' photos, over ' + str(total_pages) + ' pages.\n')
    if (amount != 0):
        total_number = amount
    flickr_photos = []
    counter= 0

    current_page = 0
    photos = []
    sys.stdout.write('INFO: Collecting pages: ')
    while ((len(flickr_photos) < total_number) and (current_page <= total_pages)):
        current_page += 1
        each_page = flickr.people_getPhotos(user_id = userinfo.FLICKR_ID, page = current_page)
        photos = photos + (each_page.findall('.//photo'))
        sys.stdout.write('%0d.' %current_page)
        
    # Save photos and add Flickr Metadata 
    sys.stdout.write('\nINFO: Downloading to: ' + download_folder +'\n')
    for counter in range(0, total_number):
        flickr_photo = (Flickr_photo(photos[counter].get('id'), photos[counter].get('title'),photos[counter].get('server'), photos[counter].get('farm'), photos[counter].get('secret')))
        image = urllib.URLopener()
        dest_filename = flickr_photo.title + '.jpg'
        filename = image.retrieve(flickr_photo.url, os.path.join(download_folder,dest_filename))[0]
        lib.set_metadata_in_file(filename, flickr_photo)
        print 'INFO: ' + str(counter) + ' of ' + str(total_number) + ' - url: ' + flickr_photo.url + ', file: ' + os.path.split(filename)[1]
        lib.set_metadata_in_file(filename, flickr_photo)


    print 'INFO: Done'
    return download_folder
