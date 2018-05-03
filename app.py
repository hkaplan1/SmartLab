from flask import Flask, Markup, flash, render_template, jsonify, session, request, json
import requests
import urllib


app = Flask(__name__)
app.secret_key = 'smartlab'
app.jinja_env.filters['json'] = lambda v: Markup(json.dumps(v))
# particle access key
access_key = "077ab2a1817aecb1dbacb4cc58439f447eeffc76"

airTable_key = "keychadtrZj5TMvY1"
authorization = "Bearer " + airTable_key


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('hub.html')

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/guides')
def guides():
    headers = {
        'Authorization': authorization,
    }
    response = requests.get("https://api.airtable.com/v0/apphVTQe3k0dgvpjV/Hub%20Projects", headers=headers)
    projects = []
    for i in response.json()['records']:
        try:
            projects.append([i['fields']['Project Name'],i['fields']['Main Photo'][0]['url'],i['id']])
        except:
            projects.append([i['fields']['Project Name'],i['id']])

    return render_template('guides.html', projects = projects)

def chomp(s):
    return s[:-1] if s.endswith('\n') else s

@app.route('/guides/', defaults ={'project_id':''})
@app.route('/guides/<string:project_id>')
def guide(project_id):
    session['project_id'] = project_id

    # get projects table data
    headers = {
        'Authorization': authorization,
    }
    project_response = requests.get("https://api.airtable.com/v0/apphVTQe3k0dgvpjV/Hub%20Projects", headers=headers)
    project = {}

    steps2 = {}
    # collect all steps from project table
    for i in project_response.json()['records']:
        if i['id'] == project_id:
            project['name'] = i['fields']['Project Name']
            try:
                videos = i['fields']['Videos'].strip().split(',')
                for k in range(len(videos)):
                    videos[k] = chomp(videos[k])
                session['videos'] = videos
            except:
                pass

            j = 1
            steps = []
            while True:
                materialTag = 'Step ' + str(j) + ' Materials'
                textTag = 'Step ' + str(j) + ' Text'
                photoTag= 'Step ' + str(j) + ' Photos'
                try:
                    steps.append([i['fields'][materialTag],i['fields'][textTag]])
                    try:
                        photos = []
                        for photo in i['fields'][photoTag]:
                            photos.append(photo['url'])
                        steps2[str(j-1)] = {'text':i['fields'][textTag],'photos':photos}
                        j += 1
                    except:
                        pass
                except:
                    break
            project['steps'] = steps
            break

    print(steps2)
    #get material categories from materials table data
    material_response = requests.get("https://api.airtable.com/v0/apphVTQe3k0dgvpjV/tblB5R6ZDXJ2Z4YoQ?sort%5B0%5D%5Bfield%5D=ID+%23&sort%5B0%5D%5Bdirection%5D=asc", headers=headers)
    stepCat = []

    categories = set()
    for step in project['steps']:
        for material in step[0]:
            for item in material_response.json()['records']:
                if item['id'] == material:
                    categories.add(item['fields']['Category'][0])
                    break
        stepCat.append(categories)
        categories = set()


    #convert categories for each step, to areas for each step
    area_response = requests.get("https://api.airtable.com/v0/apphVTQe3k0dgvpjV/Space%20Organization?&view=Grid%20view", headers=headers)
    functions = {}
    stepAreas = []
    areas = set()
    for k in stepCat:
        for step2 in k:
            for area in area_response.json()['records']:
                if area['id'] == step2:
                    areas.add(area['fields']['Area'][0])
                    try:
                        functions[area['fields']['Area'][0]].append(area['fields']['Associated Neopixels'])
                    except:
                        functions[area['fields']['Area'][0]] = [area['fields']['Associated Neopixels']]
                    break

        stepAreas.append(areas)
        areas = set()

    #convert areas for each step, to devices for each step
    deviceData = requests.get("https://api.airtable.com/v0/apphVTQe3k0dgvpjV/Space%20Areas?view=Grid%20view",headers = headers)
    stepDevices = []
    devices = set()
    for l in stepAreas:
        for step3 in l:
            for deviceArea in deviceData.json()['records']:
                if deviceArea['id'] == step3:
                    devices.add((deviceArea['fields']['MIT'][0],functions[step3].pop(0)))
                    break
        stepDevices.append(devices)
        devices = set()

    #convert devices to device_ids
    deviceIds = requests.get("https://api.airtable.com/v0/apphVTQe3k0dgvpjV/Particle%20Devices?view=Grid%20view",headers = headers)
    stepIds = []
    Ids = set()
    allIds = set()
    for k in stepDevices:
        for step4 in k:
            for device in deviceIds.json()['records']:
                if device['id'] == step4[0]:
                    Ids.add((device['fields']['Particle Device ID'],step4[1]))
                    allIds.add(device['fields']['Particle Device ID'])
                    break
        stepIds.append(list(Ids))
        Ids = set()
    current_step = []

    print(steps2)
    for l in range(0,len(stepIds)):
        for m in stepIds[l]:
            current_step.append({"deviceid":m[0],"function":m[1]})
        steps2[str(l)]['lights'] = current_step
        current_step = []
    allSteps = {}
    allSteps['steps'] = steps2
    particles = {}
    particles['devices'] = list(allIds)



    stepsTextImg = {}
    for s in range(len(allSteps['steps'])):
        stepsTextImg[str(s)] = [allSteps['steps'][str(s)]['text'],allSteps['steps'][str(s)]['photos']]



    return render_template('slideshow.html',name = project['name'],template_steps = stepIds, script_steps = json.dumps(allSteps),stepsTextImg = stepsTextImg, devices = json.dumps(particles))

@app.route('/videos')
def videos():
    videos = session['videos']
    return render_template('videos.html',videos=videos)

@app.route('/themes')
def theme():
    return render_template('themes.html')

@app.route('/materials')
def materials():
    headers = {
        'Authorization': authorization,
    }
    #get all tags from airtable
    tags = []
    tagResponse = requests.get("https://api.airtable.com/v0/apphVTQe3k0dgvpjV/Material%2FTechnical%20Tags", headers=headers)
    for k in tagResponse.json()['records']:
        tags.append((k['fields']['Material Tags'],k['fields']['Material Tags'].replace(" ","")))

    #get all materials from airtable
    response = requests.get("https://api.airtable.com/v0/apphVTQe3k0dgvpjV/Material%20Database", headers=headers)
    materials = []
    for i in response.json()['records']:
        part_info = {}
        #build dictionaries for each mateirl with name,category,id, and tags
        #not all parts will have tags hence the try,except
        try:
            part_info['name'] = i['fields']['Name']
            part_info['id'] = i ['id']
            part_info['category'] = i['fields']['Category']
            try:
                part_tags = []
                for tag in i['fields']['Technical Tags']:
                    for j in tagResponse.json()['records']:
                        if tag == j['id']:
                            part_tags.append(j['fields']['Material Tags'].replace(" ",""))
                part_info['tags'] = part_tags
            except:
                pass
            materials.append(part_info)
        except:
            pass
    print(materials)
    return render_template('materials.html',materials=materials, tags = tags)
#
# @app.route('/videoHub')
# def videoHub():
#     return render_template('video_hub.html')
#
# @app.route('/projectVideos')
# def projectVideos():
#     headers = {
#         'Authorization': authorization,
#     }
#     response = requests.get("https://api.airtable.com/v0/apphVTQe3k0dgvpjV/Hub%20Projects", headers=headers)
#     projects = []
#     for i in response.json()['records']:
#         try:
#             projects.append([i['fields']['Project Name'],i['fields']['Main Photo'][0]['url'],i['id']])
#         except:
#             projects.append([i['fields']['Project Name'],i['id']])
#
#     project_response = requests.get("https://api.airtable.com/v0/apphVTQe3k0dgvpjV/Hub%20Projects", headers=headers)
#     project_videos = []
#
#     steps2 = {}
#     # collect all steps from project table
#     for item in projects:
#         for i in project_response.json()['records']:
#             if i['id'] == item[-1]:
#                 project = {}
#                 project['name'] = item[0]
#                 if len(item) > 2:
#                     project['photo'] = item[1]
#                 try:
#                     videos = i['fields']['Videos'].strip().split(',')
#                     for k in range(len(videos)):
#                         videos[k] = chomp(videos[k])
#                     project['videos'] = videos
#                     project['id'] = i['id']
#                     project_videos.append(project)
#                 except:
#                     pass
#
#     session['project_videos']  = project_videos
#     return render_template('projectvideos.html',project_videos=project_videos)
#
# @app.route('/projectVideos/', defaults ={'project_id':''})
# @app.route('/projectVideos/<string:project_id>')
# def projectVideo(project_id):
#     for i in session['project_videos']:
#         if i['id'] == project_id:
#             current = i
#     return render_template('showVideos.html',project = i)



if __name__ == "__main__":
    app.run(port=5000,debug = True)
