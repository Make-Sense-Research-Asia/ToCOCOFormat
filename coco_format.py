import numpy as np
from PIL import Image
from pathlib import Path
import json
def init_info(dataset):
    import datetime
    return {
        'year':str(datetime.datetime.now().year),
        'version':'1.0',
        'description':str(dataset),
        'contributor':'',
        'url':'',
        'date_created':f'{datetime.datetime.now().year}-{datetime.datetime.now().month}-{datetime.datetime.now().day}T{datetime.datetime.now().hour}:{datetime.datetime.now().minute}:{datetime.datetime.now().second}'
    }

class Format:
    def __init__(self,dataset) -> None:
        self.data = {
            'info': init_info(dataset),
            #'licenses':init_licenses(),
            'categories':[],
            'images':[],
            'annotations':[]
        }
        self._tmp={}
    
    def post_process(self,output_path):
        with open(output_path,'w')as f:
            json.dump(self.data,f)
    
class ReferItGameFormat(Format):
    def __init__(self,images_dir) -> None:
        super().__init__('ReferItGame')
        self._tmp['f2i']={}
        self._tmp['images_dir']=images_dir

    def add_image(self,img_file):
        if img_file in self._tmp['f2i']:
            return self._tmp['f2i'][img_file]

        image_id = len(self.data['images'])
        img = Image.open(Path(self._tmp['images_dir'],img_file))
        self.data['images'].append(
            {
            "id": image_id,
            "license": 1,
            "file_name": img_file,
            "height": img.height,
            "width": img.width,
            "date_captured": ""
        })
        self._tmp['f2i'][img_file]=image_id
        return image_id

    def add_annotation(self,item):
        img_file, _, bbox, phrase, attri = item
        img_id = self.add_image(img_file)
        # Referit 天然是xyxy的
        bbox = np.array(bbox, dtype=int)
        self.data['annotations'].append({
            "id": len(self.data['annotations']),
            "image_id": img_id,
            "bbox": bbox.tolist(),
            "caption": phrase,
            "attribute": attri
        })
    
