# -*- coding: utf-8 -*-
"""
DICOM script to pull images to local files from research PACS

Created on Thu Mar 13 15:37:16 2014

@author: Cristina Gallego
"""

import os, os.path
import sys
import string
import time
from sys import argv, stderr, exit
import shlex, subprocess
import re

import numpy as np
import dicom
import psycopg2
import sqlalchemy as al
import sqlalchemy.orm

import pandas as pd
import database
from PyQt4 import Qt, QtGui

from dictionaries import data_loc, my_aet, hostID, local_port, clinical_aet, clinical_IP, clinical_port, remote_aet, remote_IP, remote_port
import dcmtk_routines as dcmtk

"""
----------------------------------------------------------------------
This script will

@ Copyright (C) Cristina Gallego, University of Toronto, 2013
----------------------------------------------------------------------
"""

def getScans(path_rootFolder, fileline, PatientID, StudyID, AccessionN, oldExamID):
    """
    run : getScans(path_rootFolder, PatientID, StudyID, AccessionN):

    Inputs
    ======
    path_rootFolder: (string)   Automatically generated based on the location of file 
    
    PatientID : (int)    MRN
    
    StudyID : (int)    CAD StudyID
    
    AccessionN : (int)  CAD AccessionN
    
    database : (bool) [True]   whether to check database for info about study.
    
    Output
    ======
    """
    try:
        dcmtk.check_MRI_MARTEL(path_rootFolder, remote_aet, remote_port, remote_IP, local_port, PatientID, StudyID, AccessionN)
        if(oldExamID==False):
            dcmtk.pull_MRI_MARTEL(path_rootFolder, remote_aet, remote_port, remote_IP, local_port, PatientID, StudyID, AccessionN, countImages=False)
        else:
            ExamID = fileline[4]
            dcmtk.pull_MRI_MARTELold(path_rootFolder, remote_aet, remote_port, remote_IP, local_port, PatientID, StudyID, AccessionN, ExamID, countImages=False)
            
    except (KeyboardInterrupt, SystemExit):
        dcmtk.check_pacs(path_rootFolder, data_loc,  clinical_aet , clinical_port, clinical_IP, local_port, PatientID, StudyID, AccessionN)
        dcmtk.pull_pacs(path_rootFolder, data_loc, clinical_aet, clinical_port, clinical_IP, local_port, PatientID, StudyID, AccessionN)
    except (KeyboardInterrupt, SystemExit):
        print 'Unable to find study in MRI_MARTEL or AS0SUNB --- Abort'
        sys.exit()
        
    return
            
if __name__ == '__main__':
    # Get Root folder ( the directory of the script being run)
    path_rootFolder = os.path.dirname(os.path.abspath(__file__))

    # Open filename list
    file_ids = open(sys.argv[1],"r")
    for fileline in file_ids:
        # Get the line: Study#, DicomExam#
        fileline = fileline.split()
        PatientID = fileline[0] 
        StudyID = fileline[1]
        AccessionN = fileline[2]
        dateID = fileline[3] #dateID = '2010-11-29' as '2010,11,29';
        
        ###### Retrieving
        print "Retrieving Scans to local drive..."
        getScans(path_rootFolder, fileline, PatientID, StudyID, AccessionN, oldExamID=False)
        
        ###### Querying
        print "Executing SQL connection..."
        # Format query StudyID
        if (len(StudyID) == 3 ): StudyID='0'+StudyID
        if (len(StudyID) == 2 ): StudyID='00'+StudyID
        if (len(StudyID) == 1 ): StudyID='000'+StudyID
        
        # Format query redateID
        redateID = dateID[0:4]+'-'+dateID[4:6]+'-'+dateID[6:8]
        #database.queryDatabase(StudyID, redateID)
               
    # end of line
    file_ids.close()
