SELECT 
  tbl_pt_mri_cad_record.cad_pt_no_txt, 
  tbl_pt_mri_cad_record.latest_mutation_status_int, 
  tbl_pt_mri_cad_record.pt_id, 
  tbl_pt_exam.exam_dt_datetime, 
  tbl_pt_exam.a_number_txt, 
  tbl_pt_exam.mri_cad_status_txt, 
  tbl_pt_procedure.proc_dt_datetime, 
  tbl_pt_procedure.proc_side_int, 
  tbl_pt_procedure.proc_source_int, 
  tbl_pt_procedure.proc_guid_int, 
  tbl_pt_procedure.proc_tp_int, 
  tbl_pt_pathology.pt_procedure_id, 
  tbl_pt_pathology.cytology_int, 
  tbl_pt_pathology.histop_core_biopsy_benign_yn, 
  tbl_pt_pathology.histop_core_biopsy_high_risk_yn, 
  tbl_pt_pathology.histop_tp_isc_yn, 
  tbl_pt_pathology.histop_tp_ic_yn, 
  tbl_pt_pathology.tumr_site_int, 
  tbl_pt_pathology.tumr_size_width_double, 
  tbl_pt_pathology.tumr_size_height_double, 
  tbl_pt_pathology.tumr_size_depth_double, 
  tbl_pt_pathology.tumr_grade_int, 
  tbl_pt_pathology.tumr_stage_curr_stage_clin_int, 
  tbl_pt_exam_finding.mri_mass_yn, 
  tbl_pt_exam_finding.mri_nonmass_yn, 
  tbl_pt_exam_finding.mri_foci_yn, 
  tbl_pt_exam.pt_exam_id, 
  tbl_pt_exam_finding.size_x_double, 
  tbl_pt_exam_finding.size_y_double, 
  tbl_pt_exam_finding.size_z_double, 
  tbl_pt_exam_finding.mri_dce_init_enh_int, 
  tbl_pt_exam_finding.mri_dce_delay_enh_int, 
  tbl_pt_exam_finding.curve_int, 
  tbl_pt_exam_finding.mri_mass_margin_int, 
  tbl_pt_exam_finding.mammo_n_mri_mass_shape_int, 
  tbl_pt_exam_finding.pt_exam_finding_id, 
  tbl_pt_exam.exam_tp_int
FROM 
  public.tbl_pt_mri_cad_record, 
  public.tbl_pt_exam, 
  public.tbl_pt_procedure, 
  public.tbl_pt_pathology, 
  public.tbl_pt_exam_finding
WHERE 
  tbl_pt_mri_cad_record.pt_id = tbl_pt_exam.pt_id AND
  tbl_pt_exam.pt_id = tbl_pt_procedure.pt_id AND
  tbl_pt_procedure.pt_procedure_id = tbl_pt_pathology.pt_procedure_id AND
  tbl_pt_exam_finding.pt_exam_id = tbl_pt_exam.pt_exam_id AND
  tbl_pt_mri_cad_record.cad_pt_no_txt = '0114' AND 
  tbl_pt_exam.exam_dt_datetime = '2011-10-02';
