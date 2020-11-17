from Retention_Confirmation_Workflow import Join_StandAlone_Molecular_Features,Run_Model_On_Punitive_Matches_debug
import pandas as pd


def Compile_Results_By_RT(approved_df,unapproved_df,diff_report,out_dir):

    
    app_rt_dict = {}
    for index,row in approved_df.iterrows():
        actual_rt = row['Actual Retention Time']
        if actual_rt not in app_rt_dict.keys():
            app_rt_dict[actual_rt] = row[1]
        else:
            list_of_approved =app_rt_dict[actual_rt]
            list_of_approved += ',' + row[1]
            app_rt_dict[actual_rt] = list_of_approved
            
    unapp_rt_dict = {}
    for index,row in unapproved_df.iterrows():
        actual_rt = row['Actual Retention Time']
        if actual_rt not in unapp_rt_dict.keys():
            unapp_rt_dict[actual_rt] = row[1]
        else:
            list_of_unapproved =unapp_rt_dict[actual_rt]
            list_of_unapproved += ',' + row[1]
            unapp_rt_dict[actual_rt] = list_of_unapproved
            
    diff_report=pd.read_csv(diff_report,sep='\t')
    rt_feature_dict = {}
    for index,row in diff_report.iterrows():
        rt = round(row['rtmin'],10)
        feature_id = row['featureidx']
        if rt not in rt_feature_dict.keys():
            rt_feature_dict[rt] = [feature_id]
        else:
            feature_list = rt_feature_dict[rt]
            feature_list.append(feature_id)
            rt_feature_dict[rt] = feature_list
    # if no_unsure == True        
    # unsure_rt_dict = {}
    # for index,row in unsure_df.iterrows():
    #     actual_rt = row['Actual Retention Time']
    #     if actual_rt not in unsure_rt_dict.keys():
    #         unsure_rt_dict[actual_rt] = row[1]
    #     else:
    #         list_of_unsure =unsure_rt_dict[actual_rt]
    #         list_of_unsure += ',' + row[1]
    #         unsure_rt_dict[actual_rt] = list_of_unsure
            
            
    app_df = pd.DataFrame.from_dict(app_rt_dict,orient='index')
    unapp_df = pd.DataFrame.from_dict(unapp_rt_dict,orient='index')
    merge1_df = app_df.merge(unapp_df,how='outer',left_index=True, right_index=True)
    
    merge1_df.columns = ['Approved','Unapproved']
    merge1_df=merge1_df.rename_axis('Retention Time')
    df_feat_list = []
    for index,row in merge1_df.iterrows():
        try:
            rt = round(index,10)
            list_of_features = rt_feature_dict[rt]
            index_cont = 0
            feature_str = ''
            for feature in list_of_features:
                if index_cont == 0:
                    feature_str += str(feature)
                    index_cont +=1
                else:
                    what_to_add = '/' + str(feature)
                    feature_str = feature_str + what_to_add
            df_feat_list.append(feature_str)
        except KeyError:
            df_feat_list.append('Retention Time Rounding Error')
    print(len(df_feat_list))
    merge1_df['Feaure ID'] = df_feat_list
    merge1_df.to_csv(out_dir + 'BreakdownByRT.csv')
    return merge1_df

file_dir = r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/KristenResultsKidney/results/'

approved = file_dir + 'RT_Folder/approved.csv'
unapproved = file_dir + 'RT_Folder/unapproved.csv'
diff_report = file_dir + 'DiffReport.tsv'
# unsure = r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/KristenResults/results/RT_Folder/unsure.csv'

Final_DF = Compile_Results_By_RT(approved,unapproved,diff_report,file_dir + 'RT_Folder/')