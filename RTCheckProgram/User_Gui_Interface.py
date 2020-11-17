import tkinter as tk 
import os
from Core_Code.Retention_Confirmation_Workflow import One_Click_Program
from Core_Code.MoleculeRepRT import main_compound_pic_generator
from Core_Code.Metabolism_overlap import Mummichog_Processer
from Core_Code.Run_Model_Standalone_Cmpds import Run_Model_On_StandAlone_Cmpds

def folder_iteration(folder,keep_ending=False,ending='.jpg'):
    if keep_ending == False:
        length_of_ending = len(ending)
        index = length_of_ending * -1
        return [file[:index] for file in os.listdir(folder) if file.endswith(ending)]
    else:
        return [file for file in os.listdir(folder) if file.endswith(ending)]



class Window1():
    def __init__(self,parent,*args,**kwargs):
        self.parent = parent
        parent.title("Retention Verification Software")
        folder_dir_lbl = tk.Label(parent,text='Enter the file path to your xcms results')
        folder_dir_lbl.grid(row=0,column=0)
        self.folder_dir = tk.StringVar(parent,value='C:\\Users\\rubya\\Desktop\\Forsberg Lab\\MainThesisFolderRTPred\\KristenResultsSpleen\\results\\')
        folder_dir_text_box = tk.Entry(parent,textvariable=self.folder_dir)
        folder_dir_text_box.grid(row=0,column=1)
        
        ret_standards_dir_lbl = tk.Label(parent,text='Select the reference standards to be used')
        ret_standards_dir_lbl.grid(row=1,column=0)
        self.ret_standards_dir = tk.StringVar(parent)
        self.ret_standards_dir.set('Select Standard File')
        stds = folder_iteration('Standards',ending='.csv')
        ret_standards_text_box = tk.OptionMenu(parent,self.ret_standards_dir,*stds)
        ret_standards_text_box.grid(row=1,column=1)
        
        
        model_dir_lbl = tk.Label(parent,text='Select to the model to be used')
        models = folder_iteration('Models',ending='.pickle')
        model_dir_lbl.grid(row=2,column=0)
        self.model_dir = tk.StringVar(parent)
        self.model_dir.set('Choose Model')
        model_dir_option_box = tk.OptionMenu(parent,self.model_dir,*models)
        model_dir_option_box.grid(row=2,column=1)
        
        Processing_Button = tk.Button(parent,text = "Begin Processing",command = self.Begin_Processing)
        Processing_Button.grid(row=3,column=0)
        
        self.Create_Picture_Button = tk.Button(parent,text = "Create Template Images",command = self.Create_Images)
        self.Create_Picture_Button.grid(row=3,column=1)
        
        Open_Picture_Window_Button = tk.Button(parent,text = "View Images", command = self.Open_Picture_Window)
        Open_Picture_Window_Button.grid(row=4,column=0)
        
        self.Launch_Pathway_Analysis = tk.Button(parent,text = "View Pathway Breakdown", command = self.Open_Pathway_Window)
        self.Launch_Pathway_Analysis.grid(row=4,column=1)
        
        self.Launch_Standalone_Processor = tk.Button(parent,text = "Stand Alone Processor", command = self.Open_Standalone_Window)
        self.Launch_Standalone_Processor.grid(row=5,column=0)
    
        
    def Begin_Processing(self):
        folder_dir_value = self.folder_dir.get()
        ret_standards_dir_value = 'Standards\\' + self.ret_standards_dir.get() + '.csv'
        model_dir_value = 'Models\\' + self.model_dir.get() + '.pickle'
        print(folder_dir_value + ret_standards_dir_value + model_dir_value)
        One_Click_Program(folder_dir_value,ret_standards_dir_value,model_dir_value)
        
    def Create_Images(self):
        self.Create_Picture_Button.destroy()
        self.Create_Picture_Button = tk.Button(self.parent,text = "Processing",command = self.Create_Images,relief=tk.SUNKEN)
        self.Create_Picture_Button.grid(row=3,column=1)
        self.Create_Picture_Button.config(relief=tk.SUNKEN,text='Processing')
        main_compound_pic_generator()
        # Create_Picture_Button.config(text='Done')
        self.Create_Picture_Button.destroy()
        lbl = tk.Label(self.parent,text="Picture Files Created")
        lbl.grid(row=3,column=1)
        
    def Open_Picture_Window(self):
        self.new_picture_window = Picture_window(self.parent)
        
    def Open_Pathway_Window(self):
        self.new_pathway_window = Pathway_window(self.parent,self.folder_dir)
    
    def Open_Standalone_Window(self):
        self.new_standalone_window = Processor_window(self.parent)
        
class Processor_window(tk.Tk):
    def __init__(self,parent,*args,**kwargs):
        self.parent = parent
        self.processor_window = tk.Toplevel(self.parent)
        
        lbl1 = tk.Label(self.processor_window,text = "Paste Directory of Standalone File")
        lbl1.grid(row=0,column=0)
        self.inchivar = tk.StringVar(self.processor_window,value = 'standalone file')
        txtbox1 = tk.Entry(self.processor_window,textvariable=self.inchivar)
        txtbox1.grid(row=0,column=1)
        process_button = tk.Button(self.processor_window,text= "Process",command=self.process_file)
        process_button.grid(row=3,column=0)
        
        ret_standards_dir_lbl = tk.Label(self.processor_window,text='Select the reference standards to be used')
        ret_standards_dir_lbl.grid(row=1,column=0)
        self.ret_standards_dir = tk.StringVar(self.processor_window)
        self.ret_standards_dir.set('Select Standard File')
        stds = folder_iteration('Standards',ending='.csv')
        ret_standards_text_box = tk.OptionMenu(self.processor_window,self.ret_standards_dir,*stds)
        ret_standards_text_box.grid(row=1,column=1)
        
        
        model_dir_lbl = tk.Label(self.processor_window,text='Select to the model to be used')
        models = folder_iteration('Models',ending='.pickle')
        model_dir_lbl.grid(row=2,column=0)
        self.model_dir = tk.StringVar(self.processor_window)
        self.model_dir.set('Choose Model')
        model_dir_option_box = tk.OptionMenu(self.processor_window,self.model_dir,*models)
        model_dir_option_box.grid(row=2,column=1)

    def process_file(self):
        file_dir = self.inchivar.get()
        ret_standards_dir_value = 'Standards\\' + self.ret_standards_dir.get() + '.csv'
        model_dir_value = 'Models\\' + self.model_dir.get() + '.pickle'
        approved,unapproved,unsure,predictions, prob_A,essential_df = Run_Model_On_StandAlone_Cmpds(file_dir,ret_standards_dir_value,model_dir_value)
        print(approved)
        print(unapproved)
        
class Picture_window(tk.Tk):
    def __init__(self,parent,*args,**kwargs):
        self.parent = parent
        self.pic_window = tk.Toplevel(self.parent)
        self.pic_window.title('Image Sorter')
        
        lbl = tk.Label(self.pic_window,text = "Choose Image to render")
        lbl.pack()
        
        self.tkvar_image = tk.StringVar(self.pic_window)
        self.tkvar_image.set('Choose Image')
        images = folder_iteration('labeled timeline')
        self.dropdown = tk.OptionMenu(self.pic_window,self.tkvar_image,*images)
        self.dropdown.pack()
        
        show_image = tk.Button(self.pic_window,text='Show Image', command = self.Render_Image)
        show_image.pack()
    def Render_Image(self):
        try:
            self.panel.destroy()
        except:
            pass
        complete_image_dir = os.getcwd() + '\\labeled timeline\\' + self.tkvar_image.get() + '.jpg'
        print(complete_image_dir)
        self.img = ImageTk.PhotoImage(file=complete_image_dir)
        self.panel = tk.Label(self.pic_window,image=self.img)
        self.panel.photo=self.img
        self.panel.pack()
        # canvas = tk.Canvas(self.pic_window,width = 300, height = 300)
        # canvas.create_image(20,20,anchow=tk.SW,image=img)

class Pathway_window(tk.Tk):
    def __init__(self,parent,folder_dir,*args,**kwargs):
        self.parent = parent
        self.pathway_window = tk.Toplevel(self.parent)
        self.pathway_window.title('Pathway Analysis')
        self.folder_dir = folder_dir.get()
        lbl = tk.Label(self.pathway_window,text="Choose Pathway")
        lbl.grid(row=0,column=0)
        
        lbl2 = tk.Label(self.pathway_window,text="Directory of result files")
        lbl2.grid(row=1,column=0)
        self.results_folder_dir = tk.StringVar(self.pathway_window,value=r'C:/Users/rubya/Desktop/Forsberg Lab/MainThesisFolderRTPred/KristenResults/results/RT_Folder/')
        folder_dir_text_box = tk.Entry(self.pathway_window,textvariable=self.results_folder_dir)
        folder_dir_text_box.grid(row=1,column=1)
        
        self.tkvar_pathways = tk.StringVar(self.pathway_window)
        self.tkvar_pathways.set('Pathway')
        file = self.folder_dir + 'mummichog//tsv//mcg_pathwayanalysis_mummichog.tsv' 
        self.mummichog_obj = Mummichog_Processer(file)
        pathways = sorted(self.mummichog_obj.Pull_List_of_Pathways())
        self.dropdown = tk.OptionMenu(self.pathway_window,self.tkvar_pathways,*pathways)
        self.dropdown.grid(row=0,column=1)
        
        show_stats_button  = tk.Button(self.pathway_window,text = 'Pull Pathway',command = self.render_pathway_df)
        show_stats_button.grid(row=2,column=0)
        
        write_all_pathway_file = tk.Button(self.pathway_window,text = 'Output Pathway Analysis File',command=self.print_pathway_file)
        write_all_pathway_file.grid(row=2,column=1)
    def render_pathway_df(self):
        results = tk.Text(self.pathway_window,width=130)
        # callable_dict = self.mummichog_obj.Get_Dict()
        results_folder = self.results_folder_dir.get()
        mummichog_df = self.mummichog_obj.Render_DF_Pathway(self.tkvar_pathways.get(),results_folder)
        results.insert(tk.END,mummichog_df)
        results.insert(tk.END,"\nList of potential metabolites")
        
        
        for metab in self.mummichog_obj.Pull_Metabolites(self.tkvar_pathways.get()):
            results.insert(tk.END,"\n" + metab)
        results.grid(row=2,column=0)
        
    def print_pathway_file(self):
        self.mummichog_obj.print_file_all_pathways(self.results_folder_dir.get())
        

if __name__=='__main__':
    root=tk.Tk()
    Window1(root)
    root.mainloop()
    

# Main_Window = tk.Tk()
# Main_Window.title("Retention Verification Software")

# folder_dir_lbl = tk.Label(Main_Window,text='Enter the file path to your xcms results')
# folder_dir_lbl.grid(row=0,column=0)
# folder_dir = tk.StringVar(Main_Window,value='C:\\Users\\rubya\\Desktop\\Forsberg Lab\\MainThesisFolderRTPred\\KristenResults\\results\\')
# folder_dir_text_box = tk.Entry(Main_Window,textvariable=folder_dir)
# folder_dir_text_box.grid(row=0,column=1)

# ret_standards_dir_lbl = tk.Label(Main_Window,text='Enter the file path to the standard rt file')
# ret_standards_dir_lbl.grid(row=1,column=0)
# ret_standards_dir = tk.StringVar(Main_Window,value=r'C:\Users\rubya\Desktop\Forsberg Lab\MainThesisFolderRTPred\csvfiles\TemplateCompounds.csv')
# ret_standards_text_box = tk.Entry(Main_Window,textvariable=ret_standards_dir)
# ret_standards_text_box.grid(row=1,column=1)


# model_dir_lbl = tk.Label(Main_Window,text='Enter the file path to the model to be used')
# model_dir_lbl.grid(row=2,column=0)
# model_dir = tk.StringVar(Main_Window,value=r"C:\Users\rubya\Desktop\Forsberg Lab\MainThesisFolderRTPred\pickles\RFClassifier.pickle")
# model_dir_text_box = tk.Entry(Main_Window,textvariable=model_dir)
# model_dir_text_box.grid(row=2,column=1)

# def Begin_Processing():
#     Processing_Button.config(relief=tk.SUNKEN,text='Processing')
#     folder_dir_value = folder_dir.get()
#     ret_standards_dir_value = ret_standards_dir.get()
#     model_dir_value = model_dir.get()
#     print(folder_dir_value + ret_standards_dir_value + model_dir_value)
#     One_Click_Program(folder_dir_value,ret_standards_dir_value,model_dir_value)
    
# def Create_Images():
#     Create_Picture_Button.destroy()
#     Create_Picture_Button = tk.Button(Main_Window,text = "Processing",command = Create_Images,relief=tk.SUNKEN)
#     Create_Picture_Button.grid(row=3,column=1)
#     # Create_Picture_Button.config(relief=tk.SUNKEN,text='Processing')
#     main_compound_pic_generator()
#     # Create_Picture_Button.config(text='Done')
#     Create_Picture_Button.destroy()
#     lbl = tk.Label(Main_Window,text="Picture Files Created")
#     lbl.grid(row=3,column=1)

# Processing_Button = tk.Button(Main_Window,text = "Begin Processing",command = Begin_Processing)
# Processing_Button.grid(row=3,column=0)

# Create_Picture_Button = tk.Button(Main_Window,text = "Create Template Images",command = Create_Images)
# Create_Picture_Button.grid(row=3,column=1)




# Main_Window.mainloop()




