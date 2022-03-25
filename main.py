import torch
from coco_format import ReferItGameFormat
from tqdm import tqdm
if __name__=='__main__':
    from icecream import ic
    pth_path='data/referit/referit_test.pth'
    data = torch.load(pth_path)
    
    form = ReferItGameFormat(images_dir='ln_data/referit/images')
    for item in tqdm(data):
        #ic(item)
        form.add_annotation(item)
    form.post_process('referit_test.json')