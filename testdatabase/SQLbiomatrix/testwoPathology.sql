SELECT 
  tbl_pt_mri_cad_record.pt_id, 
  tbl_pt_mri_cad_record.cad_pt_no_txt, 
  tbl_pt_mri_cad_record.latest_mutation_status_int, 
  tbl_pt_exam.exam_dt_datetime, 
  tbl_pt_exam.a_number_txt, 
  tbl_pt_exam.mri_cad_status_txt, 
  tbl_pt_exam.comment_txt, 
  tbl_pt_exam_finding.mri_mass_yn, 
  tbl_pt_exam_finding.mri_nonmass_yn, 
  tbl_pt_exam_finding.mri_foci_yn, 
  tbl_pt_procedure.pt_procedure_id, 
  tbl_pt_procedure.proc_dt_datetime, 
  tbl_pt_procedure.proc_side_int, 
  tbl_pt_procedure.proc_source_int, 
  tbl_pt_procedure.proc_guid_int, 
  tbl_pt_procedure.proc_tp_int, 
  tbl_pt_procedure.original_report_txt
FROM 
  public.tbl_pt_mri_cad_record, 
  public.tbl_pt_exam, 
  public.tbl_pt_exam_finding, 
  public.tbl_pt_procedure
WHERE 
  tbl_pt_exam.pt_exam_id = tbl_pt_exam_finding.pt_exam_id AND
  tbl_pt_exam.pt_id = tbl_pt_mri_cad_record.pt_id AND
  tbl_pt_exam.pt_id = tbl_pt_procedure.pt_id AND
  tbl_pt_mri_cad_record.cad_pt_no_txt = '0673';
