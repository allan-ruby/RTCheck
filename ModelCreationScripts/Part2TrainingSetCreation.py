import pickle
import pandas as pd



def create_training_set(training_set_df,output):
    """
    

    Parameters
    ----------
    training_set_df : Need to unpickle the file from part 1,
    feed into this function compare each molecule to start training 
    model to learn what molecules come after the other
    output : this is the name of the output pickle.

    Returns
    -------
    train_df : TYPE
        DESCRIPTION.

    """
    df_list = []
    col_A = []
    col_B = []
    for index,col in enumerate(training_set_df.columns):
        if index < 159:
            col_A.append('A' + str(index))
            col_B.append('B' + str(index))
        else:
            col_A.append('A' + col)
            col_B.append('B' + col)
    for i in range(len(training_set_df)):
        print('On index {}'.format(i))
        first_part= training_set_df.iloc[[i]]
        first_part.columns=col_A
        first_part = first_part.reset_index()
        for i2 in range(i+1,len(training_set_df)):
    #        print(i2)
            entry=[]
            second_part = training_set_df.iloc[[i2]]
            second_part.columns=col_B
            second_part = second_part.reset_index()
            entry = [first_part,second_part]
            df = pd.concat(entry,axis=1)
            df_list.append(df)
    train_df = pd.concat(df_list,ignore_index=True)
    RT_status = []
    for index,row in train_df.iterrows():
    #    print(row['ART'],row['BRT'])
        a_RT = float(row['ART'])
        b_RT = float(row['BRT'])
        if a_RT == b_RT:
            RT_status.append('error')
        elif a_RT < b_RT:
            RT_status.append(0)
        elif a_RT > b_RT:
            RT_status.append(1)
        else:
            RT_status.append('error')
    train_df['Result'] = RT_status
    for index,row in train_df.iterrows():
        if row['Result'] == 'error':
            train_df = train_df.drop(index)
    train_df =train_df.drop(['ART','BRT','AName','BName','index','Amol','Bmol','Aisomeric_smiles','Bisomeric_smiles','ASystem','BSystem','Afingerprint','Bfingerprint','Acactvs_fingerprint','Bcactvs_fingerprint'],axis=1)
    train_df = train_df.fillna(0)

    train_df.to_csv(output)
    return train_df



infile = open('output.p','rb')
complete_DF= pickle.load(infile)
system_dict = {}

for index,row in complete_DF.iterrows():
    if row['System'] not in system_dict.keys():
      system_dict[row['System']] = [index]
    else:
      value = system_dict[row['System']]
      value.append(index)
      system_dict[row['System']] = value
list_of_dataframes = []
for key in system_dict.keys():
    inter_df_list = []
    idx_list = system_dict[key]
    for index,row in complete_DF.iterrows():
        if index in idx_list:
            inter_df_list.append(row)
    inter_df = pd.DataFrame(inter_df_list)
    list_of_dataframes.append([key,inter_df])
# col_A = []
# col_B = []
# for index,col in enumerate(complete_DF.columns):
#     if index < 159:
#        col_A.append('A' + str(index))
#        col_B.append('B' + str(index))
#     else:
#         col_A.append('A' + col)
#         col_B.append('B' + col)
# ###Creating a training set from FEM long
# ###FEM_long    412    Reversed-phase    Waters ACQUITY UPLC HSS T3 C18    acidic    Water:MeOH    0.1% FA    10.1007/s11306-011-0298-z
# ### C18 column, 50:50
# for tup in list_of_dataframes:
#     if tup[0] == 'FEM_long':
#         df_fem_long = tup[1]
#     if tup[0] == 'FEM_orbitrap_plasma':
#         df_orb_plasma = tup[1]
#     if tup[0] == 'MTBLS36':
#         df_MTBLS36 = tup[1]
# #first_part = []
# #second_part = []
# df_MTBLS36 = create_training_set(df_MTBLS36,'MTBLS36.csv')
# df_fem_long =create_training_set(df_fem_long,'fem_long.csv')
# df_orb_plasma = create_training_set(df_orb_plasma,'orb_plasma.csv')
# list_of_pickles = ['MerckHILIC.p']
# mtbls87 = []
# Cao_HILIC = []
# for pick in list_of_pickles:
#     print('On column {}'.format(pick[0:-2]))
#     unpickled = pickle.load(open(pick,'rb'))
#     for index,row in unpickled.iterrows():
#         if row['System'] == 'MTBLS87':
#             mtbls87.append(row)
#         if row['System'] == 'Cao_HILIC':
#             Cao_HILIC.append(row)
# Cao_HILIC_df = pd.DataFrame(Cao_HILIC)
# mtbls87_df = pd.DataFrame(mtbls87)
# cao_training_set = create_training_set(Cao_HILIC_df,'Cao_HILIC.csv')
# mtbl_training_set = create_training_set(mtbls87_df,'mtbls87.csv')
#     # ts_df = create_training_set(unpickled,pick[0:-2] + '.csv')
# print('output written')

