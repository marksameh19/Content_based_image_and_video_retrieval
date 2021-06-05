from feature_extractors import ColorDistance,HistogramComparison,SiftComparison
import numpy as np
import os
import cv2
import codecs, json 
import sqlite3


db_dir='mm_db.db'
conn= sqlite3.connect(db_dir)
c= conn.cursor()
c.execute('''CREATE TABLE Images (
    name varchar(30),
    directory varchar(200),
    feature json
)''')

conn.commit()


src_dir= 'public/images/'
dest_dir= 'images/'
files = os.listdir(src_dir)

#des_dir= 'features/'

for file in files:
    indx= file.find('.')
    file_name= file[:indx]
    img =cv2.imread(os.path.join(src_dir,file),1)
    
    color= ColorDistance.extract_feature_vector(img)
    hist= HistogramComparison.extract_feature_vector(img)
    sift = SiftComparison.sift_key_des_extracrors(img)

    # create json
    b = {"color_distance": color.tolist(), 'histogram': hist.tolist(),'sift':sift.tolist()}
    #file_path = os.path.join(des_dir,file_name+'.json') ## your path variable
    # json.dump(b, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format

    # save to db
    c.execute('''INSERT INTO Images values (?,?,?)''',[file_name,os.path.join(dest_dir,file),json.dumps(b,separators=(',', ':'), sort_keys=True, indent=4)])
    conn.commit()

conn.close()

    







# img = cv2.imread('images/car.png')

# color= ColorDistance.extract_feature_vector(img)
# hist= HistogramComparison.extract_feature_vector(img)
# sift = SiftComparison.sift_key_des_extracrors(img)

# create json
# b = {"color_distance": color.tolist(), 'histogram': hist.tolist(),'sift':sift.tolist()}
# file_path = "fe.json" ## your path variable
# json.dump(b, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format

# # load json
# json_file= open('fe.json')
# items= json.load(json_file)


# h=np.array(items['histogram']).shape
# print(h==hist.shape)
    







