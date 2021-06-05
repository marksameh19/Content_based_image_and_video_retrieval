import sys
import json
import sqlite3
from feature_extractors import ColorDistance,HistogramComparison,SiftComparison
import cv2
import numpy as np

extractors= {'2': ColorDistance.extract_feature_vector,
             '3': HistogramComparison.extract_feature_vector,
             "1": SiftComparison.sift_key_des_extracrors }

comparators= {'2': ColorDistance.calc_distance,
             '3': HistogramComparison.compare_hist,
             '1': SiftComparison.sift_compare }
feature_name= {'2': 'color_distance',
               '3': 'histogram',
               '1': 'sift'}

k = int(sys.argv[2])
q_image_path= 'uploads/image.jpg'

# read the image
q_img= cv2.imread(q_image_path,1)

# get query image features
q_feature = extractors[sys.argv[1]](q_img)
#print(type(q_feature))


db_dir='mm_db.db'
conn= sqlite3.connect(db_dir)
c= conn.cursor()

c.execute('''SELECT * FROM Images''')

rows= c.fetchall()

d= list()

for row in rows:
    dirr = row[1]
    feature= np.array(json.loads(row[2])[feature_name[sys.argv[1]]])
    distance = comparators[sys.argv[1]](q_feature,feature)
    d.append((dirr,distance))
conn.close()
# print("1",d)
d.sort(key= lambda x: x[1])
d = d[:k]
# print("2",d)
output_dirs = [e[0] for e in d]
print(output_dirs)




    