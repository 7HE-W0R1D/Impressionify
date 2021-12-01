import random
import os, time, shutil, json

def randgen(digit = 10) :
    rand_num = random.random()
    rand_result = int(rand_num * (10 ** (digit + 1)))

    return rand_result

EXPIRE_TIME = 60 * 10
FILE_DICT = "userupload"
def clear_expire_file(filepath = os.path.join("static", FILE_DICT), expiretime = EXPIRE_TIME):
    currtime = int(time.time())
    folder_lst = [x for x in os.scandir(filepath)]
    for folder in folder_lst:
        ctime = os.path.getctime(folder)
        if currtime - ctime > expiretime:
            print("abridge")
            shutil.rmtree(folder)

def validate_path(path):
    return path.replace("\\", "/")

def get_dict(filename = "modules/galleryinfo.txt"):
    '''
    Loads local api key chain file
    '''
    with open(filename, "r", encoding="utf-8") as f:
        # need utf 8 here to prevent corrupted text
        content = f.read()
        key_chain = json.loads(content)

    return key_chain

def get_header_image(this_folder):
    filepath = os.path.join(this_folder, "static", "img", "header-images")
    img_lst = [x for x in os.scandir(filepath)]
    rand_index = random.randint(0, len(img_lst) - 1)
    picked_img = img_lst[rand_index].name
    return picked_img