import numpy as np
import cv2
from scipy.stats import skew
import pickle
import os


class ColorDistance():
    
    def _divide_to_grids(self,image):
        '''
        input:
            image
        
        output:
            list of 25 grids of the image
        '''
        

        #resize to 600x600 image to unify the size
        image= cv2.resize(image,(600,600))
        GRID_SIZE=600//5

        #convert the image to hsv
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        out=[]

        for i in range(0,600,GRID_SIZE):
            for j in range(0,600,GRID_SIZE):
                grid = image_hsv[i:i+GRID_SIZE, j:j+GRID_SIZE, :]
                out.append(grid)
        
        return np.array(out)


    def _get_grid_info(self,grid):
        '''
        input:
            grid
        output:
            return a list contains 9 numbers (mean , std, skewness) for each color channel of the grid
        '''
        out=[]
        for i in range(grid.shape[-1]):
            channel = grid[:,:,i]
            mue = np.mean(channel)
            std= np.std(channel)
            skewness= skew(channel.ravel())
            out.append(mue)
            out.append(std)
            out.append(skewness)
        
        return out
    
    @staticmethod
    def extract_feature_vector(image):
        '''
        input:
            image
        output:
            an array of shape 225x1 contains the image features
        '''
        grids = ColorDistance._divide_to_grids(ColorDistance,image)
        vec= []
        for grid in grids:
            info = ColorDistance._get_grid_info(ColorDistance,grid)
            vec = np.append(vec,info)
        return np.array(vec)

    @staticmethod
    def calc_distance(vec1,vec2):
        '''
        input:
            vec1
            vec2
        output:
            return the L2 distance between the two feature vectors
        '''
        dis = np.linalg.norm(vec1-vec2)

        return dis




class HistogramComparison():
    @staticmethod
    def extract_feature_vector(image):
        image = cv2.resize(image,(600,600))  

        #convert images to HSV
        img1_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)



        #calculate Hist of 2 images and normalize them
        hist_img1 = cv2.calcHist([img1_hsv], [0,1], None, [180,256], [0,180,0,256])
        cv2.normalize(hist_img1, hist_img1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

    
        return hist_img1

    @staticmethod
    def compare_hist(hist_img1,hist_img2):
        # cv2.normalize(hist_img1, hist_img1, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        # cv2.normalize(hist_img2, hist_img2, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        # find the metric value using correlation
        # metric_val1 = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_CORREL)
        hist_img1 = np.array(hist_img1, dtype=np.float32)
        hist_img2 = np.array(hist_img2, dtype=np.float32)
        metric_val2 = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_BHATTACHARYYA)        
        # metric_val3 = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_CHISQR)
        # metric_val4 = cv2.compareHist(hist_img1, hist_img2, cv2.HISTCMP_INTERSECT)
        # if metric_val2 <= 0.5 : return True
        return metric_val2



class SiftComparison():
    @staticmethod
    def sift_key_des_extracrors(img):
        img = cv2.resize(img,(600,600))  
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        sift = cv2.SIFT_create()
        _, des = sift.detectAndCompute(gray,None)
        return des

    @staticmethod
    def sift_compare(des_inp,des_dp):
        des_inp = np.array(des_inp ,dtype= np.float32)
        des_dp = np.array(des_dp ,dtype= np.float32)

        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des_inp, des_dp, k=2)
        # Apply ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good.append([m])

        return len(matches)/len(good)