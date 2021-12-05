from flask import Flask, render_template, request, redirect, jsonify, url_for
import modules.supportfunc as supportfunc
import modules.application as application
import os, json, urllib, sys

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024
FILE_DICT = "userupload"
ART_DICT = "aicphoto"
AI_DICT = "result"

page_info = {
	"#explore": {
		"title": "Explore",
		"content_id": ["explore-content"]
	},
	"#lucky": {
		"title": "I'm Feeling Lucky",
		"content_id": ["lucky-content"]
	},
	"#diy": {
		"title": "Do It Yourself",
		"content_id": ["diy-content-01", "diy-content-02", "diy-content-03"]
	},
	"#about": {
		"title": "About",
		"content_id": ["about"]
	}
}

basepath = "./"
loc_link = "static"

file_dir = os.path.join(basepath, loc_link, FILE_DICT)
art_dir = os.path.join(basepath, loc_link, ART_DICT)
result_dir = os.path.join(basepath, loc_link, AI_DICT)

if not os.path.isdir(file_dir):
	os.mkdir(file_dir)

if not os.path.isdir(art_dir):
	os.mkdir(art_dir)

if not os.path.isdir(result_dir):
	os.mkdir(result_dir)

@app.route('/')
def index():
	header_img = supportfunc.get_header_image(basepath)
	supportfunc.clear_expire_file(file_dir)
	supportfunc.clear_expire_file(art_dir)
	supportfunc.clear_expire_file(result_dir)

	return render_template('index.html', explore_data = supportfunc.get_dict(), lucky_data = application.get_rand_comb(), header_img = header_img)

@app.route('/switchtab', methods=['POST'])
def process():
	'''
	Used to switch tabs when user clicks
	'''
	print("Switch Tabs")
	target_page = request.form['target']
	print("Data: " +  target_page)

	return_dict = {
		"info":  page_info[target_page]
		}
	return jsonify(return_dict)

@app.route('/discover', methods=['POST'])
def prepdiscover():
	'''
	Prepare data for discovery when user clicks
	'''
	print("Prepare for Discover")
	
	result = supportfunc.get_dict().get(request.form['target'])
	print("Data: " +  str(result))
	return_dict = {
		"info":  result,
		"from":  request.form['target']
		}
	return jsonify(return_dict)

@app.route('/refreshlucky', methods=['POST'])
def preplucky():
	'''
	Refresh data for I'm feeling lucky when user clicks
	'''
	print("Prepare for I'm feeling lucky")
	
	result = application.get_rand_comb();
	print("Data: " +  str(result))
	return_dict = {
		"info":  result,
		}
	return jsonify(return_dict)

@app.route('/getrandart', methods=['POST'])
def preprandart():
	'''
	
	'''
	print("Prepare for rand art")
	print(request.form['num'])
	print(request.form['keyword'])
	keywords = json.loads(request.form['keyword'])
	result = []
	for i in range(int(request.form['num'])):
		result.append(application.get_random_art_json(art_genres = keywords))
	print("Data: " +  str(result))
	return_dict = {
		"info":  result,
		}
	return jsonify(return_dict)

@app.route('/getsearchart', methods=['POST'])
def prepsearchart():

	print("Prepare for search art")
	print(request.form['num'])
	print(request.form['keyword'])
	keywords = json.loads(request.form['keyword'])
	result = []
	result = application.get_searched_art(keyword=keywords[0], num=request.form['num'])
	print("Data: " +  str(result))
	return_dict = {
		"info":  result,
		}
	return jsonify(return_dict)


@app.route('/uploadfile', methods=['POST'])
def upload_file():
	uploaded_file = request.files['file']
	print("Name: " + str(uploaded_file.filename))
	return_dict = {
		"org_fileloc":  ""
	}
	if uploaded_file.filename != '':
		rand = str(supportfunc.randgen())
		os.mkdir(os.path.join(loc_link, FILE_DICT, rand))
		temp_path = os.path.join(loc_link, FILE_DICT, rand, uploaded_file.filename)
		uploaded_file.save(temp_path)
		temp_path = supportfunc.validate_path(temp_path)
		return_dict = {
			"org_fileloc":  temp_path,
			"filename": uploaded_file.filename
		}
	print(temp_path)
	return jsonify(return_dict)

@app.route('/finaldisplay', methods=['POST'])
def finaldisplay():
	print("Prepare for final display")
	print(request.form['art'])
	print(request.form['img'])
	# download art from link

	rand_dir = str(supportfunc.randgen())
	file_loc = os.path.join(loc_link, ART_DICT, rand_dir, "aic.jpg")
	os.mkdir(os.path.join(loc_link, ART_DICT, rand_dir))
	urllib.request.urlretrieve(request.form['art'], file_loc)

	result_obj = application.upload_photos_request(open(request.form['img'],"rb"), open(file_loc,"rb"))
	# save file
	rand_dir = str(supportfunc.randgen())
	result_loc = os.path.join(loc_link, AI_DICT, rand_dir)
	os.mkdir(result_loc)
	urllib.request.urlretrieve(result_obj.url, os.path.join(result_loc, "result.jpg"))

	result_xs = application.deepai_export(result_obj)
	result_xs["info_link"] = os.path.join(result_loc, "result.jpg")
	print("Data: " +  str(result_xs))
	return_dict = {
		"info":  result_xs,
		}
	return jsonify(return_dict)


if __name__ == '__main__':
	app.run(debug=True)