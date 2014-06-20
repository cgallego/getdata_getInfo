# -*- coding: utf-8 -*-
"""
Created on Fri Mar 14 12:36:36 2014

@author: Cristina Gallego
"""
import sys, os
import string
import datetime
import numpy as np

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from base import Base

#  created a Cad_record mapping 
class Cad_record(Base):
    """Base for cad_record class using Declarative. for table tbl_pt_mri_cad_record
    Outputs:
    ========
    tbl_pt_mri_cad_record.cad_pt_no_txt, 
    
    tbl_pt_mri_cad_record.latest_mutation_status_int, 
    
    tbl_pt_mri_cad_record.pt_id, 
    """
    __tablename__ = 'tbl_pt_mri_cad_record'
    __table_args__ = {'autoload':True}
    pt_id = Column(Integer, primary_key=True)
      
    def __repr__(self):
        return "Cad_record: cad_pt_no=%s, mutation_status=%s" % (self.cad_pt_no_txt, self.latest_mutation_status_int)

#  created a Exam_record mapping                              
class Exam_record(Base):
    """Base for Exam_record class using Declarative. for table tbl_pt_exam"""
    __tablename__ = 'tbl_pt_exam'
    __table_args__ = {'autoload':True}
    pt_exam_id = Column(Integer, primary_key=True)
    # class introduces the ForeignKey construct, which is a directive applied to Column that indicates that values in this column should be constrained to be values present in the named remote column.
    pt_id = Column(Integer, ForeignKey('tbl_pt_mri_cad_record.pt_id'))
    cad_record = relationship("Cad_record", backref=backref('tbl_pt_exam', order_by=pt_id))
    
    def __repr__(self):
        return "Exam_record: datetime=%s, a_number_txt=%s, mri_cad_status_txt=%s" % (self.exam_dt_datetime, self.a_number_txt, self.mri_cad_status_txt)

#  created a Exam_record mapping                              
class Exam_Finding(Base):
    """Base for Exam_Finding class using Declarative. for table tbl_pt_exam_finding"""
    __tablename__ = 'tbl_pt_exam_finding'
    __table_args__ = {'autoload':True}
    pt_exam_finding_id = Column(Integer, primary_key=True)
    
    # class introduces the ForeignKey construct, which is a directive applied to Column that indicates that values in this column should be constrained to be values present in the named remote column.
    pt_exam_id = Column(Integer, ForeignKey('tbl_pt_exam.pt_id'))
    finding_record = relationship("Exam_record", backref=backref('tbl_pt_exam', order_by=pt_exam_id))
    
    def __repr__(self):
        return "Exam_Finding: mri_mass_yn=%s, mri_nonmass_yn=%s, mri_foci_yn=%s" % (self.mri_mass_yn, self.mri_nonmass_yn, self.mri_foci_yn)
                   
#  created a Procedure mapping                              
class Procedure(Base):
    """Base for Procedure class using Declarative. """
    __tablename__ = 'tbl_pt_procedure'
    __table_args__ = {'autoload':True}
    pt_procedure_id = Column(Integer, primary_key=True)
    
    # class introduces the ForeignKey construct, which is a directive applied to Column that indicates that values in this column should be constrained to be values present in the named remote column.
    pt_id = Column(Integer, ForeignKey('tbl_pt_exam.pt_id'))
    
    def __repr__(self):
        return "Procedure: proc_dt_datetime=%s, proc_side_int=%s, proc_source_int=%s, proc_guid_int=%s, proc_tp_int=%s, original_report_txt=%s" % (self.proc_dt_datetime, self.proc_side_int, self.proc_source_int, self.proc_guid_int, self.proc_tp_int, self.original_report_txt)
  
 
#  created a Pathology mapping                              
class Pathology(Base):
    """Base for Pathology class using Declarative. """
    __tablename__ = 'tbl_pt_pathology'
    __table_args__ = {'autoload':True}
    pt_path_id = Column(Integer, primary_key=True)
    
    # class introduces the ForeignKey construct, which is a directive applied to Column that indicates that values in this column should be constrained to be values present in the named remote column.
    pt_procedure_id = Column(Integer, ForeignKey('tbl_pt_procedure.pt_procedure_id'))
    #pathology_record = relationship("Pathology",  primaryjoin="Pathology.pt_procedure_id==Procedure.pt_procedure_id")
    
    def __repr__(self):
        return "Pathology: cytology_int=%s, biopsy_benign_yn=%s, biopsy_high_risk_yn=%s, insitu_carcinoma=%s, invasive_carcinoma=%s, " % (self.cytology_int, self.histop_core_biopsy_benign_yn, self.histop_core_biopsy_high_risk_yn, self.histop_tp_isc_yn, self.histop_tp_ic_yn)

  
##  created exam_finding_lesion_link  
#class Finding_Lesion_link(Base):
#    """Base for Finding_Lesion_link class using Declarative. """
#    __tablename__ = 'tbl_pt_exam_finding_lesion_link'
#    __table_args__ = {'autoload':True}
#    pt_exam_finding_lesion_link_id = Column(Integer, primary_key=True)
#    
#    # class introduces the ForeignKey construct, which is a directive applied to Column that indicates that values in this column should be constrained to be values present in the named remote column.
#    pt_exam_finding_id = Column(Integer, ForeignKey('tbl_pt_exam_finding.pt_exam_finding_id'))
#    
#    def __repr__(self):
#        return
#
#
##  created exam_lesion_  
#class Exam_Lesion(Base):
#    """Base for tbl_pt_exam_lesion class using Declarative. """
#    __tablename__ = 'tbl_pt_exam_lesion'
#    __table_args__ = {'autoload':True}
#    
#    # class introduces the ForeignKey construct, which is a directive applied to Column that indicates that values in this column should be constrained to be values present in the named remote column.
#    pt_exam_lesion_id = Column(Integer, ForeignKey('tbl_pt_exam_finding_lesion_link.pt_exam_lesion_id'))
#    
#    def __repr__(self):
#        return
