'''
photoblog_tools - file methods

Created on Sep 15, 2013
@author: Ben Cowell-Thomas
contact: http://bct.me
'''

import os
import constants
import lib
import time
import datetime
import shutil
import sys

def __get_date_created(file_path):
    '''
    Returns the EXIF date taken value
    '''
    date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).year, datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).month
    # Don't use exif, use date created
    return date

def __get_folder_name(file_path):
    date = __get_date_created(file_path)
    folder = (str(date[0]) + '_' +str(date[1]).zfill(2))
    return folder

def __create_folder(the_path):
    if not os.path.isdir(the_path):
        # Create the folder
        os.makedirs(the_path)
        print 'Creating: ' + the_path
    else:
        pass
    return

def fix_renames(source_folder):
    # Utility to strip out the 'rename' postfix on files
    for root, folders, files in os.walk(source_folder):
        for each_file in files:
            if each_file.find('_rename') > 0:
                newname = each_file.replace('_rename','')
                os.rename(os.path.join(root, each_file),os.path.join(root,newname))

def __move_files(file_path, destination_path):
    '''
    Internal Method to move files, if a duplicate is found will add a postfix to the name
    '''
    if not os.path.isdir(destination_path):
        __create_folder(destination_path)
    filename = os.path.split(file_path)[1]
    if os.path.isfile(os.path.join(destination_path, filename)): # Check if the file name exists, if so then add postfix to the name
        filename = (os.path.splitext(filename)[0] + '_rename' + os.path.splitext(filename)[1])
        destination_path = os.path.join(destination_path, filename)
    try: # Move file
        shutil.move(file_path, destination_path)
        sys.stdout.write('INFO: Moving ' + file_path + '\n')
        sys.stdout.write('INFO: to ' + destination_path + '\n')
    except:
        sys.stdout.write('ERROR: Cannot move ' + file_path + ', to ' + destination_path)
        
def organise(source_folder, debug=False):
    '''
    Organise a folder full of images, movies etc from a camera card and sort them into dated folders.
    These folders will be under the folder named in constants.PROCESS_FOLDER
    If it finds any duplicate names they'll be renamed with the postfix _rename
    
    NOTE: This code MOVES files, it can make a huge mess so make sure you're working using a backup.
    '''
    if lib.query_yes_no('Are you sure you want to Organise: ' + source_folder):
        counter = 0
        photo_extensions = (constants.VALID_EXTENSIONS + constants.RAW_EXTENSIONS)
        process_folder = os.path.join(source_folder, constants.ORGANISE_FOLDER)
        for root, folders, files in os.walk(source_folder):
            folder_minus_source_folder = ((root.split(source_folder))[1])
            proceed = True
            if folder_minus_source_folder: # set a flag to proceed if we're sure we're not in the organise folder
                proceed = folder_minus_source_folder.split(os.path.sep)[0] != constants.ORGANISE_FOLDER
            if proceed:
                    for each_file in files:
                        file_path = os.path.join(root, each_file)
                        if (os.path.splitext(each_file)[1] in photo_extensions): # Photo files
                            destination_path = os.path.join(process_folder, __get_folder_name(file_path))
                            if not debug:
                                __move_files(file_path, destination_path)
                                counter +=1
                        elif (os.path.splitext(each_file)[1] in constants.MOVIE_EXTENSIONS): # Movie Files
                            destination_path = os.path.join(process_folder, constants.MOVIE_FOLDER)
                            if not debug:
                                __move_files(file_path, destination_path)
                                counter +=1
                        else:
                            if each_file not in constants.IGNORE_FILES: # Misc files
                                destination_path = os.path.join(process_folder, constants.MISC_FOLDER)
                                if not debug:
                                    __move_files(file_path, destination_path)
                                    counter +=1
        sys.stdout.write('INFO: Moved ' + str(counter) + ' files.\n')
                                    
                                    