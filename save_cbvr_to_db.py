import numpy as np
from CBVR_Extractors import CBVR
import cv2
import json 
import sqlite3
import os

db_dir='cbvr_db.db'
conn= sqlite3.connect(db_dir)
c= conn.cursor()
c.execute('''CREATE TABLE Videos (
    name varchar(30),
    directory varchar(200),
    feature json
)''')

conn.commit()

src_dir= 'public/videos/'
dest_dir= 'videos/'
files = os.listdir(src_dir)

for file in files:
    indx= file.find('.')
    file_name= file[:indx]
    vid = os.path.join(src_dir,file)
    
    Db_hist,_= CBVR.CBVR_Sequintial_Method(vid)
    # create json
    b = {'histogram': Db_hist.tolist()}
    #file_path = os.path.join(des_dir,file_name+'.json') ## your path variable
    # json.dump(b, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), sort_keys=True, indent=4) ### this saves the array in .json format

    # save to db
    c.execute('''INSERT INTO Videos values (?,?,?)''',[file_name,os.path.join(dest_dir,file),json.dumps(b,separators=(',', ':'), sort_keys=True, indent=4)])
    conn.commit()

conn.close()