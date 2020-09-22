#!/usr/bin/env python
# encoding: utf-8
'''
@file: merge_jsons.py
@author: wangjianong
@time: 2020/3/30 18:00
@desc:将多个coco格式的json文件合并为一个json文件
'''
import json
import os

def match2license(license1,license2):
    '''
    比较两个license，相同则返回True，否则返回False
    :param license1:
    :param license2:
    :return:
    '''
    for key in license1.keys():
        if license1[key] != license2[key]:
            return False
    return True

def match_licenses_and_license(licenses,license):
    '''
    判断licenses中是否存在相同的license，存在则返回True，否则返回False
    :param licenses:
    :param license:
    :return:
    '''
    for license_ in licenses:
        if match2license(license_,license):
            return True
    return False

def merge2licenses(licenses1,licenses2):
    '''
    合并两个licenses
    :param licenses1:
    :param licenses2:
    :return:
    '''
    licenses = licenses1
    for license2 in licenses2:
        if not match_licenses_and_license(licenses1,license2):
            licenses.append(license2)
    return licenses

def merge_images_anns(json1,json2):
    images1 = json1["images"]
    images2 = json2["images"]

    anns1 = json1['annotations']
    anns2 = json2['annotations']
    anns = anns1.copy()
    images = images1.copy()

    img_ids1 = [image['id'] for image in images1]
    img_ids2 = [image['id'] for image in images2]
    max_imageid1 = max(img_ids1)
    min_imageid2 = min(img_ids2)
    if min_imageid2 == 0:
        interval_imageid = max_imageid1 + 1
    else:
        interval_imageid = max_imageid1

    for image in images2:
        image["id"] = image["id"] + interval_imageid
        images.append(image)

    ann_ids1 = [ann['id'] for ann in anns1]
    ann_ids2 = [ann['id'] for ann in anns2]
    max_annid1 = max(ann_ids1)
    if len(ann_ids2) == 0:
        return images, anns
    min_annid2 = min(ann_ids2)
    if min_annid2 == 0:
        interval_annid= max_annid1 + 1
    else:
        interval_annid = max_annid1
    for ann in anns2:
        ann["image_id"] = ann["image_id"] + interval_imageid
        ann["id"] = ann["id"] + interval_annid
        anns.append(ann)
    return images,anns




def merge2jsons(json1,json2):
    #合并licenses
    # licenses1 = json1["licenses"]
    # licenses2 = json2["licenses"]
    # licenses = merge2licenses(licenses1,licenses2)
    # json1["licenses"] = licenses

    #合并images、annotations
    images,anns = merge_images_anns(json1,json2)
    json_merged = json1
    json_merged['images'] = images
    json_merged['annotations'] = anns
    return json_merged



if __name__ == '__main__':
    #smoke:
    json_files = [
        '/workspace_wjr/shm/dataset/new_smoke_data/initial_processed/train.json',
        '/workspace_wjr/shm/dataset/new_smoke_data/smoke_0409/task_7/train.json',
        '/workspace_wjr/shm/dataset/new_smoke_data/smoke_0610/train.json',
        '/workspace_wjr/shm/dataset/new_smoke_data/smoke_0618/train.json',
        '/workspace_wjr/shm/dataset/new_smoke_data/valid_data/train.json',
        '/workspace_wjr/shm/dataset/new_smoke_data/sync_errors/train.json',
        '/workspace_wjr/shm/dataset/new_smoke_data/smoke_0721_filtered/train.json',
        # '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_1/train.json',
        # '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_2/train.json',
        # '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_3/train.json',
        # '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_4/train.json',
        # '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_5/train.json',
        # '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_6/train.json',
        # '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_7/train.json',
        # '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_9/train.json',
        # '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_10/train.json',
        # '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_12/train.json',
        # '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_13/train.json',
        # '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_15/train.json'
    ]
    image_folders = [
        'new_smoke_data/initial_processed/images',
        'new_smoke_data/smoke_0409/task_7/images',
        'new_smoke_data/smoke_0610/images',
        'new_smoke_data/smoke_0618/images',
        'new_smoke_data/valid_data/images',
        'new_smoke_data/sync_errors/images',
        'new_smoke_data/smoke_0721_filtered/images',
        # 'fire_smoke_data/fire_data_1/images',
        # 'fire_smoke_data/fire_data_2/images',
        # 'fire_smoke_data/fire_data_3/images',
        # 'fire_smoke_data/fire_data_4/images',
        # 'fire_smoke_data/fire_data_5/images',
        # 'fire_smoke_data/fire_data_6/images',
        # 'fire_smoke_data/fire_data_7/images',
        # 'fire_smoke_data/fire_data_9/images',
        # 'fire_smoke_data/fire_data_10/images',
        # 'fire_smoke_data/fire_data_12/images',
        # 'fire_smoke_data/fire_data_13/images',
        # 'fire_smoke_data/fire_data_15/images',
    ]
    #fire and smoke
    # json_files = [
    #     '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_1/train.json',
    #     '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_2/train.json',
    #     '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_3/train.json',
    #     '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_4/train.json',
    #     '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_5/train.json',
    #     '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_6/train.json',
    #     '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_7/train.json',
    #     '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_9/train.json',
    #     '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_10/train.json',
    #     '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_12/train.json',
    #     '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_13/train.json',
    #     '/workspace_wjr/shm/dataset/fire_smoke_data/fire_data_15/train.json'
    # ]
    # image_folders = [
    #     'fire_smoke_data/fire_data_1/images',
    #     'fire_smoke_data/fire_data_2/images',
    #     'fire_smoke_data/fire_data_3/images',
    #     'fire_smoke_data/fire_data_4/images',
    #     'fire_smoke_data/fire_data_5/images',
    #     'fire_smoke_data/fire_data_6/images',
    #     'fire_smoke_data/fire_data_7/images',
    #     'fire_smoke_data/fire_data_9/images',
    #     'fire_smoke_data/fire_data_10/images',
    #     'fire_smoke_data/fire_data_12/images',
    #     'fire_smoke_data/fire_data_13/images',
    #     'fire_smoke_data/fire_data_15/images',
    # ]
    save_path = '/workspace_wjr/shm/dataset/train.json'
    # json_files = [
    #     '/workspace_wjr/shm/dataset/smoke_data/det/initial_data/train_filtered.json',
    #               '/workspace_wjr/shm/dataset/smoke_data/smoke_0408/train_filtered.json', \
    #               '/workspace_wjr/shm/dataset/smoke_data/smoke_0409/task_7/train_filtered.json',
    #                '/workspace_wjr/shm/dataset/smoke_data/synthetic_0426/train_filtered.json',
    #                 '/workspace_wjr/shm/dataset/smoke_data/valid_data/train_filtered.json',
    #     '/workspace_wjr/shm/dataset/smoke_data/yongxiang/train_filtered.json',
    #     '/workspace_wjr/shm/dataset/smoke_data/errors/train_filtered.json'
    # ]
    # image_folders = [
    #     'det/initial_data/images/',
    #                  'smoke_0408/images/',
    #                  'smoke_0409/task_7/images',
    #                  'synthetic_0426/images',
    #                 'valid_data/images',
    #     'yongxiang/images',
    #     'errors/images'
    #                  ]
    # json_files = [
    #     '/shm/dataset/smoking_0609/train_filtered.json',
    #     '/shm/dataset/smoking/smoking/train_filtered.json',
    # ]
    # image_folders = [
    #     'smoking_0609/images',
    #     'smoking/smoking/images'
    # ]
    # save_path = '/workspace_wjr/shm/dataset/smoke_data/train_filtered.json'
    json_merged = None
    for i,json_file in enumerate(json_files):
        json_data = json.load(open(json_file, 'r'))
        for image in json_data['images']:
            image['file_name'] = os.path.join(image_folders[i], image['file_name'])
        print(json_file,f'images:{len(json_data["images"])},anns:{len(json_data["annotations"])}')
        if i == 0:
            json_merged = json_data
        else:
            json_merged = merge2jsons(json_merged,json_data)
    print("total image cnt:{},total ann cnt:{}".format(len(json_merged["images"]),len(json_merged["annotations"])))
    json.dump(json_merged,open(save_path,'w'),indent=4)
    print()

