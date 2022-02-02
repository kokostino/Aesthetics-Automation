import pandas as pd
import sqlite3
from sklearn.cluster import KMeans
import cv2
import ast
from skimage.color import deltaE_ciede2000
import matplotlib.pyplot as plt
import numpy as np


path='C:\\Users\\dherschmann\\Documents\\GitHub\\Instagram-Automation\\database\\'
path2='C:\\Users\\dherschmann\\Documents\\GitHub\\Instagram-Automation\\posted-pics\\second_sequence\\'

sql='SELECT * FROM IMAGE_INFO WHERE IMAGE_CLASS_CALC="snow" and IMAGE_COLOUR is not null'
conn = sqlite3.connect('database/Instagram.sqlite')
cur = conn.cursor()
cur.execute(sql)
SnowList =cur.fetchall()
names=[plyr[0] for plyr in SnowList]
player=[plyr[1] for plyr in SnowList]

def pxl_of_image(i):
    p=[]
    for pl in player[i].split(']['):
        pl=pl.replace('[','').replace(']','')
        p.append(list(ast.literal_eval(pl)))
    return p


def distance_vec(lab1,lab2):
    dist=[]
    for pxl1 in range(0,len(lab1)):
        idis=[]
        for pxl2 in range(0,len(lab2)):
            d=deltaE_ciede2000(lab1[pxl1], lab2[pxl2])
            idis.append(d)
        dist.append(min(idis))
    return dist 


def similarity_vec(lab1,lab2,smlrty_threshold):
    sim_vec=[]
    for d in distance_vec(lab1,lab2):
        if smlrty_threshold<d<smlrty_threshold*2:
            sim_vec.append(1)
        if d<smlrty_threshold:
            sim_vec.append(2)        
        else:
            sim_vec.append(0)
    return sim_vec 

sim=pd.DataFrame(index=names, columns=names)

for i in range(0,len(SnowList)-1):
    
    for j in range(i,len(SnowList)):
        if j==i:
            sim.at[names[i],names[j]] = 10/2
        else:
            sim.at[names[i],names[j]] = sum(similarity_vec(pxl_of_image(i),pxl_of_image(j),3.5))
sim=sim.fillna(0)+sim.T.fillna(0)    


kmeans = KMeans(n_clusters=10, random_state=0).fit(sim)
try:
    sim.insert(0, 'Cluster Labels', kmeans.labels_)
except:
    print('already has cluster labels')

def show_cluster(cluster_label):
    for i in range(0,len(sim)):
        if sim["Cluster Labels"][i]==cluster_label:
            print("Cluster "+str(cluster_label)+": "+sim.index[i])
            plt.figure()
            plt.axis('off')
            plt.imshow(cv2.cvtColor(cv2.imread(path+sim.index[i].replace('Images','Favs')), cv2.COLOR_BGR2RGB))
            plt.savefig(path2+'CLUSTER'+str(cluster_label)+"_"+sim.index[i].rsplit('\\')[1],dpi=800,bbox_inches='tight')
            #plt.show()
            
for i in np.unique(kmeans.labels_).tolist():
    #print('\n---------------------------------------------\n')
    #print("Images of cluster "+str(i))
    #print('\n---------------------------------------------\n')
    show_cluster(i)
