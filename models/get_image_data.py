from bing_image_downloader import downloader
import uuid
import os

def get_images_with_query(query, n, output_location):
    # get a bunch of data
    downloader.download(query,
                        limit=n,
                        output_dir=output_location,
                        adult_filter_off=True,
                        force_replace=False,
                        timeout=60,
                        verbose=True)

def rename_with_uuids(directory):
    all_folders = [x[0] for x in os.walk(directory)]
    for folder in all_folders:
        files = os.listdir(folder)
        for f in files:
            f = f.lower()
            if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".gif") or f.endswith(".jpeg"):
                parts = f.split(".")
                oldfile = os.path.join(folder, f)
                guid = str(uuid.uuid4())
                newfile = os.path.join(folder, guid + "." + parts[1])
                os.rename(oldfile,newfile)
                print("Renamed file {} to {}".format(oldfile, newfile))


output_dir = 'C:\\Projects\\data\\is-potato\\raw-potato'
query = "potatoes"
n = 1000

# get_images_with_query(query, n, output_dir)

rename_with_uuids('C:\\Projects\\data\\is-potato')