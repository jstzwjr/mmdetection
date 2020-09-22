_base_ = '../retinanet/retinanet_r50_fpn_1x_coco.py'

model = dict(
    bbox_head=dict(
        _delete_=True,
        type='FreeAnchorRetinaHead',
        num_classes=11, #not including bg,e.g.,80 for coco
        in_channels=256,
        stacked_convs=4,
        feat_channels=256,
        anchor_generator=dict(
            type='AnchorGenerator',
            octave_base_scale=4,
            scales_per_octave=3,
            ratios=[0.5, 1.0, 2.0],
            strides=[8, 16, 32, 64, 128]),
        bbox_coder=dict(
            type='DeltaXYWHBBoxCoder',
            target_means=[.0, .0, .0, .0],
            target_stds=[0.1, 0.1, 0.2, 0.2]),
        loss_bbox=dict(type='SmoothL1Loss', beta=0.11, loss_weight=0.75)))
optimizer_config = dict(
    _delete_=True, grad_clip=dict(max_norm=35, norm_type=2))

# npgus = 2
# multiplier = 2

img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='Resize', img_scale=[(1333, 640), (1333, 800)],multiscale_mode='value', keep_ratio=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='Normalize', **img_norm_cfg),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels']),
]

# optimizer = dict(lr=0.02*multiplier*npgus)
dataset_type = 'PressingPlateDataset'
data_root = '/workspace_wjr/shm/dataset/pressing_plate/'
data = dict(
    samples_per_gpu=12,
    workers_per_gpu=12,
    train=dict(
        type=dataset_type,
        ann_file=data_root + 'train.json',
        img_prefix=data_root + 'images/'),
    val=dict(
        type=dataset_type,
        ann_file=data_root + 'train.json',
        img_prefix=data_root + 'images/'),
    )
evaluation = dict(interval=1, metric='bbox')
optimizer = dict(lr=0.01*6)





