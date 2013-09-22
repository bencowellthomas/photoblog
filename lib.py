'''
photoblog_tools - internal methods

Created on Aug 14, 2013
@author: Ben Cowell-Thomas
contact: http://bct.me
'''

# Python imports
import os
import pyexiv2
import xmlrpclib
import sys

# Package imports
import constants, wordpress, userinfo

def set_metadata_in_file(filename, flickr_photo):
    '''
    set_metadata_in_file
    '''
    file_metadata = pyexiv2.ImageMetadata(filename)
    file_metadata.read()
    flickr_meta = {}
    for each_taxonomy in flickr_photo.meta:
        key = each_taxonomy['metadata']
        file_metadata[key] = pyexiv2.IptcTag(key, each_taxonomy['value'])
        file_metadata.write()
        #flickr_meta[each_taxonomy['flickr']] = self.get_metadata_from_file(each_taxonomy)

def check_wp_terms(server, term, taxonomy):
    '''
    Return Terms with Worpdress ID numbers ready for posting
    Also adds new Terms to your wordpress taxonomy values if required
    '''
    # Get all the terms
    terms_response = server.wp.getTerms(userinfo.BLOGID, userinfo.USERNAME, userinfo.PASSWORD, taxonomy)
    exists = False
    
    # cycle through all the terms and see if any match our term
    for each_term in terms_response:
        if ((each_term['taxonomy'] == taxonomy) and (each_term['name'].title() == term.title())):
            exists = True
            wp_term = each_term['term_id']
            
    # If term doesn't exist then attempt to add it to Wordpress
    if exists == False:
        term = str(term).title() #Title case
        content = {'taxonomy': taxonomy, 'name': term}
        print 'INFO: Adding ' + taxonomy + ': ' + term
        wp_term = '---'
        add_term_response = server.wp.newTerm(userinfo.BLOGID, userinfo.USERNAME, userinfo.PASSWORD, content)
        wp_term = add_term_response
    return wp_term
    

def is_string_empty(string):
    '''
    Sometimes IPTC / XMP data can contain empty strings, this function tests a string and returns True if string is  or pure whitespace
    '''    
    result = True
    for each_char in string:
        if (each_char != ' '): result = False
    return result

def strip_trailing_whitespace(string):
    '''
    Sometimes terms contain trailing whitespace, Wordpress trims this so we need to as well to avoid duplicate terms being added
    '''
    processed = False
    while (processed == False):
        if string[-1] != ' ':
            processed = True
        else:
            string = string[:-1]
            if (string[-1] != ' '): processed = True
    return string

def query_yes_no(question, default="yes"):
    ''''Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    '''
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

def strip_carriage_return(string):
    '''
    Sometimes terms contain newline escape characters, Wordpress trims this so we need to as well to avoid duplicate terms being added
    '''
    string = string.replace('\n','')
    return string

def post_to_blog(image):
    '''
    Post via XML-RPC
    '''
    server = xmlrpclib.ServerProxy(userinfo.URL)
    
    # Upload the image
    print 'INFO: Uploading: ' + image.filename
    data = {'name': image.post_title + '.jpg','type': 'image/jpg'}
    with open(image.filepath, 'rb') as img:
        data['bits'] = xmlrpclib.Binary(img.read())
        pass
    image_attachment = server.wp.uploadFile(userinfo.BLOGID, userinfo.USERNAME, userinfo.PASSWORD, data)
    
    # Create post_images content
    post_content = '<img src="' + image_attachment['url'] + '">'

    # Get term ID numbers and create any terms that don't exist
    print 'INFO: Processing taxonomy'
    wp_terms = {}
    for each_taxonomy, terms in image.terms.iteritems():
        wp_term_ids = []
        if terms != None:
            for each_term in terms:
                if is_string_empty(each_term) == False:
                    each_term = strip_trailing_whitespace(each_term)
                    each_term = strip_carriage_return(each_term)
                    wp_term_ids.append(check_wp_terms(server, each_term, each_taxonomy))
        wp_terms[each_taxonomy] = wp_term_ids
        
    # Prepare the content dictionary
    content = { 'post_type' : userinfo.POST_TYPE,
               'post_status' : 'publish',
               'post_title' : image.post_title,
                'post_date' : image.post_date,
                'terms' : wp_terms,
                'post_content' : post_content,
                'post_thumbnail' : image_attachment['id'],
                }
    print 'INFO: Creating blog post' 
    post_id = server.wp.newPost(userinfo.BLOGID, userinfo.USERNAME, userinfo.PASSWORD, content)
    print 'INFO: Succcess, Post title: ' + image.post_title

def get_from_folder(path, subfolders=True, debug=False):
    '''
    Returns an array of Blogpost objects from a given folder
    '''
    images = []
    i = 0
    if not (os.path.exists(path)):
        print 'ERROR: Path not found'
        return
    for root, folders, files in os.walk(path):
        for each_file in files:
            if (os.path.splitext(each_file)[1] in constants.VALID_EXTENSIONS):
                images.append(wordpress.Blogpost(each_file, root))
                if debug: print images[i].post_date
                i += 1
    return images
    