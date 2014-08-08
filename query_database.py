# -*- coding: utf-8 -*-
"""
Created on Wed Apr 09 15:53:42 2014

@ author (C) Cristina Gallego, University of Toronto
"""
import sys, os
import string
import datetime
from numpy import *

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import database
from base import Base, engine
import pandas as pd

import wx
import wxTableBase

#!/usr/bin/env python
class Query(object):
    """
    USAGE:
    =============
    database = QueryDatabase()
    """
    def __call__(self):       
        """ Turn Class into a callable object """
        QueryDatabase()
        
        
    def __init__(self): 
        """ initialize QueryDatabase """
        self.QueryPatient = []
        self.is_mass = []
        self.is_nonmass = []
                              
    def queryDatabaseSingle(self, StudyID, redateID):
        """
        run : Query by StudyID/AccesionN pair study to local folder by by steps in case information is not linked
        
        Inputs
        ======
        StudyID : (int)    CAD StudyID
        redateID : (int)  CAD StudyID Data of exam (format yyyy-mm-dd)
        
        Output
        ======
        """
        # Create the ORMâ€™s â€œhandleâ€ to the database: the Session. 
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)  # once engine is available
        session = self.Session() #instantiate a Session
        
        # Create first display
        """ Creates Table grid and Query output display Cad_Container"""
        self.app = wx.App(False)
        self.display = wxTableBase.Container(self.app)
        
        data_cad_case = []; data_exam_case=[];
         #first query CAD case table 
        for cad_case in session.query(database.Cad_record).filter(database.Cad_record.cad_pt_no_txt == str(StudyID)):
            print "cad_case.pt_id, cad_case.cad_pt_no_txt, cad_case.latest_mutation_status_int"
            print cad_case.pt_id, cad_case.cad_pt_no_txt, cad_case.latest_mutation_status_int
            data_cad_case.append([cad_case.pt_id, cad_case.cad_pt_no_txt, cad_case.latest_mutation_status_int])
        
        colLabels = ("pt_id", "cad_pt_no_txt", "latest_mutation_status_int")
        rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(data_cad_case))])
        # Add display query to wxTable    
        self.display.Cad_Container_initGUI(data_cad_case, rowLabels, colLabels)
        
        #Now query CAD case exams donw
        for cad_case, exam_case, in session.query(database.Cad_record,  database.Exam_record).\
            filter(database.Cad_record.cad_pt_no_txt == str(StudyID)).\
            filter(database.Cad_record.pt_id == database.Exam_record.pt_id):
                
            data_exam_case.append([exam_case.exam_dt_datetime, exam_case.a_number_txt, exam_case.mri_cad_status_txt, exam_case.comment_txt, exam_case.exam_img_dicom_txt, exam_case.side_int])
                                 
        # add mass lesion record table
        colLabels = ("exam_dt_datetime", "a_number_txt", "mri_cad_status_txt", "comment_txt", "exam_img_dicom_txt", "side_int")
        rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(data_exam_case))])
        # Add display query to wxTable    
        self.display.MassNonM_Container_initGUI(data_exam_case, rowLabels, colLabels, "Exam records")
                
        # Finish the display and Show
        self.display.Centre()
        self.display.Show()
        self.app.MainLoop()    
        
        return
        
        
    def queryDatabase(self, StudyID, redateID):
        """
        run : Query by StudyID/AccesionN pair study to local folder
        
        Inputs
        ======
        StudyID : (int)    CAD StudyID
        redateID : (int)  CAD StudyID Data of exam (format yyyy-mm-dd)
        
        Output
        ======
        """               
        # Create the database: the Session. 
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)  # once engine is available
        session = self.Session() #instantiate a Session
        
        # Create first display
        """ Creates Table grid and Query output display Cad_Container"""
        self.app = wx.App(False)
        self.display = wxTableBase.Container(self.app)
        
        #for cad_case in session.query(Cad_record).order_by(Cad_record.pt_id): 
        #    print cad_case.pt_id, cad_case.cad_pt_no_txt, cad_case.latest_mutation_status_int    
        
        datainfo = []; is_mass=[];  is_nonmass=[]; pathology=[]; 
        for cad, exam, finding, proc, patho in session.query(database.Cad_record, database.Exam_record, database.Exam_Finding, database.Procedure, database.Pathology).\
                     filter(database.Cad_record.pt_id==database.Exam_record.pt_id).\
                     filter(database.Exam_record.pt_exam_id==database.Exam_Finding.pt_exam_id).\
                     filter(database.Exam_record.pt_id==database.Procedure.pt_id).\
                     filter(database.Procedure.pt_procedure_id==database.Pathology.pt_procedure_id).\
                     filter(database.Cad_record.cad_pt_no_txt == str(StudyID)).\
                     filter(database.Exam_record.exam_dt_datetime == str(redateID)).all():
                         
           # print results
           if not cad:
               print "cad is empty"
           if not exam:
               print "exam is empty"
           if not finding:
               print "finding is empty"
           if not proc:
               print "proc is empty"
           if not patho:
               print "patho is empty"
                   
           datainfo.append([cad.cad_pt_no_txt, cad.latest_mutation_status_int,
              exam.exam_dt_datetime, exam.a_number_txt, exam.mri_cad_status_txt, exam.comment_txt,
              finding.mri_mass_yn, finding.mri_nonmass_yn, finding.mri_foci_yn,
              proc.pt_procedure_id, proc.proc_dt_datetime, proc.proc_side_int, proc.proc_source_int, proc.proc_guid_int, proc.proc_tp_int, proc.original_report_txt])
           
           #iterate through patho keys
           pathodict = patho.__dict__
           pathokeys = pathodict.keys()
           pathoItems = pathodict.items()
           procpath=[]; procLabels=[];
           for k in range(len(pathokeys)):
               if( pathoItems[k][1] ):
                   procpath.append( pathoItems[k][1] )
                   procLabels.append( str(pathoItems[k][0]) )
           
           # add procedure lesion record table 
           pathology.append(procpath)
           rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(pathology))])
           # Add display query to wxTable    
           self.display.MassNonM_Container_initGUI(pathology, rowLabels, procLabels, "procedure/pathology")
           pathology=[];  
           
           # Find if it's mass or non-mass and process
           if (finding.mri_mass_yn):
               is_mass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_mass_margin_int, finding.mammo_n_mri_mass_shape_int, finding.t2_signal_int])
           
           # Find if it's mass or non-mass and process
           if (finding.mri_nonmass_yn):
               is_nonmass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_nonmass_dist_int, finding.mri_nonmass_int_enh_int, finding.t2_signal_int ])
          
          ####### finish finding masses and non-masses
        
        ################### Send to table display  
        # add main CAD record table       
        colLabels = ("cad.cad_pt_no_txt", "cad.latest_mutation", "exam.exam_dt_datetime","exam.a_number_txt", "exam.mri_cad_status_txt", "exam.comment_txt", "finding.mri_mass_yn", "finding.mri_nonmass_yn", "finding.mri_foci_yn", "proc.pt_procedure_id", "proc.proc_dt_datetime", "proc.proc_side_int", "proc.proc_source_int", "proc.proc_guid_int", "proc.proc_tp_int", "proc.original_report_txt")
        rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(datainfo))])
        # Add display query to wxTable    
        self.display.Cad_Container_initGUI(datainfo, rowLabels, colLabels)
        
        # write output query to pandas frame.
        self.d1 = pd.DataFrame(data=array(datainfo), columns=list(colLabels))
        
        # add mass lesion record table
        colLabelsmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_mass_margin_int", "finding.mammo_n_mri_mass_shape_int", "finding.t2_signal_int")
        rowLabelsmass = tuple(["%s" % str(x) for x in xrange(0,len(is_mass))])
        # Add display query to wxTable    
        self.display.MassNonM_Container_initGUI(is_mass, rowLabelsmass, colLabelsmass, "Masses")
        
        # add non-mass lesion record table
        colLabelsnonmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_nonmass_dist_int", "finding.mri_nonmass_int_enh_int", "finding.t2_signal_int")
        rowLabelsnonmass = tuple(["%s" % str(x) for x in xrange(0,len(is_nonmass))])
        # Add display query to wxTable    
        self.display.MassNonM_Container_initGUI(is_nonmass, rowLabelsnonmass, colLabelsnonmass, "NonMasses")
        
        # Finish the display and Show
        self.display.Centre()
        self.display.Show()
        self.app.MainLoop()    
        
        return
        

    def queryDatabasewNoGui(self, StudyID, redateID):
        """
        run : Query by StudyID/AccesionN pair study to local folder
        
        Inputs
        ======
        StudyID : (int)    CAD StudyID
        redateID : (int)  CAD StudyID Data of exam (format yyyy-mm-dd)
        
        Output
        ======
        """
        # Create the ORMâ€™s â€œhandleâ€ to the database: the Session. 
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)  # once engine is available
        session = self.Session() #instantiate a Session
        
        datainfo = []; is_mass=[];  is_nonmass=[]; pathology=[]; 
        for cad, exam, finding, proc, patho in session.query(database.Cad_record, database.Exam_record, database.Exam_Finding, database.Procedure, database.Pathology).\
                     filter(database.Cad_record.pt_id==database.Exam_record.pt_id).\
                     filter(database.Exam_record.pt_exam_id==database.Exam_Finding.pt_exam_id).\
                     filter(database.Exam_record.pt_id==database.Procedure.pt_id).\
                     filter(database.Procedure.pt_procedure_id==database.Pathology.pt_procedure_id).\
                     filter(database.Cad_record.cad_pt_no_txt == str(StudyID)).\
                     filter(database.Exam_record.exam_dt_datetime == str(redateID)).all():
                         
           # print results
           if not cad:
               print "cad is empty"
           if not exam:
               print "exam is empty"
           if not finding:
               print "finding is empty"
           if not proc:
               print "proc is empty"
           if not patho:
               print "patho is empty"
                   
           datainfo.append([cad.cad_pt_no_txt, cad.latest_mutation_status_int,
              exam.exam_dt_datetime, exam.a_number_txt, exam.mri_cad_status_txt, exam.comment_txt,
              finding.mri_mass_yn, finding.mri_nonmass_yn, finding.mri_foci_yn,
              proc.pt_procedure_id, proc.proc_dt_datetime, proc.proc_side_int, proc.proc_source_int, proc.proc_guid_int, proc.proc_tp_int, proc.original_report_txt])
           
           #iterate through patho keys
           pathodict = patho.__dict__
           pathokeys = pathodict.keys()
           pathoItems = pathodict.items()
           procpath=[]; procLabels=[];
           for k in range(len(pathokeys)):
               if( pathoItems[k][1] ):
                   procpath.append( pathoItems[k][1] )
                   procLabels.append( str(pathoItems[k][0]) )
           
           # add procedure lesion record table 
           pathology.append(procpath)
           rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(pathology))])
           
           # Find if it's mass or non-mass and process
           if (finding.mri_mass_yn):
               is_mass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_mass_margin_int, finding.mammo_n_mri_mass_shape_int, finding.t2_signal_int])
           
           # Find if it's mass or non-mass and process
           if (finding.mri_nonmass_yn):
               is_nonmass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_nonmass_dist_int, finding.mri_nonmass_int_enh_int, finding.t2_signal_int ])
          
          ####### finish finding masses and non-masses
        
        ################### Send to table display  
        # add main CAD record table       
        colLabels = ("cad.cad_pt_no_txt", "cad.latest_mutation", "exam.exam_dt_datetime","exam.a_number_txt", "exam.mri_cad_status_txt", "exam.comment_txt", "finding.mri_mass_yn", "finding.mri_nonmass_yn", "finding.mri_foci_yn", "proc.pt_procedure_id", "proc.proc_dt_datetime", "proc.proc_side_int", "proc.proc_source_int", "proc.proc_guid_int", "proc.proc_tp_int", "proc.original_report_txt")
        rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(datainfo))])
        
        # write output query to pandas frame.
        self.d1 = pd.DataFrame(data=array(datainfo), columns=list(colLabels))
        
        # add mass lesion record table
        colLabelsmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_mass_margin_int", "finding.mammo_n_mri_mass_shape_int", "finding.t2_signal_int")
        rowLabelsmass = tuple(["%s" % str(x) for x in xrange(0,len(is_mass))])
        
        # add non-mass lesion record table
        colLabelsnonmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_nonmass_dist_int", "finding.mri_nonmass_int_enh_int", "finding.t2_signal_int")
        rowLabelsnonmass = tuple(["%s" % str(x) for x in xrange(0,len(is_nonmass))])
        
        return 
        
        
    def queryDatabaseNoproced(self, StudyID, redateID):
        """
        run : Query by StudyID/AccesionN pair study to local folder
        
        Inputs
        ======
        StudyID : (int)    CAD StudyID
        NO procedure, No pathology        
        Output
        ======
        Create a query to provide information about radiology findings in order to identify and segment lesion
        """               
        # Create the database: the Session. 
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)  # once engine is available
        session = self.Session() #instantiate a Session
                
        #for cad_case in session.query(Cad_record).order_by(Cad_record.pt_id): 
        #    print cad_case.pt_id, cad_case.cad_pt_no_txt, cad_case.latest_mutation_status_int    
        
        datainfo = []; radreport=[];
        for cad, exam, finding in session.query(database.Cad_record, database.Exam_record, database.Exam_Finding).\
                     filter(database.Cad_record.pt_id==database.Exam_record.pt_id).\
                     filter(database.Exam_record.pt_exam_id==database.Exam_Finding.pt_exam_id).\
                     filter(database.Cad_record.cad_pt_no_txt == str(StudyID)).all():
                         
           # print results
           if not cad:
               print "cad is empty"
           if not exam:
               print "exam is empty"
           if not finding:
               print "finding is empty"
                   
           datainfo.append([cad.cad_pt_no_txt, cad.latest_mutation_status_int,
              exam.exam_dt_datetime, exam.a_number_txt, exam.exam_img_dicom_txt, exam.mri_cad_status_txt, exam.comment_txt,
              finding.mri_mass_yn, finding.mri_nonmass_yn, finding.mri_foci_yn,
              finding.all_comments_txt])
           
           # Create rad report dataset
           radreport.append([ str(exam.original_report_txt), str(exam.comment_txt)])
           
           # Find if it's mass or non-mass and process
           if (finding.mri_mass_yn):
               self.is_mass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_mass_margin_int, finding.mammo_n_mri_mass_shape_int, finding.t2_signal_int])
           
           # Find if it's mass or non-mass and process
           if (finding.mri_nonmass_yn):
               self.is_nonmass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_nonmass_dist_int, finding.mri_nonmass_int_enh_int, finding.t2_signal_int ])
          
          ####### finish finding masses and non-masses
        
        ################### Send to table display  
        # add main CAD record table       
        colLabels = ("cad.cad_pt_no_txt", "cad.latest_mutation", "exam.exam_dt_datetime","exam.a_number_txt", "exam.exam_img_dicom_txt", "exam.mri_cad_status_txt", "exam.comment_txt", "finding.mri_mass_yn", "finding.mri_nonmass_yn", "finding.mri_foci_yn", "all_comments_txt")
        rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(datainfo))])
        
        # Add display query to wxTable    
        self.display.Cad_Container_initGUI(datainfo, rowLabels, colLabels)
        
        # write output query to pandas frame.
        self.d1 = pd.DataFrame(data=array(datainfo), columns=list(colLabels))
        
        # write output query to pandas frame.
        radreport_label = ("exam.original_report_txt", "exam.comment_txt")
        self.radreport = pd.DataFrame(data=array(radreport), columns=list(radreport_label))
           
        # add mass lesion record table
        colLabelsmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_mass_margin_int", "finding.mammo_n_mri_mass_shape_int", "finding.t2_signal_int")
        rowLabelsmass = tuple(["%s" % str(x) for x in xrange(0,len(self.is_mass))])
        # Add display query to wxTable    
        self.display.MassNonM_Container_initGUI(self.is_mass, rowLabelsmass, colLabelsmass, "Masses")
        
        # add non-mass lesion record table
        colLabelsnonmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_nonmass_dist_int", "finding.mri_nonmass_int_enh_int", "finding.t2_signal_int")
        rowLabelsnonmass = tuple(["%s" % str(x) for x in xrange(0,len(self.is_nonmass))])
        # Add display query to wxTable    
        self.display.MassNonM_Container_initGUI(self.is_nonmass, rowLabelsnonmass, colLabelsnonmass, "NonMasses")
        
        # Finish the display and Show
        self.display.Center()
        self.display.Show(True)
        self.app.MainLoop()   


        return  self.is_mass, colLabelsmass, self.is_nonmass, colLabelsnonmass
        
        
    def queryDatabase4T2(self, StudyID, redateID):
        """
        run : Query by StudyID/AccesionN pair study to local folder
        
        Inputs
        ======
        StudyID : (int)    CAD StudyID
        redateID : (int)  CAD StudyID Data of exam (format yyyy-mm-dd)
        
        Output
        ======
        """               
        # Create the database: the Session. 
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)  # once engine is available
        session = self.Session() #instantiate a Session
        
        # Create first display
        """ Creates Table grid and Query output display Cad_Container"""
        self.app = wx.App(False)
        self.app.ExitOnFrameDelete = True
        self.display = wxTableBase.Container(self.app)
        
        #for cad_case in session.query(Cad_record).order_by(Cad_record.pt_id): 
        #    print cad_case.pt_id, cad_case.cad_pt_no_txt, cad_case.latest_mutation_status_int    
        
        datainfo = []; pathology=[]; 
        for cad, exam, finding, proc, patho in session.query(database.Cad_record, database.Exam_record, database.Exam_Finding, database.Procedure, database.Pathology).\
                     filter(database.Cad_record.pt_id==database.Exam_record.pt_id).\
                     filter(database.Exam_record.pt_exam_id==database.Exam_Finding.pt_exam_id).\
                     filter(database.Exam_record.pt_id==database.Procedure.pt_id).\
                     filter(database.Procedure.pt_procedure_id==database.Pathology.pt_procedure_id).\
                     filter(database.Cad_record.cad_pt_no_txt == str(StudyID)).\
                     filter(database.Exam_record.exam_dt_datetime == str(redateID)).all():
                         
           # print results
           if not cad:
               print "cad is empty"
           if not exam:
               print "exam is empty"
           if not finding:
               print "finding is empty"
           if not proc:
               print "proc is empty"
           if not patho:
               print "patho is empty"
                   
           datainfo.append([cad.cad_pt_no_txt, cad.latest_mutation_status_int,
              exam.exam_dt_datetime, exam.a_number_txt, exam.mri_cad_status_txt, exam.comment_txt,
              finding.mri_mass_yn, finding.mri_nonmass_yn, finding.mri_foci_yn,
              proc.pt_procedure_id, proc.proc_dt_datetime, proc.proc_side_int, proc.proc_source_int, proc.proc_guid_int, proc.proc_tp_int, proc.original_report_txt])
           
           #iterate through patho keys
           pathodict = patho.__dict__
           pathokeys = pathodict.keys()
           pathoItems = pathodict.items()
           procpath=[]; procLabels=[];
           for k in range(len(pathokeys)):
               if( pathoItems[k][1] ):
                   procpath.append( pathoItems[k][1] )
                   procLabels.append( str(pathoItems[k][0]) )
           
           # add procedure lesion record table 
           pathology.append(procpath)
           rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(pathology))])
           # Add display query to wxTable    
           self.display.MassNonM_Container_initGUI(pathology, rowLabels, procLabels, "procedure/pathology")
           pathology=[];  
           
           # Find if it's mass or non-mass and process
           if (finding.mri_mass_yn):
               self.is_mass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_mass_margin_int, finding.mammo_n_mri_mass_shape_int, finding.t2_signal_int])
           
           # Find if it's mass or non-mass and process
           if (finding.mri_nonmass_yn):
               self.is_nonmass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_nonmass_dist_int, finding.mri_nonmass_int_enh_int, finding.t2_signal_int ])
          
          ####### finish finding masses and non-masses
        
        ################### Send to table display  
        # add main CAD record table       
        colLabels = ("cad.cad_pt_no_txt", "cad.latest_mutation", "exam.exam_dt_datetime","exam.a_number_txt", "exam.mri_cad_status_txt", "exam.comment_txt", "finding.mri_mass_yn", "finding.mri_nonmass_yn", "finding.mri_foci_yn", "proc.pt_procedure_id", "proc.proc_dt_datetime", "proc.proc_side_int", "proc.proc_source_int", "proc.proc_guid_int", "proc.proc_tp_int", "proc.original_report_txt")
        rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(datainfo))])
        # Add display query to wxTable    
        self.display.Cad_Container_initGUI(datainfo, rowLabels, colLabels)
        
        # write output query to pandas frame.
        self.d1 = pd.DataFrame(data=array(datainfo), columns=list(colLabels))
        
        # add mass lesion record table
        colLabelsmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_mass_margin_int", "finding.mammo_n_mri_mass_shape_int", "finding.t2_signal_int")
        rowLabelsmass = tuple(["%s" % str(x) for x in xrange(0,len(self.is_mass))])
        # Add display query to wxTable    
        self.display.MassNonM_Container_initGUI(self.is_mass, rowLabelsmass, colLabelsmass, "Masses")
        
        # add non-mass lesion record table
        colLabelsnonmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_nonmass_dist_int", "finding.mri_nonmass_int_enh_int", "finding.t2_signal_int")
        rowLabelsnonmass = tuple(["%s" % str(x) for x in xrange(0,len(self.is_nonmass))])
        
        # Add display query to wxTable    
        self.display.MassNonM_Container_initGUI(self.is_nonmass, rowLabelsnonmass, colLabelsnonmass, "NonMasses")
        
        # Finish the display and Show
        self.display.Centre()
        self.display.Show(True)
        self.app.MainLoop() 
        
        return  self.is_mass, colLabelsmass, self.is_nonmass, colLabelsnonmass
        
        
    def queryDatabasebyProc(self, StudyID, procdate):
        """
        run : Query by StudyID/AccesionN pair study to local folder
        
        Inputs
        ======
        StudyID : (int)    CAD StudyID
        procdate : (int)  CAD StudyID Data of Procedure (format yyyy-mm-dd)
        
        Output
        ======
        Create a query to provide information about radiology findings in order to identify and segment lesion
        """               
        # Create the database: the Session. 
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)  # once engine is available
        session = self.Session() #instantiate a Session
        
        # Create first display
        """ Creates Table grid and Query output display Cad_Container"""
        self.app = wx.App(False)
        self.app.ExitOnFrameDelete = True
        self.display = wxTableBase.Container(self.app)
        
        #for cad_case in session.query(Cad_record).order_by(Cad_record.pt_id): 
        #    print cad_case.pt_id, cad_case.cad_pt_no_txt, cad_case.latest_mutation_status_int    
        
        datainfo = []; pathology=[]; radreport=[];
        for cad, exam, finding, proc, patho in session.query(database.Cad_record, database.Exam_record, database.Exam_Finding, database.Procedure, database.Pathology).\
                     filter(database.Cad_record.pt_id==database.Exam_record.pt_id).\
                     filter(database.Exam_record.pt_exam_id==database.Exam_Finding.pt_exam_id).\
                     filter(database.Exam_record.pt_id==database.Procedure.pt_id).\
                     filter(database.Procedure.pt_procedure_id==database.Pathology.pt_procedure_id).\
                     filter(database.Cad_record.cad_pt_no_txt == str(StudyID)).\
                     filter(database.Procedure.proc_dt_datetime == str(procdate)).all():
                         
           # print results
           if not cad:
               print "cad is empty"
           if not exam:
               print "exam is empty"
           if not finding:
               print "finding is empty"
           if not proc:
               print "proc is empty"
           if not patho:
               print "patho is empty"
                   
           datainfo.append([cad.cad_pt_no_txt, cad.latest_mutation_status_int,
              exam.exam_dt_datetime, exam.a_number_txt, exam.exam_img_dicom_txt, exam.mri_cad_status_txt, exam.comment_txt,
              finding.mri_mass_yn, finding.mri_nonmass_yn, finding.mri_foci_yn,
              proc.pt_procedure_id, proc.proc_dt_datetime, proc.proc_side_int, proc.proc_source_int, proc.proc_guid_int, proc.proc_tp_int, proc.original_report_txt])
           
           # Create rad report dataset
           radreport.append([ str(exam.original_report_txt), str(exam.comment_txt)])
           
           #iterate through patho keys
           pathodict = patho.__dict__
           pathokeys = pathodict.keys()
           pathoItems = pathodict.items()
           procpath=[]; procLabels=[];
           for k in range(len(pathokeys)):
               if( pathoItems[k][1] ):
                   procpath.append( pathoItems[k][1] )
                   procLabels.append( str(pathoItems[k][0]) )
           
           # add procedure lesion record table 
           pathology.append(procpath)
           rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(pathology))])
           # Add display query to wxTable    
           self.display.MassNonM_Container_initGUI(pathology, rowLabels, procLabels, "procedure/pathology")
           pathology=[];  
           
           # Find if it's mass or non-mass and process
           if (finding.mri_mass_yn):
               self.is_mass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_mass_margin_int, finding.mammo_n_mri_mass_shape_int, finding.t2_signal_int])
           
           # Find if it's mass or non-mass and process
           if (finding.mri_nonmass_yn):
               self.is_nonmass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_nonmass_dist_int, finding.mri_nonmass_int_enh_int, finding.t2_signal_int ])
          
          ####### finish finding masses and non-masses
        
        ################### Send to table display  
        # add main CAD record table       
        colLabels = ("cad.cad_pt_no_txt", "cad.latest_mutation", "exam.exam_dt_datetime","exam.a_number_txt", "exam.exam_img_dicom_txt", "exam.mri_cad_status_txt", "exam.comment_txt", "finding.mri_mass_yn", "finding.mri_nonmass_yn", "finding.mri_foci_yn", "proc.pt_procedure_id", "proc.proc_dt_datetime", "proc.proc_side_int", "proc.proc_source_int", "proc.proc_guid_int", "proc.proc_tp_int", "proc.original_report_txt")
        rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(datainfo))])
        # Add display query to wxTable    
        self.display.Cad_Container_initGUI(datainfo, rowLabels, colLabels)
        
        # write output query to pandas frame.
        self.d1 = pd.DataFrame(data=array(datainfo), columns=list(colLabels))
        
        # write output query to pandas frame.
        radreport_label = ("exam.original_report_txt", "exam.comment_txt")
        self.radreport = pd.DataFrame(data=array(radreport), columns=list(radreport_label))
           
        # add mass lesion record table
        colLabelsmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_mass_margin_int", "finding.mammo_n_mri_mass_shape_int", "finding.t2_signal_int")
        rowLabelsmass = tuple(["%s" % str(x) for x in xrange(0,len(self.is_mass))])
        # Add display query to wxTable    
        self.display.MassNonM_Container_initGUI(self.is_mass, rowLabelsmass, colLabelsmass, "Masses")
        
        # add non-mass lesion record table
        colLabelsnonmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_nonmass_dist_int", "finding.mri_nonmass_int_enh_int", "finding.t2_signal_int")
        rowLabelsnonmass = tuple(["%s" % str(x) for x in xrange(0,len(self.is_nonmass))])
        # Add display query to wxTable    
        self.display.MassNonM_Container_initGUI(self.is_nonmass, rowLabelsnonmass, colLabelsnonmass, "NonMasses")
        
        # Finish the display and Show
        self.display.Center()
        self.display.Show(True)
        self.app.MainLoop()   


        return  self.is_mass, colLabelsmass, self.is_nonmass, colLabelsnonmass
        
        
    def queryDatabasebyProcBenignAssumed(self, StudyID, procdate):
        """
        run : Query by StudyID/AccesionN pair study to local folder
        
        Inputs
        ======
        StudyID : (int)    CAD StudyID
        NO procedure, No pathology        
        Output
        ======
        Create a query to provide information about radiology findings in order to identify and segment lesion
        """               
        # Create the database: the Session. 
        self.Session = sessionmaker()
        self.Session.configure(bind=engine)  # once engine is available
        session = self.Session() #instantiate a Session
        
        # Create first display
        """ Creates Table grid and Query output display Cad_Container"""
        self.app = wx.App(False)
        self.app.ExitOnFrameDelete = True
        self.display = wxTableBase.Container(self.app)
        
        #for cad_case in session.query(Cad_record).order_by(Cad_record.pt_id): 
        #    print cad_case.pt_id, cad_case.cad_pt_no_txt, cad_case.latest_mutation_status_int    
        
        datainfo = []; radreport=[];
        for cad, exam, finding in session.query(database.Cad_record, database.Exam_record, database.Exam_Finding).\
                     filter(database.Cad_record.pt_id==database.Exam_record.pt_id).\
                     filter(database.Exam_record.pt_exam_id==database.Exam_Finding.pt_exam_id).\
                     filter(database.Cad_record.cad_pt_no_txt == str(StudyID)).all():
                         
           # print results
           if not cad:
               print "cad is empty"
           if not exam:
               print "exam is empty"
           if not finding:
               print "finding is empty"
                   
           datainfo.append([cad.cad_pt_no_txt, cad.latest_mutation_status_int,
              exam.exam_dt_datetime, exam.a_number_txt, exam.exam_img_dicom_txt, exam.mri_cad_status_txt, exam.comment_txt,
              finding.mri_mass_yn, finding.mri_nonmass_yn, finding.mri_foci_yn,
              finding.all_comments_txt])
           
           # Create rad report dataset
           radreport.append([ str(exam.original_report_txt), str(exam.comment_txt)])
           
           
           # Find if it's mass or non-mass and process
           if (finding.mri_mass_yn):
               self.is_mass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_mass_margin_int, finding.mammo_n_mri_mass_shape_int, finding.t2_signal_int])
           
           # Find if it's mass or non-mass and process
           if (finding.mri_nonmass_yn):
               self.is_nonmass.append([finding.side_int, finding.size_x_double, finding.size_y_double, finding.size_z_double, finding.mri_dce_init_enh_int, finding.mri_dce_delay_enh_int, finding.curve_int, finding.mri_nonmass_dist_int, finding.mri_nonmass_int_enh_int, finding.t2_signal_int ])
          
          ####### finish finding masses and non-masses
        
        ################### Send to table display  
        # add main CAD record table       
        colLabels = ("cad.cad_pt_no_txt", "cad.latest_mutation", "exam.exam_dt_datetime","exam.a_number_txt", "exam.exam_img_dicom_txt", "exam.mri_cad_status_txt", "exam.comment_txt", "finding.mri_mass_yn", "finding.mri_nonmass_yn", "finding.mri_foci_yn", "all_comments_txt")
        rowLabels = tuple(["%s" % str(x) for x in xrange(0,len(datainfo))])
        # Add display query to wxTable    
        self.display.Cad_Container_initGUI(datainfo, rowLabels, colLabels)
        
        # write output query to pandas frame.
        self.d1 = pd.DataFrame(data=array(datainfo), columns=list(colLabels))
        
        # write output query to pandas frame.
        radreport_label = ("exam.original_report_txt", "exam.comment_txt")
        self.radreport = pd.DataFrame(data=array(radreport), columns=list(radreport_label))
           
        # add mass lesion record table
        colLabelsmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_mass_margin_int", "finding.mammo_n_mri_mass_shape_int", "finding.t2_signal_int")
        rowLabelsmass = tuple(["%s" % str(x) for x in xrange(0,len(self.is_mass))])
        # Add display query to wxTable    
        self.display.MassNonM_Container_initGUI(self.is_mass, rowLabelsmass, colLabelsmass, "Masses")
        
        # add non-mass lesion record table
        colLabelsnonmass = ("finding.side_int", "finding.size_x_double", "finding.size_y_double", "finding.size_z_double", "finding.mri_dce_init_enh_int", "finding.mri_dce_delay_enh_int", "finding.curve_int", "finding.mri_nonmass_dist_int", "finding.mri_nonmass_int_enh_int", "finding.t2_signal_int")
        rowLabelsnonmass = tuple(["%s" % str(x) for x in xrange(0,len(self.is_nonmass))])
        # Add display query to wxTable    
        self.display.MassNonM_Container_initGUI(self.is_nonmass, rowLabelsnonmass, colLabelsnonmass, "NonMasses")
        
        # Finish the display and Show
        self.display.Center()
        self.display.Show(True)
        self.app.MainLoop()   


        return  self.is_mass, colLabelsmass, self.is_nonmass, colLabelsnonmass