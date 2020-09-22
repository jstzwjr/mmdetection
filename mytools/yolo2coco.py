#!/usr/bin/env python
# encoding: utf-8
'''
@file: yolo2coco.py
@author: wangjianong
@time: 2020/2/21 16:04
@desc:yolo格式转coco
'''

import os
import cv2
import os
import mmcv
import random
import tqdm
from PIL import Image
import re
import datetime


#data format must be:r
#yolo: label_id(start from 0) xc yc w h
#custom: contour
data_format = 'yolo'
filter_empty = False


dataset_name = 'pressing_plate_dataset'
company_name = 'dhzl'
# class_labels = ["bg","head"]
# class_labels = ["bg", 'Crack', 'Blowhole', 'Uneven', 'Break', 'Fray']
# class_labels = ["bg",'helmet','nohelmet']
class_labels = ['bg','yp90','yp45','yp0','rp90','rp0','gp0','yp135','r90','w45','y90','y45']
# class_labels = ['bg','smoke','fire']
# labels_needed = ['bg','smoke','fire']
create_time = datetime.datetime.now().strftime('%Y/%m/%d')

'''
/workspace_wjr/shm/dataset/pressing_plate
'''
train_ratio = 1.0
#图片和标签所在根目录
# root_folder = '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_15/'  #'/workspace/dataset/switch_crop'

folders = [
    '/workspace_wjr/shm/dataset/pressing_plate/',
]


for root_folder in folders:
    train_label_dir = root_folder + 'labels' #"/workspace/dataset/switch_crop/labels"
    train_img_dir = root_folder + 'images'#"/workspace/dataset/switch_crop/images"
    # test_label_dir = "/dataset/wjr_dataset/helmet_data/helmet_dataset/labels" #""/workspace/dataset/switch_crop/labels"
    # test_img_dir = "/dataset/wjr_dataset/helmet_data/helmet_dataset/images" #""/workspace/dataset/switch_crop/images"
    # train_txt = os.path.join('/workspace/dataset/switch_crop','train.txt')
    # test_txt = os.path.join('/workspace/dataset/switch_crop','test.txt')
    #图片所在目录
    root_folder_train = root_folder + 'images'
    root_folder_test = root_folder + 'images'

    # new_list_train_imgs = [p for p in os.listdir(train_img_dir) if p.startswith("11")] #成都环境摄像头
    all_imgs = [p for p in os.listdir(train_img_dir)] # if p.startswith('det') or random.random()>=0.8]
    # all_imgs = [p for p in os.listdir(train_img_dir) if p.startswith('1_') or p.startswith('2_')]
    random.shuffle(all_imgs)
    # list_train_imgs = list_train_imgs[:int(len(list_train_imgs)*0.2)]
    # list_train_imgs += new_list_train_imgs
    # random.shuffle(list_train_imgs)
    len_train = int(len(all_imgs)*train_ratio)
    list_test_imgs = all_imgs[len_train:]
    list_train_imgs = all_imgs[:len_train]
    # list_train_imgs = []
    # list_test_imgs = []
    # for file in all_imgs:
    #     if file.startswith('smoke'):
    #         list_test_imgs.append(file)
    #     else:
    #         list_train_imgs.append(file)

    # list_train_imgs = []
    # with open(train_txt,'r') as f:
    #     for line in f.readlines():
    #         line = os.path.basename(line.strip())
    #         list_train_imgs.append(line)
    print('total train img:{}'.format(len(list_train_imgs)))

    # list_test_imgs = []
    # with open(test_txt,'r') as f:
    #     for line in f.readlines():
    #         line = os.path.basename(line.strip())
    #         list_test_imgs.append(line)
    print('total test img:{}'.format(len(list_test_imgs)))

    # list_train_imgs = os.listdir(train_img_dir)
    # print('total train img:{}'.format(len(list_train_imgs)))
    # list_test_imgs = os.listdir(test_img_dir)
    # print('total test img:{}'.format(len(list_test_imgs)))





    anns = []

    anns_train = {"info": {
            "description": dataset_name,
            "url": "xxxxxx",
            "version": "1.0",
            "year": 2020,
            "contributor": company_name,
            "date_created": create_time},
        "licenses": [
            {
                "url": "xxxxxx",
                "id": 1,
                "name": company_name
            }
        ],
        "images":[],
        "annotations":[],
        "categories":[]
        }

    anns_val = {"info": {
            "description": dataset_name,
            "url": "xxxxxx",
            "version": "1.0",
            "year": 2020,
            "contributor": company_name,
            "date_created": create_time},
        "licenses": [
            {
                "url": "xxxxxx",
                "id": 1,
                "name": company_name
            }
        ],
        "images":[],
        "annotations":[],
        "categories":[]
        }



    for i in range(1,len(class_labels)):
        anns_train['categories'].append(
            {
                "supercategory": class_labels[i],
                "id": i,
                "name": class_labels[i]})
        anns_val['categories'].append(
            {
                "supercategory": class_labels[i],
                "id": i,
                "name": class_labels[i]})



    cur_idx = 0
    train_imgid = {}
    val_imgid = {}
    for filename in tqdm.tqdm(list_train_imgs):
        # img = mmcv.imread(os.path.join(root_folder_train,filename))
        # h,w,_ = img.shape
        img = Image.open(os.path.join(root_folder_train,filename))
        w,h = img.size
        img_info = {
            "license": 1,
            "file_name": filename,
            "coco_url": "xxxxxxxx",
            "height": h,
            "width": w,
            # "height": 1000,
            # "width": 2446,
            "date_captured": create_time,
            "flickr_url": "xxxxxxxx",
            "id":cur_idx
        }
        anns_train['images'].append(img_info)
        train_imgid[filename] = cur_idx
        cur_idx += 1

    cur_idx = 0
    for filename in tqdm.tqdm(list_test_imgs):
        # img = mmcv.imread(os.path.join(root_folder_test,filename))
        # h,w,_ = img.shape
        img = Image.open(os.path.join(root_folder_test,filename))
        w,h = img.size
        img_info = {
            "license": 1,
            "file_name": filename,
            "coco_url": "xxxxxxxx",
            "height": h,
            "width": w,
            # "height": 1000,
            # "width": 2446,
            "date_captured": create_time,
            "flickr_url": "xxxxxxxx",
            "id":cur_idx
        }
        anns_val['images'].append(img_info)
        val_imgid[filename] = cur_idx
        cur_idx += 1

    print(len(train_imgid),len(val_imgid),len(list_train_imgs),len(list_test_imgs))

    cur_idx_train = 0
    cur_idx_val = 0

    with open(os.path.join(root_folder,'train.txt'),'w') as f_train,open(os.path.join(root_folder,'test.txt'),'w') as f_test:
        for filename in tqdm.tqdm(list_train_imgs+list_test_imgs):
            if filename in list_train_imgs:
                img_path = os.path.join(root_folder_train,filename)
                txt_path = os.path.join(root_folder_train,filename).replace('JPG','txt').replace("jpg","txt").replace("png","txt").replace("images","labels")
                f_train.write(filename+'\n')
            else:
                img_path = os.path.join(root_folder_test,filename)
                txt_path = os.path.join(root_folder_test, filename).replace('JPG','txt').replace("jpg", "txt").replace("png","txt").replace("images", "labels")
                f_test.write(filename+'\n')
            # img = cv2.imread(img_path)
            # height,width,_ = img.shape
            img = Image.open(img_path)
            width,height = img.size
            area_img = width*height
            if not os.path.exists(txt_path):
                continue
            with open(txt_path,"r") as f:
                not_empty = False
                for line in f.readlines():
                    not_empty = True
                    ann = {}

                    # line = line.strip().split(',')
                    line = re.split(r',| ',line.strip())
                    line = [float(v) for v in line]
                    # 烟雾分割数据
                    if data_format=='yolo':
                        xmin = (line[1]-line[3]/2)*width
                        ymin = (line[2]-line[4]/2)*height
                        xmax = (line[1]+line[3]/2)*width
                        ymax = (line[2] + line[4] / 2) * height
                        seg_info = [[xmin,ymin,xmax,ymin,xmax,ymax,xmin,ymax]]
                    elif data_format=='custom':
                        cor_x = []
                        cor_y = []
                        for j in range(len(line)):
                            if j%2 == 0:
                                cor_x.append(line[j])
                            else:
                                cor_y.append(line[j])
                        xmin = min(cor_x)
                        xmax = max(cor_x)
                        ymin = min(cor_y)
                        ymax = max(cor_y)
                        seg_info = [line]

                    # ann["category_id"] = class_labels[int(line[0])]
                    ann["category_id"] = int(line[0]) + 1
                    # ann["category_id"] = 1
                    w=xmax-xmin
                    h=ymax-ymin
                    # #如果目标面积过小则删除，判断方法：面积占原图比例小于1%
                    area =w*h
                    # if area / area_img <= 0.0005:
                    #     continue
                    ann["segmentation"] = seg_info
                    ann["area"] = area
                    ann["bbox"] = [xmin,ymin,w,h]
                    ann["iscrowd"] = 0
                    assert not (filename in train_imgid.keys() and filename in val_imgid.keys())
                    if filename in train_imgid.keys():
                        ann["image_id"] = train_imgid[filename]
                        ann["id"] = cur_idx_train
                        anns_train["annotations"].append(ann)
                        cur_idx_train += 1
                    elif filename in val_imgid.keys():
                        ann["image_id"] = val_imgid[filename]
                        ann["id"] = cur_idx_val
                        anns_val["annotations"].append(ann)
                        cur_idx_val += 1
                    else:
                        print("filename id {} not exist!".format(filename))
                        continue


    # json.dump(anns_obj,open('/data/AIGroup/wangjianrong/dataset/textile_defect/train/annotations/all_data.json','w'),indent=4)
    # mmcv.dump(anns_obj,outdir,indent=4)
    mmcv.dump(anns_train,os.path.join(root_folder,"train.json"),indent=4)
    mmcv.dump(anns_val,os.path.join(root_folder,"test.json"),indent=4)





