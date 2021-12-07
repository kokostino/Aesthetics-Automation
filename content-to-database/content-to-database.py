from PIL import Image
import numpy as np
from skimage import transform
import os
import csv
import tensorflow as tf
import sqlite3

path='C:\\Users\\dherschmann\\Documents\\GitHub\\Instagram-Automation\\database'
model = tf.keras.models.load_model("my_model.h5")

def load(filename):
    np_image = Image.open(filename)
    np_image = np.array(np_image).astype('float32')/255
    np_image = transform.resize(np_image, (224, 224, 3))
    np_image = np.expand_dims(np_image, axis=0)
    return np_image

def write_content_data_to_database(content_info):
    conn = sqlite3.connect('C:\\Users\\dherschmann\\Documents\\GitHub\\Instagram-Automation\\database\\instagram.sqlite')
    cur = conn.cursor()
    for line in content_info:

        name = line[0]
        content = line[1]

        cur.execute('''INSERT OR IGNORE INTO IMAGE_INFO (IMAGE_NAME, IMAGE_CLASS_CALC) VALUES (?,?)''',
        (name, content))
        cur.execute('''UPDATE IMAGE_INFO SET IMAGE_CLASS_CALC = ? WHERE IMAGE_NAME=?''',
        (content, name))
    conn.commit()

def read_from_file(file):            
    with open(file, newline='') as csvfile:
        already_in_db=[]
        csv.register_dialect("custom", delimiter=",", skipinitialspace=True)
        reader = csv.reader(csvfile, dialect='custom')
        for row in reader:
            if row!=[]:
                already_in_db.append(row[0])  
        return already_in_db
    
def write_to_file(content, file):    
    with open(file, "a") as the_file:
        csv.register_dialect("custom", delimiter=",", skipinitialspace=True)
        writer = csv.writer(the_file, dialect="custom")
        for tup in content:
            writer.writerow(tup)
            
image_names=os.listdir(path+"/Favs")

# for image in read_from_file('database/content.csv'):
#         image_names.remove(path+"/Favs/"+image) 

list_of_problematic_images=[]
content_info=[]

for i in image_names:
    try:
        img = load(path+'/Favs/'+i)
        a=model.predict(img)
        content=str(np.argmax(a)).replace('0','palm').replace('1','rest').replace('2','snow')
        i='Images\\'+i
        content_info.append((i, content))
    except:
        list_of_problematic_images.append((i))
        
write_content_data_to_database(content_info)         
write_to_file(content_info, path+ "/content.csv")  
write_to_file(list_of_problematic_images,path+ "/has_issues_content.csv")