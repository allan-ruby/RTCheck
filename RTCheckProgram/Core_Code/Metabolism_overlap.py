import pandas as pd
import numpy as np
    

def metabolite_string_builder(list_of_cmpds):
    string = ''
    for cmpd in list_of_cmpds:
        string += cmpd + '.'
    return string

class Mummichog_Processer():
    """Class meant to instantiate the pathway analysis file"""
    def __init__(self,file_path):
        pathway_df = pd.read_csv(file_path,sep='\t')
        self.pathway_dict = {}
        for index,row in pathway_df.iterrows():
            if row[0] == '++++++':
                break
            else:
                pathway_name_key = row[0]
                path_id = row[1]
                pathway_hits = row[2]
                pathway_size = row[3]
                unprocessed_names_hits = row[6]
                try:
                    split_list_names = unprocessed_names_hits.split('$')
                except:
                    pass
            self.pathway_dict[pathway_name_key] = [path_id,pathway_hits,pathway_size,split_list_names]
        
         
    def Get_Dict(self):
        """ Returns the pathway dictionary with the following format pathway:[path_id,pathway_hits,pathway_size,split_list_names]"""
        return self.pathway_dict
    
    def Pull_Metabolites(self,pathway):
        """Returns the list of metabolites in that pathway"""
        value_list = self.pathway_dict[pathway]
        return value_list[3]
    
    def Pull_List_of_Pathways(self):
        """Returns a list of all the metabolites """
        return_list =[str(key) for key in self.pathway_dict.keys()]
        return return_list

    def Render_DF_Pathway(self,pathway,filedir):
        approved_cmpds = [row[1] for index,row in pd.read_csv(filedir + 'approved.csv').iterrows()]
        approved_hits = [match for match in self.Pull_Metabolites(pathway) if match in approved_cmpds]
        unapproved_cmpds = [row[1] for index,row in pd.read_csv(filedir + 'unapproved.csv').iterrows()]
        unapproved_hits = [match for match in self.Pull_Metabolites(pathway) if match in unapproved_cmpds]
        unsure_cmpds = [row[1] for index,row in pd.read_csv(filedir + 'unsure.csv').iterrows()]
        unsure_hits = [match for match in self.Pull_Metabolites(pathway) if match in unsure_cmpds]
        # approved_cmpds = len([match for match in self.Pull_Metabolites(pathway) if match in [row[1] for index,row in pd.read_csv(filedir + 'approved.csv')]])
        # unapproved_cmpds = len([match for match in self.Pull_Metabolites(pathway) if match in [row[1] for index,row in pd.read_csv(filedir + 'unapproved.csv')]])
        # unsure_cmpds = len([match for match in self.Pull_Metabolites(pathway) if match in [row[1] for index,row in pd.read_csv(filedir + 'unsure.csv')]])
        list_of_data = self.pathway_dict[pathway]
        
        df = pd.DataFrame({'Pathway ID': list_of_data[0], 'Pathway Hits': list_of_data[1],'Pathway Size' : list_of_data[2], 'Approved Hits': len(approved_hits),'Negative Hits':len(unapproved_hits),'Unsure Hits':len(unsure_hits),
                           'Approved Metabolites':metabolite_string_builder(approved_hits),'Unapproved Metabolites':metabolite_string_builder(unapproved_hits),'Unsure Metabolites':metabolite_string_builder(unsure_hits)},index=[0])
        return df
    
    def cross_compare_model_results(self,pathway,filedir):
        approved_cmpds = [row[1] for index,row in pd.read_csv(filedir).iterrows()]
        punitive = self.Pull_Metabolites(pathway)
        list_of_approved_metabs =[]
        for pun in punitive:
            if pun in approved_cmpds:
                list_of_approved_metabs.append(pun)
        return list_of_approved_metabs
    
    def return_list_na_compounds(self,pathway,approved_filedir,unapproved_filedir,unsure_filedir):
        punitive = self.Pull_Metabolites(pathway)
        approved_cmpds = [row[1] for index,row in pd.read_csv(approved_filedir).iterrows()]
        unapproved_cmpds = [row[1] for index,row in pd.read_csv(unapproved_filedir).iterrows()]
        unsure_cmpds = [row[1] for index,row in pd.read_csv(unsure_filedir).iterrows()]
        final_list = []
        for pun in punitive:
            if pun not in approved_cmpds:
                if pun not in unapproved_cmpds:
                    if pun not in unsure_cmpds:
                        final_list.append(pun)
        return final_list
                
    def print_file_all_pathways(self,filedir):
        list_of_df = []
        for pathway in self.Pull_List_of_Pathways():
            try:
                pathway_df = self.Render_DF_Pathway(pathway,filedir)
                pathway_df['Pathway Name'] = pathway
                list_of_df.append(pathway_df)
            except:
                pass
        whole_df = pd.concat(list_of_df)
        whole_df.to_csv(filedir+'pathwayRTanalysis.csv',index=False)
            
        




# mummichog_obj = Mummichog_Processer('C://Users//rubya//Desktop//Forsberg Lab//MainThesisFolderRTPred//KristenResults//results//mummichog//tsv//mcg_pathwayanalysis_mummichog.tsv')
# approved_file_dir = 'C://Users//rubya//Desktop//Forsberg Lab//MainThesisFolderRTPred//KristenResults//results//RT_Folder//approved.csv'
# unapproved_file_dir = 'C://Users//rubya//Desktop//Forsberg Lab//MainThesisFolderRTPred//KristenResults//results//RT_Folder//unapproved.csv'
# unsure_file_dir = 'C://Users//rubya//Desktop//Forsberg Lab//MainThesisFolderRTPred//KristenResults//results//RT_Folder//unsure.csv'
# missing_cmpds = mummichog_obj.return_list_na_compounds('bile acid biosynthesis, neutral pathway',approved_file_dir,unapproved_file_dir,unsure_file_dir)
# unapproved = [row[1] for index,row in pd.read_csv(unapproved_file_dir).iterrows()]
# # mummichog_dict = mummichog_obj.Get_Dict()
# tca_results = mummichog_obj.Render_DF_Pathway('bile acid biosynthesis, neutral pathway',r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/KristenResults/results/RT_Folder/')
# mummichog_obj.print_file_all_pathways(r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/KristenResults/results/RT_Folder/')
# # tca_metabs = mummichog_obj.Pull_Metabolites('bile acid biosynthesis, neutral pathway')
# keys = mummichog_obj.Pull_List_of_Pathways()
# approved_pathway_hits = mummichog_obj.cross_compare_model_results('bile acid biosynthesis, neutral pathway',approved_file_dir)
# false_hits = mummichog_obj.cross_compare_model_results('bile acid biosynthesis, neutral pathway',unapproved_file_dir)
# unsure_hits = mummichog_obj.cross_compare_model_results('bile acid biosynthesis, neutral pathway',unsure_file_dir)