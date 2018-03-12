from flask import Flask, flash, render_template, jsonify, session, request
import requests
import json
import urllib


app = Flask(__name__)
app.secret_key = 'smartlab'
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

    # collect all steps from project table
    for i in project_response.json()['records']:
        if i['id'] == project_id:
            project['name'] = i['fields']['Project Name']
            videos = i['fields']['Videos'].strip().split(',')
            for k in range(len(videos)):
                videos[k] = chomp(videos[k])
            session['videos'] = videos

            j = 1
            steps = []
            while True:
                materialTag = 'Step ' + str(j) + ' Materials'
                textTag = 'Step ' + str(j) + ' Text'
                try:
                    steps.append([i['fields'][materialTag],i['fields'][textTag]])
                    j += 1
                except:
                    break
            project['steps'] = steps
            break

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
                    print('AREA')
                    print(area)
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
    for j in stepDevices:
        for step4 in j:
            for device in deviceIds.json()['records']:
                if device['id'] == step4[0]:
                    Ids.add((device['fields']['Particle Device ID'],step4[1]))
                    allIds.add(device['fields']['Particle Device ID'])
                    break
        stepIds.append(list(Ids))
        Ids = set()
    steps = {}
    steps['steps'] = stepIds

    return render_template('projects.html',name = project['name'],template_steps = stepIds, script_steps = steps, devices = list(allIds))


@app.route('/videos')
def videos():
    videos = session['videos']
    return render_template('videos.html',videos=videos)

@app.route('/themes')
def theme():
    return render_template('themes.html')



if __name__ == "__main__":
    app.run(port=5000,debug = True)
