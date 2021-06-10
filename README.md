# Content-Based Multimedia Retrieval System

## CBIR

### CBIR System Architecture
<img src="https://github.com/marksameh19/Content_based_image_and_video_retrieval/blob/master/samples/cbir_arch.PNG" width = "500">

### Feature Extraction
All classes can be found in the [feature_extractor.py](https://github.com/marksameh19/Content_based_image_and_video_retrieval/blob/master/feature_extractors.py) file
- Color Distance
- Color Histogram
- SIFT

### Database & Dataset
For our system we used the **Flicker8k** dataset which contains aprroximately 8k images, and for each image we saved a json file contains the features extracted using every feature extractor mentioned above.

We used a SQL database that contains _One_ tabel, the table contains _three attributes_ (image_name, image_dir and image_json)

The **image_json** attribute is where we saved the json file of the image.

The code of saving the dataset into the database is in [save_to_db.py](https://github.com/marksameh19/Content_based_image_and_video_retrieval/blob/master/save_to_db.py) file.

### Main Code
In [main_cbir.py](https://github.com/marksameh19/Content_based_image_and_video_retrieval/blob/master/main_cbir.py) we connect the [app.js](https://github.com/marksameh19/Content_based_image_and_video_retrieval/blob/master/app.js) file to our python code to run our server.

### Demo Videos

Color Distance

![Color Distance](https://github.com/marksameh19/Content_based_image_and_video_retrieval/blob/master/samples/cbir_dist.gif)

Color Histogram

![Color Histogram](https://github.com/marksameh19/Content_based_image_and_video_retrieval/blob/master/samples/cbir_hist.gif)

SIFT

![SIFT](https://github.com/marksameh19/Content_based_image_and_video_retrieval/blob/master/samples/cbir_sift.gif)


_______________________________________________________________________________________________________________________________________________________________________

## CBVR

### CBVR System Architecture
<img src="https://github.com/marksameh19/Content_based_image_and_video_retrieval/blob/master/samples/cbvr_arch.PNG" width = "500">

### Feature Extraction
We first extract the key frames from the video using color histogram comparison between frames and then save the histograms of the key frames,
the key frame extractor is in [CBVR_Extractors.py](https://github.com/marksameh19/Content_based_image_and_video_retrieval/blob/master/CBVR_Extractors.py)

also we compare the videos by applying the NVS(Naive Video Similarity) for all key frames extracted from the reference video and the query video 
### Database & Dataset
For our system we used the **Random short animation videos from youtube** for dataset , and for each video we extract the keyframes and we saved a json file contains the features extracted for every frame in the video.

We used a SQL database that contains _One_ table, the table contains _three attributes_ (video_name, video_dir and video_json)

The **video_json** attribute is where we saved the json file of the video frames.

The code of saving the dataset into the database is in [save_cbvr_to_db.py](https://github.com/marksameh19/Content_based_image_and_video_retrieval/blob/master/save_cbvr_to_db.py) file.

### Main Code
In [main_cbvr.py](https://github.com/marksameh19/Content_based_image_and_video_retrieval/blob/master/main_cbvr.py) we connect the [app.js](https://github.com/marksameh19/Content_based_image_and_video_retrieval/blob/master/app.js) file to our python code to run our server.

### Demo Videos

Naive Video Similarity

![NVS](https://github.com/marksameh19/Content_based_image_and_video_retrieval/blob/master/samples/cbvr.gif)


