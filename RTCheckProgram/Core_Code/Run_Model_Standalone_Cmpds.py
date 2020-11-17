from Core_Code.Retention_Confirmation_Workflow import Join_StandAlone_Molecular_Features,Run_Model_On_Punitive_Matches_debug
import pandas as pd
import os

# approved,unapproved,unsure = Run_Model_On_Punitive_Matches(mummichog_with_rts_mol_features,template_rt_file_dir,model_dir,file_dir)

cmpd_file = r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/xcmsScripts/Standards/ScherzoValidation/ribose.csv'
template_file = r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/xcmsScripts/Standards/ScherzoValidation/TemplateCmpds101020noribose.csv'
model_pickle_file =r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/xcmsScripts/Models/RanForc18predretandSMRTdata2.pickle'
file_dir = r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/xcmsScripts/'


def Run_Model_On_StandAlone_Cmpds(cmpd_file,template_file,model_pickle_file,file_dir=os.getcwd(),Threshold=1.0):
    pos_matches_with_mol_feature = Join_StandAlone_Molecular_Features(cmpd_file)
    approved,unapproved,unsure,predictions, prob_A,essential_df = Run_Model_On_Punitive_Matches_debug(pos_matches_with_mol_feature,template_file,model_pickle_file,file_dir,Threshold)
    return approved,unapproved,unsure,predictions, prob_A,essential_df
# approved,unapproved,unsure,predictions, prob_A,essential_df = Run_Model_On_StandAlone_Cmpds(cmpd_file,template_file,model_pickle_file,file_dir)