'''
photoblog_tools - usernames and API keys

NOTE: Change this filename to userinfo.py before importing

Created on Sept 21st, 2013
@author: Ben Cowell-Thomas
contact: http://bct.me
'''  

'''
Wordpress information
'''
USERNAME = '<username>'
PASSWORD = '<password>'
URL = '<blog url>/xmlrpc.php'
POST_TYPE = '<post_type>'
BLOGID = 1 # Currently ignored by XMLRPC API

'''
Flickr
'''
FLICKR_ID = '<flickr ID>'
FLICKR_API_KEY = '<flickr API Key>'
FLICKR_API_SECRET = '<flickr API Secret>'

'''
Taxonomy information
Array of Structs for Taxonomy terms in Wordpress and the associated metadata found within the IPTC data and Flickr
see README.md for an explanation
'''
CUSTOM_TAXONOMYS = [{'name': 'label', 'taxonomy': '<taxonomy>', 'metadata': '<meta>', 'flickr': 'tag'}]