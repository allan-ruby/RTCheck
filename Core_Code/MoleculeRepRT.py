from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import MolToFile
from rdkit.Chem import AllChem
from PIL import Image,ImageDraw,ImageFont
import pickle
import pandas as pd
import os
import pubchempy as pcp

# template = Chem.MolFromSmiles('c1nccc2n1ccc2')
# img = Chem.Draw.MolToFile(template,'example.png')


def inchi_image_processor(inchi,name):
    template = Chem.MolFromInchi(inchi)
    img = Chem.Draw.MolToFile(template,name+'.png')
    return name + ' has been saved'

def mol_image_processor(mol,name):
    Chem.Draw.MolToFile(mol,name+'.png')
    return name + ' has been saved'

def merge_images(image_list):
    """Merge images into one, displayed side by side
    :param file1: path to first image file
    :param file2: path to second image file
    :return: the merged Image object
    """
    open_images = [Image.open(file) for file in image_list]
    # image1,image2,image3 = Image.open(file1),Image.open(file2),Image.open(file3)
    width, height = open_images[0].size
    result_width = width * len(image_list)
    # result_height = height
    result = Image.new('RGB', (result_width, height))
    for index,img in enumerate(open_images):
        result.paste(im=img,box=(width*index,0))
    # result.paste(im=image1, box=(0, 0))
    # result.paste(im=image2, box=(width1, 0))
    # result.paste(im=image3,box=(width1+width2,0))
    return result

def label_pictures_from_dict(the_dict,ext,color_string):
    counter = 1
    for k,v in the_dict.items():
        print(counter)
        print(k)
        counter +=1
        try:
            os.makedirs('raw_mol_pics/')
        except OSError:
            pass
        try:
            raw_file_dir = 'raw_mol_pics/' + k + ext
            mol_image_processor(v[1],raw_file_dir )
            image = Image.open(raw_file_dir + '.png')
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf',15)
            text = k + ' RT: ' + str(v[0]) + '\nxlogp:' + str(v[2])
            draw.text((25,225),text,fill=color_string,font=font)
            try:
                os.makedirs('label_mol_pics/')
            except OSError:
                pass
            labeled_dir =  'label_mol_pics/' + k + ext + '.jpg'
            image.save(labeled_dir)
        except IOError:
            print('image unavailable')
            pass


def mummichog_pickle_and_template_to_dicts(mummi_pickle,template_std):
    df = pickle.load(open(mummi_pickle,'rb'))
    my_cmpd_dict = {}
    for index,row in df.iterrows():
    
        name = row['Name']
        rt = row['RT']
        mol = row['mol']
        xlogp = row['xlogp']
        my_cmpd_dict[name]=[rt,mol,xlogp]
    my_std_dict = {}
    std_rt_dict = {}
    template_compounds_df = pd.read_csv(template_std)
    for index,row in template_compounds_df.iterrows():
        mol  = Chem.MolFromInchi(row['Inchi'])
        cmpd = pcp.get_compounds(row['Inchi'],'inchi')
        props = cmpd[0].to_dict(properties=['cactvs_fingerprint',
                        'isomeric_smiles', 'xlogp', 'rotatable_bond_count','charge','complexity',
                        'exact_mass','fingerprint'])
        rt = row['RT']
        name = row['Name']
        xlogp = props['xlogp']
        my_std_dict[name] = [rt,mol,xlogp]
        std_rt_dict[rt] = name
    return my_cmpd_dict,my_std_dict,std_rt_dict
#this works to generate all images, pretty fast!  

    
def create_timeline_images(csv_dir,std_rt_dict):
    approved_df = pd.read_csv(csv_dir)
    counter = 0
    for index,row in approved_df.iterrows():
        pun_cmpd = row['Name']
        try:
            os.makedirs('labeled timeline/')
        except OSError:
            pass
        if int(row['Low Range']) == 0:
            try:
                hr_cmpd = std_rt_dict[row['High Range']]
                image = merge_images(['label_mol_pics/'+ pun_cmpd + '-cmpd.jpg', 'label_mol_pics/' + hr_cmpd + '-std.jpg'])
                image.save('labeled timeline/' + pun_cmpd + '.jpg')
            except:
                counter +=1
                print('{} are images unavailable'.format(counter))
        elif row['High Range'] == 100:
            try:
                lr_cmpd = std_rt_dict[row['Low Range']]
                image = merge_images(['label_mol_pics/'+lr_cmpd + '-std.jpg', 'label_mol_pics/'+ pun_cmpd + '-cmpd.jpg'])
                image.save('labeled timeline/' + pun_cmpd + '.jpg')
            except:
                counter +=1
                print('{} are images unavailable'.format(counter))
        else:
            lr_cmpd = std_rt_dict[row['Low Range']]
            hr_cmpd = std_rt_dict[row['High Range']]
            try:
                image = merge_images(['label_mol_pics/'+lr_cmpd + '-std.jpg', 'label_mol_pics/'+ pun_cmpd + '-cmpd.jpg', 'label_mol_pics/' + hr_cmpd + '-std.jpg'])
                image.save('labeled timeline/' + pun_cmpd + '.png')
            except:
                counter +=1
                print('{} are images unavailable'.format(counter))
    print('{} out of {} images are available'.format(counter,len(approved_df)))

def main_compound_pic_generator():
    my_cmpd_dict,my_std_dict,std_rt_dict = mummichog_pickle_and_template_to_dicts('mummichog_rt_features.p','TemplateCompounds.csv')
    label_pictures_from_dict(my_std_dict,'-std','#CD5C5C')
    label_pictures_from_dict(my_cmpd_dict,'-cmpd','#17202A')
    create_timeline_images('approved.csv',std_rt_dict) 
    
# main_compound_pic_generator()
# df = pickle.load(open('mummichog_rt_features.p','rb')) 
# template_compounds_df = pd.read_csv('TemplateCompounds.csv')    
    
    
    
    
    
    
    
    
    
    
    
    
    