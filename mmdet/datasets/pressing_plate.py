#!/usr/bin/env python
# encoding: utf-8
'''
@author: wangjianrong
@software: pycharm
@file: pressing_plate.py
@time: 2020/9/22 15:18
@desc:
'''


from .coco import CocoDataset
from .builder import DATASETS


@DATASETS.register_module()
class PressingPlateDataset(CocoDataset):

    CLASSES = ('yp90','yp45','yp0','rp90','rp0','gp0','yp135','r90','w45','y90','y45')