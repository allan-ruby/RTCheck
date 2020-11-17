import pandas as pd
from PredRetDatabaseProcessor import fps_plus_mw, mol_prop_gen


def Pred_Ret_Processor(Pred_Ret_Df,Col_parameters,system_type,outfile):
    """This function takes in previously created files of the predret database PredRetDB.csv, 
    Predret file that denotes all system parameters for each system column_parameters.csv
    """
    col_dict = {}
    for indx,row in Col_parameters.iterrows():
    	if row[3] not in col_dict:
    		col_dict[row[3]] = [row[0]]
    	else:
    		value = col_dict[row[3]]
    		value.append(row[0])
    		col_dict[row[3]] = value
    system_dict = {}
    for indx,row in Col_parameters.iterrows():
    	system_dict[row[0]] = row[3]
    df_list = []	
    for indx,row in Pred_Ret_Df.iterrows():
    	try:
    		col = system_dict[row[2]]
    	except:
    		break
    	if col == system_type:
    		df_list.append(row)
    
    system_results = pd.DataFrame(df_list)
    mol_prop_gen(system_results,outfile)
    
Pred_Ret_DF = pd.read_csv(r'C:\Users\rubya\Desktop\Forsberg Lab\MainThesisFolderRTPred\csvfiles\PredRetDB.csv')
phase_type_df = pd.read_csv(r'C:\Users\rubya\Desktop\Forsberg Lab\MainThesisFolderRTPred\csvfiles\PredRetsystemtocoltype.csv')
col_parameters = pd.read_csv(r'C:\Users\rubya\Desktop\Forsberg Lab\MainThesisFolderRTPred\csvfiles\column_parameters.csv')
system = 'Merck SeQuant ZIC-pHILIC column'
Pred_Ret_Processor(Pred_Ret_DF,col_parameters,system,'MerckHILIC.p')

# hilic_systems = ['MTBLS87','Cao_HILIC','KI_GIAR_zic_HILIC_pH2_7',]
# for sys in hilic_systems:
#     Pred_Ret_Processor(Pred_Ret_DF,col_parameters,system,sys + '.p')