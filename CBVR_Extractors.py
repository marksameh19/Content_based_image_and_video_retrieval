import numpy as np
import cv2

class CBVR():
    @staticmethod
    def CBVR_Sequintial_Method(Video_Path):
        # Capture video from file
        cap = cv2.VideoCapture(Video_Path)
        # Create ref frame
        ret, ref_frame = cap.read()
        ref_frame = cv2.resize(ref_frame, (600, 600))
        # Convert ref frame to hsv
        hsv_ref = cv2.cvtColor(ref_frame, cv2.COLOR_BGR2HSV)
        # Histogram of ref frame
        histogram_ref = cv2.calcHist([hsv_ref], [0,1], None, [180,256], [0,180,0,256])
        cv2.normalize(histogram_ref, histogram_ref, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

        Key_Frames_Histograms = []
        key_Frames=[]
        count = 0

        Key_Frames_Histograms.append(histogram_ref)
        key_Frames.append(ref_frame)
        #cv2.imwrite("frame%d.jpg" % count, ref_frame)

        while True:
            ret, frame = cap.read()
            if ret == True:
                # resize frame
                frame = cv2.resize(frame, (600, 600))
                # Convert next frame to hsv
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                # Create histogram
                histogram = cv2.calcHist([hsv], [0, 1], None, [180, 256], [0, 180, 0, 256])
                cv2.normalize(histogram, histogram, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
                # Calculate Key frames through histogram difference
                difference = cv2.compareHist(histogram, histogram_ref, cv2.HISTCMP_BHATTACHARYYA)
                if difference > 0.4:
                    # make the frame histogram be the  reference
                    histogram_ref = histogram
                    Key_Frames_Histograms.append(histogram)
                    key_Frames.append(frame)
                    # cv2.imwrite("frame%d.jpg" % count, frame)
                    count += 1

            else:
                break

        cap.release()
        cv2.destroyAllWindows()
        return np.array(Key_Frames_Histograms,dtype=np.float32),np.array(key_Frames,dtype=np.float32)
    @staticmethod
    def NAIV_VideoSamalirity(Test_Hist,DB_Hist):
        match=0
        for i in range(len(Test_Hist)):
            for j in range(len(DB_Hist)):
                difference=cv2.compareHist(Test_Hist[i], DB_Hist[j], cv2.HISTCMP_BHATTACHARYYA)
                if difference <0.35:
                    match+=1
        return match/Test_Hist.shape[0]

# Db_hist,_=CBVR.CBVR_Sequintial_Method('public/videos/30_Second_Animation.mp4')
# Test_hist,_=CBVR.CBVR_Sequintial_Method('public/videos/Rainy_Day_[short_30_sec_animation].mp4')
# print(CBVR.NAIV_VideoSamalirity(Test_hist,Db_hist))