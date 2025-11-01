import sys

import unittest

import cv2
import numpy as np

from src import hybrid

class TestCrossCorrelation2D(unittest.TestCase):
    def setUp(self):
        self.small_height = 5
        self.small_width = 4
        self.big_height = 25
        self.big_width = 20
        self.big_img_grey = np.random.rand(self.big_height,self.big_width)
        self.small_img_grey = np.random.rand(self.small_height,self.small_width)
        self.img_rgb = np.random.rand(self.big_height,self.big_width,3)

    def test_mean_filter_rect_grey(self):
        '''
        Tests cross-correlation of greyscale image using a rectangular mean filter
        '''
        mean = np.ones((3,5))
        student = hybrid.cross_correlation_2d(self.small_img_grey, mean)
        solution = cv2.filter2D(self.small_img_grey, -1, mean, borderType=cv2.BORDER_CONSTANT)

        self.assertTrue(np.allclose(student, solution, atol=1e-08), \
            msg="Incorrect cross-correlation of greyscale image using rectangular mean filter")

    def test_rand_rect_filter_RGB(self):
        '''
        Tests cross-correlation of RGB image using a random rectangular filter
        '''
        rand_filt = np.random.rand(5,7)
        student = hybrid.cross_correlation_2d(self.img_rgb, rand_filt)
        solution = cv2.filter2D(self.img_rgb, -1, rand_filt, borderType=cv2.BORDER_CONSTANT)

        self.assertTrue(np.allclose(student, solution, atol=1e-08), \
            msg="Incorrect cross-correlation of RGB image using random rectangular filter")


class TestConvolve2D(unittest.TestCase):
    def setUp(self):
        self.small_height = 5
        self.small_width = 4
        self.big_height = 25
        self.big_width = 20
        self.big_img_grey = np.random.rand(self.big_height,self.big_width)
        self.small_img_grey = np.random.rand(self.small_height,self.small_width)
        self.img_rgb = np.random.rand(self.big_height,self.big_width,3)
    
    def test_mean_filter_rect_grey(self):
        '''
        Tests convolution of greyscale image using a rectangular mean filter
        '''
        mean = np.ones((3,5))
        mean_trans = np.fliplr(np.flipud(mean))
        student = hybrid.convolve_2d(self.small_img_grey, mean)
        solution = cv2.filter2D(self.small_img_grey, -1, mean_trans, borderType=cv2.BORDER_CONSTANT)
    
        self.assertTrue(np.allclose(student, solution, atol=1e-08), \
            msg="Incorrect result convolving greyscale image using rectangular mean filter")

    def test_rand_rect_filter_RGB(self):
        '''
        Tests convolution of RGB image using a random rectangular filter
        '''
        rand_filt = np.random.rand(5,7)
        rand_filt_trans = np.fliplr(np.flipud(rand_filt))
        student = hybrid.convolve_2d(self.img_rgb, rand_filt)
        solution = cv2.filter2D(self.img_rgb, -1, rand_filt_trans, borderType=cv2.BORDER_CONSTANT)
    
        self.assertTrue(np.allclose(student, solution, atol=1e-08), \
            msg="Incorrect result convolving RGB image using random rectangular filter")



    
if __name__ == '__main__':
    np.random.seed(4670)
    unittest.main()
