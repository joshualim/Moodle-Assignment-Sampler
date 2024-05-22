#!/usr/bin/env python
# coding: utf-8

# # Moodle Assignment Sampling
# ## Instructions
# 1. From Moodle download the marksheet (Bath version) and all the submissions to this folder (if there are multiple submissions per students then you MUST make sure "submissions downloaded in folders" is checked).
# 2. Update the first "Initial setup" code block
#     - update filenames for marksheet and submissions.
#     - update the unit code prefix naming convention as needed.
# 3. Run the script!
# 
# ## What does this script do?
# For each "grade range" you specify:
# 1. A text summary output is produced
#     - number of scripts in the range
#     - candidates username and initials for scripts in that range
# 2. Scripts are moved to a samples folder and renamed as {UNIT CODE}_{S1_23-24}__{GRADE}_sample{n}
# 
# The following are looked at:
# - All the fails
# - All the firsts
# - All borderline grade (+/-1 to a grade boundary)
# - A ‘representative’ sample in between 
# 
# ## How does this script work?
# This is script has 3 parts and is written in 3 code blocks
# 1. Initial setup script (e.g. set filenames, unit code prefixes) - **you will need to update this every time you run the script**
# 2. The functions/methods for sampling - this contains the logic for the sampling.
# 3. Run the sampling - this actually performs the sampling and generates the reports. It also contains some hard coded values you ***might*** want to tweak.
# 
# 
# ## What still needs to be done?
# - Zip everything up at the end 
# - tidy up code: refactor find_samples into make_sample
# - sort out the numbering suffix for repeated entries. Currently the numbering doesn't make much sense.
# - write summary results to text file
# 
# ## About
# Provided as-is, but contact <a href="mailto:jajhl20@bath.ac.uk" target="_blank">Josh Lim</a> for questions.
# 
# <p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><span property="dct:title">Moodle Assignment Sampler</span> by <span property="cc:attributionName">Josh Lim</span> is marked with <a href="https://creativecommons.org/publicdomain/zero/1.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC0 1.0</a> - Go forth and remix without attribution ;)</p>
# 
# version 1.0

# In[ ]:


"""
Initial setup
- Please edit this section 
"""

# Name of downloaded Moodle marksheet
GradesCSV = 'GradesMarksheet.csv'

# Name of downloaded zip file (with submissions downloaded in folders)
originalZip = 'OriginalFilesDownload_Folders.zip'


# set unit code for prefixes throughout
unitCode = "MEXXXXX"

# set whether submission are downloaded in folders (True/False)
#      select True if submissions are in folders (typically if there a multiple files per student)
#      select False if submissions are NOT in folders (if there is only one file per student)
submission_in_folders = True    
# submission_in_folders = False    

# Set sample base name
sampleName = unitCode + '_S1_23-24_'

# Specify the base directory where your folders will be moved to
originalsPath = unitCode +'_OriginalSubmissions'
samplesPath = unitCode +'_Samples'


# In[ ]:


import os
import zipfile
import shutil
import math

#extract submissions to $originalsPath
with zipfile.ZipFile(originalZip, 'r') as zip_ref:
    zip_ref.extractall(originalsPath)
    
# Create a new folder for the samples
os.makedirs(samplesPath, exist_ok=True)

# Get a list of all folder names
folder_names = os.listdir(originalsPath)

# load the marksheet
import pandas as pd
df = pd.read_csv(GradesCSV)
df = df.dropna(subset=['Grade']) # drop any students without grades (these are sometimes erroneously listed in Moodle)
total_scripts = df.shape[0]

def get_initials(full_name):
    """Add a column for the initials"""
    # Split the name by spaces and get the first letter of each part
    initials = ''.join([name[0] for name in full_name.split()])
    return initials.upper()  # Return the initials in uppercase

df["Initials"] = df['Full name'].apply(get_initials)


def find_samples(dataframe, sample_min_value, sample_max_value):
    """
    create a new dataframe from the unsampled scores with results between sample_min_value and sample_max_value
    """
    condition = dataframe['Grade'].between(sample_min_value, sample_max_value)
    new_df = dataframe[condition].copy()
    
    return new_df

def summarise_result(dataframe,label):
    """
    Output a text summary of sampling 
    """
    number_students = dataframe.shape[0]
        
    # print outputs to terminal
    print(f"{label}:{number_students}")
    print(dataframe[['Username', 'Initials']].to_string(index=False)) # print table of usernames and initials
    # print(dataframe[['Username', 'Initials' , 'Grade']].to_string(index=False)) # print table of usernames, initials, grade
    print()

def copy_samples(dataframe):
    """
    Copy all listed samples in the dataframe to samplesPath directory and rename to sampleName_{score}_sample{n}
    """
    names_list = dataframe['Full name'].tolist() # get list of Full names for look up files
    scores = dataframe['Grade'].tolist()         # get list of scores for appending into file name
    
    # loop over all firsts: and copy contents to Samples folder 
    for loopindex, fullname in enumerate(names_list):
    
        # Find source diretory/file based on "Full name" string (e.g., 'John Smith')
        folder_index = [index for index, name in enumerate(folder_names) if fullname in name]
        
        if not folder_index: #skip any missing files
            continue
        else:
            source_dir = os.path.join(originalsPath, folder_names[folder_index[0]])
            
            if submission_in_folders:         # if all student submissions are in separate folders (multiple files per student)
                new_folder_name = f"{sampleName}_{scores[loopindex]}_sample{loopindex+1}" # set the new named directory
                new_folder_path = os.path.join(samplesPath, new_folder_name)
                os.makedirs(new_folder_path, exist_ok=True)  # Create the new folder               
                shutil.copytree(source_dir, new_folder_path, dirs_exist_ok=True) # copy contents from originals to samples
            else:                             # if all student submission are in a single folder (single file per student)
                root, extension = os.path.splitext(source_dir)
                new_file_name = f"{sampleName}_{scores[loopindex]}_sample{loopindex+1}{extension}" # set the new file name
                new_folder_path = os.path.join(samplesPath, new_file_name)
                shutil.copy2(source_dir, new_folder_path) # copy and rename the file from originals to samples
    
def make_sample(dataframe,label):
    """Run the processes: 1) output summary 2) run the sampling"""
    summarise_result(dataframe,label)
    copy_samples(dataframe)


# In[ ]:


""" FIRSTS """
df_firsts = find_samples(df, 70, 100) # create dataframe containing all firsts
make_sample(df_firsts, "Firsts")                # output First to report and take samples

"""FAILS """
df_fails  = find_samples(df, 0, 39.9) # create dataframe containing all fails
make_sample(df_fails, "Fails")                  # output Fails to report and take samples

""" BORDERLINES """
# create a dataframe containing all borderlines
df_border_fails  = find_samples(df, 39, 41)
df_border_22s    = find_samples(df, 49, 51)
df_border_21s    = find_samples(df, 59, 61)
df_border_firsts = find_samples(df, 69, 71)
df_borderlines   = pd.concat([df_border_fails,df_border_22s,df_border_21s,df_border_firsts]) # create dataframe combining all borderlines
make_sample(df_borderlines, "Borderlines")          # output Borderlines to report and take samples

""" IN BETWEENS """
# create a dataframe containing "a representative sample in between"
df_mid_3rd    = find_samples(df, 44, 46)
df_mid_22s    = find_samples(df, 54, 56)
df_mid_21s    = find_samples(df, 64, 66)

def prune_inbetweens_sample(dataframe):
    """ "Prune" the representative sample to avoid this being too large"""
    
    max_sample_fraction = 5/100        # fractional proportion of the total to include in the in-between sample (5/100 = 5%)
    max_number_inbetween_samples = 4   # absolute maximum number of in between samples
    
    if math.ceil(total_scripts*max_sample_fraction) < max_number_inbetween_samples:
        sample_size = math.ceil(total_scripts*max_sample_fraction)
    else:
        sample_size = max_number_inbetween_samples
    
    number_students_sample = dataframe.shape[0]
    if number_students_sample > sample_size:    # If there are more than desired samples, then limit to this number.        
        dataframe = dataframe.sample(n=sample_size)
    else:
        dataframe = dataframe
    return dataframe

df_mid_3rd    = prune_inbetweens_sample(df_mid_3rd)
df_mid_22s    = prune_inbetweens_sample(df_mid_22s)
df_mid_21s    = prune_inbetweens_sample(df_mid_21s)

df_mids       = pd.concat([df_mid_3rd, df_mid_22s, df_mid_21s]) # create dataframe combining all "in betweens"
make_sample(df_mids, "In Between Sample")                       # output "In Betweens" to report and take samples

