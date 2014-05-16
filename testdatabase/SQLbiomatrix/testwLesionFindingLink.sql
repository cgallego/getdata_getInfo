SELECT 
  tbl_pt_mri_cad_record.cad_pt_no_txt, 
  tbl_pt_exam.exam_dt_datetime, 
  tbl_pt_exam.side_int, 
  tbl_pt_exam.a_number_txt, 
  tbl_pt_exam.radiology_rpt_generated_yn, 
  tbl_pt_exam.original_report_txt, 
  tbl_pt_exam.comment_txt, 
  tbl_pt_exam.mri_cad_status_txt, 
  tbl_pt_exam_finding.size_x_double, 
  tbl_pt_exam_finding.size_y_double, 
  tbl_pt_exam_finding.size_z_double, 
  tbl_pt_exam_finding.t2_signal_int, 
  tbl_pt_exam_finding.curve_int, 
  tbl_pt_exam_lesion.lesion_tp_int, 
  tbl_pt_exam_lesion.lesion_location_bilateral_multiple_yn, 
  tbl_pt_exam_lesion.lesion_location_axillary_tail_yn, 
  tbl_pt_exam_lesion.lesion_location_retroareolar_yn, 
  tbl_pt_exam_lesion.lesion_location_upper_yn, 
  tbl_pt_exam_lesion.lesion_location_lower_yn, 
  tbl_pt_exam_lesion.lesion_location_inner_yn, 
  tbl_pt_exam_lesion.lesion_location_outer_yn, 
  tbl_pt_exam_lesion.lesion_location_central_yn, 
  tbl_pt_exam_lesion.lesion_side_int, 
  tbl_pt_exam_lesion.lesion_depth_posterior_yn, 
  tbl_pt_exam_lesion.lesion_location_detail_txt, 
  tbl_pt_exam_lesion.lesion_x_coordinate_double, 
  tbl_pt_exam_lesion.lesion_y_coordinate_double, 
  tbl_pt_exam_lesion.lesion_z_coordinate_double, 
  tbl_pt_exam_lesion.slide_image_no_txt, 
  tbl_pt_exam_lesion.mri_series_no_txt, 
  tbl_pt_exam_lesion.lesion_start_image_no_int, 
  tbl_pt_exam_lesion.lesion_depth_middle_yn, 
  tbl_pt_exam_lesion.lesion_depth_anterior_yn, 
  tbl_pt_exam_lesion.lesion_location_nipple_yn, 
  tbl_pt_exam_lesion.lesion_location_bst_nos_yn, 
  tbl_pt_exam_lesion.lesion_location_subareolar_yn, 
  tbl_pt_exam_lesion.lesion_location_multiple_scattered_area_yn, 
  tbl_pt_exam_finding.mri_foci_yn, 
  tbl_pt_exam_finding.mri_mass_yn, 
  tbl_pt_exam_finding.mri_nonmass_yn
FROM 
  public.tbl_pt_mri_cad_record, 
  public.tbl_pt_exam, 
  public.tbl_pt_exam_finding, 
  public.tbl_pt_exam_lesion, 
  public.tbl_pt_exam_finding_lesion_link
WHERE 
  tbl_pt_exam.pt_id = tbl_pt_mri_cad_record.pt_id AND
  tbl_pt_exam.pt_exam_id = tbl_pt_exam_finding.pt_exam_id AND
  tbl_pt_exam_finding.pt_exam_finding_id = tbl_pt_exam_finding_lesion_link.pt_exam_finding_id AND
  tbl_pt_exam_finding_lesion_link.pt_exam_lesion_id = tbl_pt_exam_lesion.pt_exam_lesion_id AND
  tbl_pt_mri_cad_record.cad_pt_no_txt = '6042';
