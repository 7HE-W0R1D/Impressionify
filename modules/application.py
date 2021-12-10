##############
# Your turn! #
##############
# Now you're ready for the next part, where you retrieve data from an API
# of your choice. Note that you may need to provide an authentication key
# for some APIs. For that, work another file, called hw5-application.py.
#
# You will need to copy a few of the import statements from the top of this
# file. You may copy any helpful functions, too, like pretty() or
# safe_get().
#
# See requirements in the README.
#
# Also note that when the sunrise sunset API we used is queried for a
# date that doesn't exist, it gives a 400 error. Some APIs that you may
# use will return JSON-formatted data saying that the requested item
# couldn't be found. You may have to check the contents of the data you 
# get back to see whether a query was successful. You don't have to do
# that with the sunrise sunset API.
import urllib.parse, urllib.request, urllib.error, json
import random
from urllib import request, parse
import requests

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def strip_word_punctuation(word):
    # Note - this function is far from comprehensive, and so some punctuation may 
    # still make it through
    word = word.replace("&lt;","<").replace("&gt;",">").replace("&amp;","&")
    return word.strip("&=.,()<>\"\\'~?!;*:[]-+_/`\u2014\u2018\u2019\u201c\u201d\u200b").replace("\"","\"\"")

def safe_get(url, input_load = None, header = None):
    '''
    Getting an url with optional loads and headers as dictionaries and returns the response,
    catches any error raised while fetching the url.
    '''

    try:
        if header is not None:
            if input_load is not None:
                print("Encoding loads...")
                data = parse.urlencode(input_load).encode()
                print("Encoding headers...")
                req =  request.Request(url, data=data, headers=header)
            else:
                #load is none
                print("Encoding headers...")
                req =  request.Request(url, headers=header)
            print("Getting from: " + url)
            response = request.urlopen(req)
        else:
            load_url = ""
            if input_load is not None:
                print("Encoding loads...")
                load_url = urllib.parse.urlencode(input_load)

            print("Getting from: " + url + load_url)
            response = urllib.request.urlopen(url + load_url)

    except urllib.error.URLError as e:
        code = "No Error Code Available"
        reason = "No Reason Available"
        if hasattr(e, "code"):
            code = e.code

        if hasattr(e, "reason"):
            reason = e.reason
        print("Error Code: " + str(code) + "\nError Reason: " + reason)

    else:
        print("No errors.")
        return(response)

def safe_get_json(input_url, load = None, header = None):
    res = safe_get(input_url, load, header)
    res_str = res.read().decode('utf-8')
    res_json = json.loads(res_str)
    return res_json

def rand_group(group_list):
    '''
    Given a list representing number of objects in each group, randomly pick one object and
    return its group index

    Args:
        group_list -- the list representing number of objects

    Return:
        The index of the group in the list
    '''
    total = sum(group_list)
    cmp_lst = [(group_list[0] / total)]
    for i in range(1, len(group_list)):
        cmp_lst.append(cmp_lst[i - 1] + (group_list[i] / total))

    rand = random.random()
    for j in range(len(cmp_lst)):
        if rand < cmp_lst[j]:
            return j
    
    return -1

def get_key(key_name):
    '''
    Loads local api key chain file
    '''
    with open("modules/keys.txt", "r") as f:
        content = f.read()
        key_chain = json.loads(content)

    return key_chain[key_name]

class photo():
    def __init__(self, info):
        self.url = info["url"]
        self.title = strip_word_punctuation(info["title"])
        self.artist = info["artist"]
        self.artist_id = None
        self.style = None
        self.year = None
        self.alt_text = None
        if info.get("style", False):
            self.style = info["style"]

        if info.get("year", False):
            self.year = info["year"]

        if info.get("alt_text", False):
            self.alt_text = info["alt_text"]

        if info.get("artist_id", False):
            self.artist_id = info["artist_id"]

    def __str__(self):
        title_str = self.title
        if len(title_str) > 30:
            title_str = title_str[0: 27] + "..."

        
        year_str = ""
        if self.year is not None:
            year_str = ", finished in " + str(self.year)

        style_str = ""
        if self.style is not None:
            style_str = " Styles in " + str(self.style) + "."

        result_str = "{title}, by {artist_title}{year_str}.{style_str}".format(title = self.title,\
                artist_title = self.artist, year_str = year_str, style_str = style_str)
        
        return result_str

    def get_alt_text(self):
        return self.alt_text

    def get_url(self):
        return self.url

class AICPhoto(photo):
    def __init__(self, info):
        art_dict = {}
        input_art = info
        input_art_data = input_art["data"]
        art_dict["title"] = input_art_data["title"]
        art_dict["alt_text"] = input_art_data["thumbnail"]["alt_text"]
        art_dict["year"] = input_art_data["date_end"]
        art_dict["artist"] = input_art_data["artist_title"]
        art_dict["artist_id"] = input_art_data["artist_id"]
        art_dict["style"] = input_art_data["style_title"]
        art_dict["url"] = self.get_art_image_url(input_art)
        super().__init__(art_dict)
        self.info_link = self.get_info_url(input_art)

        if input_art_data.get("artist_display", False):
            self.artist_display = input_art_data["artist_display"]

        self.artist_display = self.artist 

    def get_art_image_url(self, input_art, appendix = "/full/843,/0/default.jpg"):
        '''
        Returns the image url of an artwork
        '''
        image_id = input_art["data"]["image_id"]
        iiif_url = input_art["config"]["iiif_url"]
        image_url = iiif_url + "/" + image_id + appendix

        return image_url
    
    def get_info_url(self, input_art):
        '''
        Returns the direct link to the info page of the artwork
        '''
        art_id = input_art["data"]["id"]
        website_url = input_art["config"]["website_url"]
        return website_url + "/artworks/" + str(art_id)
    
    def export(self):
        result = {
            "title": self.title,
            "year": self.artist,
            "alt_text": self.alt_text,
            "info_link": self.info_link,
            "url": self.url,
            "btn_str": "To Artwork Site"
        }

        return result


class UnsplashPhoto(photo):
    def __init__(self, info):
        info["title"] = "No Title"
        if info.get("description", False):
            info["title"] = info["description"]

        elif info.get("alt_description", False):
            info["title"] = info["alt_description"]

        name = ""
        if info["user"].get("first_name") is not None:
            fname = info["user"].get("first_name")
            name += fname

        middle_init = "\"User\""
        if info["user"].get("username") is not None:
            middle_init = ' "' + info["user"]["username"] + '"'
        name += middle_init

        if info["user"].get("last_name") is not None:
            lname = " " + info["user"].get("last_name")
            name += lname

        info["artist"] = name
        info["year"] = info["created_at"]
        info["url"] = info["urls"]["raw"]

        super().__init__(info)
        if info["user"].get("profile_image", False):
            self.avatar = info["user"]["profile_image"]["medium"]
        self.color = info.get("color", None)
        self.info_link = self.get_info_link(info)

    def __str__(self):
        title_str = self.title
        if len(title_str) > 30:
            title_str = title_str[0: 27] + "..."
        
        year_str = ""
        if self.year is not None:
            year_str = ", taken in " + str(self.year)

        result_str = "{title}, by {artist_title}{year_str}.".format(title = self.title,\
                artist_title = self.artist, year_str = year_str)
        return result_str

    def get_info_link(self, info_dict):
        unsplash_id = info_dict["id"]
        return "https://unsplash.com/photos/" + str(unsplash_id)

class DeepAiPhoto(photo):
    def __init__(self, info):
        info["title"] = "Impressionify"
        info["artist"] = "Generated by deep.ai"
        info["url"] = info["output_url"]
        super().__init__(info)
        self.id = info["id"]
    
    def __str__(self):
        return self.title + ". " + self.artist + ". Id: " + str(self.id)

# Stuffs with the AIC api -----
AIC_URL = "https://api.artic.edu/api/v1/"
def get_random_art(art_genres = ("impressionism", "Cubism", "German Expressionism", "fauvism"), threshold = 0.1):
    '''
    Return a random art in all the genres specified. Retry 10 times max to get a satisfactory image.

    Args: 
        art_genres (tuple or list) -- a tuple or list containing all the genres to search, defult is 
        ("impressionism", "Cubism", "German Expressionism", "fauvism")

        threshold (float) -- only take to top (threshold / 1.0) results among all

    Return:
        The dictionary representing the picked artwork
    '''
    # https://api.artic.edu/api/v1/artworks/search?q=cats 
    # For performance reasons, limit cannot exceed 100. Additionally, you cannot 
    # request more than 10,000 records from a single search query through any 
    # combination of limit and page.
    search_append = "artworks/search?"
    max_index = 999
    max_retry = 10 # max retry chance attemping to get a satisfactory artwork
    accept_medium = ("canvas", "paper", "board", "panel")
    unaccept_medium = ("mixed media", "woodcut", "book", "film", "room", "lithograph")
    min_colorfulness = 25
    limit = 10
    page = 1
    arts_num_lst = []
    arts_dict = {}

    for art_genre in art_genres:
        load = {"limit": limit, "page": page}
        load["q"] = urllib.parse.quote(art_genre)
        res_json = safe_get_json(AIC_URL + search_append, load)
        res_num_info = res_json["pagination"]

        # Pick only the top % results to prevent unrelated or low quality results 
        curr_num = int(min(res_num_info["total"], max_index) * threshold)
        
        arts_num_lst.append(curr_num)
        # store arts into dict
        arts_dict[art_genre] = curr_num

    retry_time = 0
    while retry_time in range(max_retry + 1):
        result_group = art_genres[rand_group(arts_num_lst)]
        print("Selected group is: " + result_group)
        # Get an art from that genre
        picked_num = random.randint(0, arts_dict[result_group] - 1)
        print("Randomly picked number is: " + str(picked_num))
        picked_offst = picked_num % limit
        picked_pg = int((picked_num - picked_offst) / limit)
        picked_load = {"limit": limit, "page": picked_pg}
        picked_load["q"] = urllib.parse.quote(result_group)
        picked_json = safe_get_json(AIC_URL + search_append, picked_load)
        picked_art_brief = picked_json["data"][picked_offst]
        picked_art_link = picked_art_brief["api_link"]
        picked_art_json = safe_get_json(picked_art_link)
        picked_art_medium = picked_art_json["data"]["medium_display"].lower()

        if picked_art_json["data"].get("colorfulness", False) and \
            picked_art_json["data"]["colorfulness"] >= min_colorfulness and \
            any(word in picked_art_medium for word in accept_medium) and \
            not any(word in picked_art_medium for word in unaccept_medium): #minor fix here for better logic
            # met demand
            print("Accepted artwork")
            break;
        else:
            print("Unacceptable artwork, retrying...")
        
        if retry_time % 2 == 0:
            min_colorfulness -= 0.5 # Lower the demand

    return AICPhoto(picked_art_json)

def get_searched_art(keyword, num):
    # https://api.artic.edu/api/v1/artworks/search?q=cats 
    # For performance reasons, limit cannot exceed 100. Additionally, you cannot 
    # request more than 10,000 records from a single search query through any 
    # combination of limit and page.
    search_append = "artworks/search?"
    limit = num
    page = 1
    art_lst = []

    picked_load = {"limit": limit, "page": page}
    picked_load["q"] = urllib.parse.quote(keyword)
    picked_json = safe_get_json(AIC_URL + search_append, picked_load)
    picked_art_brief_lst = picked_json["data"]

    for searched_art in picked_art_brief_lst:
        
        searched_art_link = searched_art["api_link"]
        searched_art_json = safe_get_json(searched_art_link)

        searched_art_obj = AICPhoto(searched_art_json)
        art_lst.append(searched_art_obj.export())


    return art_lst


def get_random_art_json(art_genres = ("impressionism", "Cubism", "German Expressionism", "fauvism"), threshold = 0.1):
    photo = get_random_art(art_genres, threshold)
    result = {
            "title": photo.title,
            "year": photo.artist,
            "alt_text": photo.alt_text,
            "info_link": photo.info_link,
            "url": photo.url,
            "btn_str": "To Artwork Site"
        }
    return result

# Stuffs with the Unsplash api -----
SPLASH_URL = "https://api.unsplash.com/"
def get_random_pic(keyword = "nature", threshold = 0.8, num = 1):
    '''
    Get random picture from search results in unsplash with the provided keyword.

    Args:
        keyword -- the search keyword, default to 'nature'
        num -- should fewer than 10

    Return:
        A photo dictionary containing info about the picture
    '''
    # https://api.unsplash.com/search/photos?query=nature&client_id=xxx
    key_unsplash = get_key("unsplash")

    per_page = 10

    load = {"query": keyword, "client_id": key_unsplash, "per_page": per_page}
    res_json = safe_get_json(SPLASH_URL + "search/photos?", load)
    total_imgs = int(res_json["total"] * threshold)
    picked_num = random.randint(0, total_imgs - 1)
    print("Picked unsplash index is: " + str(picked_num))
    picked_offst = picked_num % per_page
    picked_pg = int((picked_num - picked_offst) / per_page)
    picked_load = {"query": keyword, "client_id": key_unsplash, "per_page": per_page, "page": picked_pg}
    picked_page = safe_get_json(SPLASH_URL + "search/photos?", picked_load)
    if(num == 1):
        picked_photo = picked_page["results"][picked_offst]
        return UnsplashPhoto(picked_photo)

    else:
        photo_lst = picked_page["results"]
        print("Type: ", type(photo_lst))
        picked_photo = photo_lst[:int(num)]
        return [unsplash_dict_helper(UnsplashPhoto(photo)) for photo in picked_photo]

def unsplash_dict_helper(photo):
    result = {
            "title": photo.title,
            "year": photo.artist,
            "alt_text": "Unsplash, the internet’s source of freely-usable images.",
            "info_link": photo.info_link,
            "url": photo.url,
            "btn_str": "View in Unsplash"
        }
    return result

# Stuffs with the Fast Style Transfer api -----
TRANSFER_URL = "https://api.deepai.org/api/fast-style-transfer"
ALT_TRANSFER_URL = " https://api.deepai.org/api/neural-style"  # Another style transfer source
ALT2_TRANSFER_URL = "https://api.deepai.org/api/CNNMRF"  # Yet another style transfer source
def upload_photos(src_url, styl_url):
    load = {"content": src_url, "style": styl_url}
    header = {"api-key": get_key("deepai")}
    res_json = safe_get_json(TRANSFER_URL, load, header)
    # {'id': 'd1ea5878-c8ea-4478-8ca8-6804e533a958', 'output_url': 'https://api.deepai.org/job-view-file/d1ea5878-c8ea-4478-8ca8-6804e533a958/outputs/output.png'}
    return DeepAiPhoto(res_json)

def upload_photos_request(src_url, styl_url):
    '''
    This is used to upload file in DIY
    '''
    r = requests.post(
        "https://api.deepai.org/api/fast-style-transfer",
        files={
            'content': src_url,
            'style': styl_url
        },
        headers= {"api-key": get_key("deepai")}
    )
    print(r.json())
    return DeepAiPhoto(r.json())

def deepai_export(photo_obj):
    result = {
            "title": photo_obj.title,
            "year": photo_obj.artist,
            "alt_text": "This is a fast online style transfer service, resolution may be limited.",
            "info_link": "https://deepai.org/machine-learning-model/fast-style-transfer",
            "url": photo_obj.url,
            "btn_str": "Check out Deep.ai"
    }
    return result


# Stuffs with the super resolution api -----
# !!Outcome not so good
SUPERRES_URL = "https://api.deepai.org/api/torch-srgan"
def supres_photos(src_url):
    load = {"image": src_url}
    header = {"api-key": get_key("deepai")}
    res_json = safe_get_json(SUPERRES_URL, load, header)
    # {'id': 'd1ea5878-c8ea-4478-8ca8-6804e533a958', 'output_url': 'https://api.deepai.org/job-view-file/d1ea5878-c8ea-4478-8ca8-6804e533a958/outputs/output.png'}
    return res_json


def get_rand_comb():
    deep_ai_site_link = "https://deepai.org/machine-learning-model/fast-style-transfer"
    art_work_obj = get_random_art(threshold = 0.1)
    nature_pic_obj = get_random_pic()
    final_pic_obj = upload_photos(nature_pic_obj.url, art_work_obj.url)
    result_dict = {
        "deepai":{
            "title": final_pic_obj.title,
            "year": final_pic_obj.artist,
            "alt_text": "This is a fast online style transfer service, resolution may be limited.",
            "info_link": deep_ai_site_link,
            "url": final_pic_obj.url,
            "btn_str": "Check out Deep.ai"
        },
        "art":{
            "title": art_work_obj.title,
            "year": art_work_obj.artist_display,
            "alt_text": art_work_obj.alt_text,
            "info_link": art_work_obj.info_link,
            "url": art_work_obj.url,
            "btn_str": "To ArtWork Site"
        },
        "unsplash":{
            "title": nature_pic_obj.title,
            "year": nature_pic_obj.artist,
            "alt_text": "Unsplash, the internet’s source of freely-usable images.",
            "info_link": nature_pic_obj.info_link,
            "url": nature_pic_obj.url,
            "btn_str": "View in Unsplash"
        }
    }
    # order matters!
    return result_dict


def main():
    artist_tpl = ("Renoir", "Cezanne", "Monet", "van Gogh", "Seurat", "Munch", "Mondrian", "Matisse", "Chagall", "Kandinsky")
    art_work_lst = []
    nature_pic_lst = []
    final_pic_lst = []
    # nature_pic_lst = get_random_pic(keyword="chris_chow", num=10)

    # Gives some example output
    # for i in range(20):
        # art_work_obj = get_random_art(threshold = 0.1)
        # print(art_work_obj)
        # art_work_lst.append(art_work_obj)
        # nature_pic_obj = get_random_pic()
        # nature_pic_lst.append(nature_pic_obj)
        # final_pic_obj = upload_photos(nature_pic_obj.url, art_work_obj.url)
        # final_pic_lst.append(final_pic_obj)

    # print("art_work_lst: " + str([art_work.__str__() for art_work in art_work_lst]))
    # print("nature_pic_lst: " + str([art_work.__str__() for art_work in nature_pic_lst]))
    # print("final_pic_lst: " + str([art_work.url for art_work in final_pic_lst]))
    # print(nature_pic_lst)

    # for art in get_searched_art("PoppyField", 10):
    #     print(art)

if __name__ == "__main__":
    main()