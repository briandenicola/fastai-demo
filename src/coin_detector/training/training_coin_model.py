import os
import argparse
from utils import *
from fastai2.vision.widgets import *

parser = argparse.ArgumentParser(description="Builds a model to detect different types of bears")
parser.add_argument("-k", "--key", help="The API key for Bing Image Search")
args = parser.parse_args()

key = args.key

coin_types = 'marcus+aurelius','aurelian', 'hadrian', 'trajan', 'antonius+pius', 'constantine', 'justinian', 'julius+caesar'
path = Path('coins')

if not path.exists():
    path.mkdir()
    for o in coin_types:
        dest = (path/o)
        dest.mkdir(exist_ok=True)
        results = search_images_bing(key, f'Roman Emperor {o} coins')
        download_images(dest, urls=results.attrgot('content_url'))

coins = DataBlock(
    blocks=(ImageBlock, CategoryBlock), 
    get_items=get_image_files, 
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=Resize(128))

fns = get_image_files(path)

failed = verify_images(fns)
failed.map(Path.unlink)

coins = coins.new(
    item_tfms=RandomResizedCrop(224, min_scale=0.5),
    batch_tfms=aug_transforms())
dls = coins.dataloaders(path)

learn = cnn_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(5)
learn.export('../models/coins.pkl')