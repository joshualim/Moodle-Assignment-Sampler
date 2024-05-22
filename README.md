# Moodle-Assignment-Sampler
Python helper script to generate a sample from a downloaded Moodle Assignment and Marksheet.

## Instructions
1. From Moodle download the marksheet (Bath version) and all the submissions to this folder (if there are multiple submissions per students then you MUST make sure "submissions downloaded in folders" is checked).
2. Update the first "Initial setup" code block
    - update filenames for marksheet and submissions.
    - update the unit code prefix naming convention as needed.
3. Run the script!

## What does this script do?
For each "grade range" you specify:
1. A text summary output is produced
    - number of scripts in the range
    - candidates username and initials for scripts in that range
2. Scripts are moved to a samples folder and renamed as {UNIT CODE}_{S1_23-24}__{GRADE}_sample{n}

The following are looked at:
- All the fails
- All the firsts
- All borderline grade (+/-1 to a grade boundary)
- A ‘representative’ sample in between 

## How does this script work?
This is script has 3 parts and is written in 3 code blocks
1. Initial setup script (e.g. set filenames, unit code prefixes) - **you will need to update this every time you run the script**
2. The functions/methods for sampling - this contains the logic for the sampling.
3. Run the sampling - this actually performs the sampling and generates the reports. It also contains some hard coded values you ***might*** want to tweak.


## What still needs to be done?
- Zip everything up at the end 
- tidy up code: refactor find_samples into make_sample
- sort out the numbering suffix for repeated entries. Currently the numbering doesn't make much sense.
- write summary results to text file

## About
Provided as-is, but contact <a href="mailto:jajhl20@bath.ac.uk" target="_blank">Josh Lim</a> for questions.

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><span property="dct:title">Moodle Assignment Sampler</span> by <span property="cc:attributionName">Josh Lim</span> is marked with <a href="https://creativecommons.org/publicdomain/zero/1.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC0 1.0</a> - Go forth and remix without attribution ;)</p>

version 1.0
