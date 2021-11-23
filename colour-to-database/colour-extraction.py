import cv2
import numpy as np
import pandas as pd
import glob
import sqlite3
import shutil
import os
import csv
from PIL import Image
from skimage.color import rgb2lab, deltaE_ciede2000
from sklearn_extra.cluster import KMedoids

import warnings
warnings.filterwarnings("ignore")

def copy_and_overwrite(from_path, to_path):
    if os.path.exists(to_path):
        shutil.rmtree(to_path)
    shutil.copytree(from_path, to_path)


# pixels in an image and their distances to eachother in deltaE_ciede2000
class pixel_distances_within_image():
    def __init__(self,pic):
        self.pic=pic
    def smallify_image(self,n):
        imgs = Image.open(self.pic) 
        imgs.thumbnail((n, n))# n=20, m=20
        return imgs.save(self.pic)
    def reshape(self):
        image = cv2.imread(self.pic)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        image = image.reshape((image.shape[0] * image.shape[1], 3))
        return image
    def transform2lab(self):
        return rgb2lab(self.reshape())
    def distances_between_pixel_df(self):
        dislab=pd.DataFrame()
        image=self.transform2lab()
        for i in range(0,len(image)-1):
            l = [0] * (i+1)
            lo=pd.DataFrame()
            for j in range(i+1,len(image)):
                data=deltaE_ciede2000(image[i],image[j])
                l.append(data)
            lo=lo.append(l).T
            dislab=dislab.append(lo).reset_index(drop=True)
        dislabT=dislab.T.reset_index(drop=True)
        distance_df=dislab.reset_index(drop=True).add(dislabT, fill_value=0).fillna(0)
        return distance_df

#calculate dominant colour clusters with KMedoids
class dominant_colours_via_KMedoids(): 
    def __init__(self, df):
        self.distance_df=df
    def kmedoids_labels(self,n_clusters=5):
        kmedoids = KMedoids(n_clusters,metric='precomputed').fit(self.distance_df)
        labels = kmedoids.predict(self.distance_df)
        #cc=kmedoids.cluster_centers_
        return labels
    def cluster(self, image, n_clusters=5):
        labels=self.kmedoids_labels()
        dist=self.distance_df
        dist.insert(0, 'Cluster Labels', labels)
        centroids=[]
        for n in range(0,n_clusters):
            cluster=dist.loc[dist['Cluster Labels'] == n][dist.index[dist['Cluster Labels'] == n].tolist()]
            summe=cluster.sum(axis=1)
            cluster['sum']=summe
            centroid_row=cluster.loc[cluster['sum']==min(summe)]
            centroid=centroid_row.index[0]
            centroids.append(image[centroid])
        return labels, centroids
    
    
def format_five_clusters(clstr):
    return str(clstr[1][0].tolist())+str(clstr[1][1].tolist())+str(clstr[1][2].tolist())+str(clstr[1][3].tolist())+str(clstr[1][4].tolist())

def write_colour_data_to_database(colour_info):
    conn = sqlite3.connect('C:\\Users\\dherschmann\\Documents\\GitHub\\Instagram-Automation\\database\\instagram.sqlite')
    cur = conn.cursor()
    for line in colour_info:

        name = line[0]
        colours = line[1]

        cur.execute('''INSERT OR IGNORE INTO IMAGE_INFO (IMAGE_NAME, IMAGE_COLOUR) VALUES (?,?)''',
        (name, colours))

    conn.commit()
    
def write_to_file(content, file):    
    with open(file, "a") as the_file:
        csv.register_dialect("custom", delimiter=",", skipinitialspace=True)
        writer = csv.writer(the_file, dialect="custom")
        for tup in content:
            writer.writerow(tup)

def read_from_file(file):            
    with open(file, newline='') as csvfile:
        already_in_db=[]
        csv.register_dialect("custom", delimiter=",", skipinitialspace=True)
        reader = csv.reader(csvfile, dialect='custom')
        for row in reader:
            if row!=[]:
                already_in_db.append(row[0])  
        return already_in_db
            
os.chdir('C:\\Users\\dherschmann\\Documents\\GitHub\\Instagram-Automation')    
    
image_names=glob.glob("colour-to-database/Images/*.jpg")

for image in read_from_file('database/colours.csv'):
        image_names.remove('colour-to-database/'+image) 

#scale down images to 20x20 pixels
for i in image_names:
    pixel_distances_within_image(i).smallify_image(20)


list_of_problematic_images=[]
colour_info=[]

for i in image_names:
    try:
        bsp=pixel_distances_within_image(i)
        dom=bsp.distances_between_pixel_df()
        km=dominant_colours_via_KMedoids(dom)
        clstr=km.cluster(bsp.reshape())
        i=i.replace('colour-to-database/','')
        colours=format_five_clusters(clstr)
        colour_info.append((i, colours))
    except:
        list_of_problematic_images.append((i))
        
write_colour_data_to_database(colour_info)         
write_to_file(colour_info, "database/colours.csv")  
write_to_file(list_of_problematic_images, "database/has_issues_colours.csv")  