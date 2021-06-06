import numpy as np
import cv2
from CBVR_Extractors import CBVR
import sys
import json
import sqlite3

k = int(sys.argv[1])

q_video_path= 'uploads/video.mp4'

q_hist,_ = CBVR.CBVR_Sequintial_Method(q_video_path)

db_dir='cbvr_db.db'
conn= sqlite3.connect(db_dir)
c= conn.cursor()

c.execute('''SELECT * FROM Videos''')

rows= c.fetchall()

d= list()

for row in rows:
    dirr = row[1]
    feature= np.array(json.loads(row[2])['histogram'],dtype=np.float32)
    distance = CBVR.NAIV_VideoSamalirity(q_hist,feature)
    d.append((dirr,distance))
conn.close()
# print("1",d)
d.sort(key= lambda x: x[1],reverse=True)
d = d[:k]
# print("2",d)
output_dirs = [e[0] for e in d]
print(output_dirs)