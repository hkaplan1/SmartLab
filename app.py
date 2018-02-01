from flask import Flask, render_template
import requests


app = Flask(__name__)

# particle access key
access_key = "077ab2a1817aecb1dbacb4cc58439f447eeffc76"

device1 = "210042001747343338333633"
device2 = "340037001147353136383631"
# nested_dictionaries = {projectnumber:{step#:{device_id:x,command:y}}}
projectData = {1:{"name":"Project 1",
                  "steps":[{"device_id":device1,"function":"step1"},
                           {"device_id":device1,"function":"step2"},
                           {"device_id":device2,"function":"step3"},
                           {"device_id":device2,"function":"step4"}]},
               2:{"name":"Project 2",
                  "steps":[{"device_id":device1,"function":"step1"},
                           {"device_id":device2,"function":"step3"},
                           {"device_id":device1,"function":"step2"},
                           {"device_id":device2,"function":"step4"}]},
                3:{"name":"Project 3",
                   "steps":[{"device_id":device2,"function":"step4"}]}
               }

airTable_key = "keychadtrZj5TMvY1"
authorization = "Bearer " + airTable_key

@app.route('/airtable')
def airtable():
    headers = {
        'Authorization': authorization,
        'maxRecords': '100'
    }
    response = requests.get("https://api.airtable.com/v0/apphVTQe3k0dgvpjV/Hub%20Projects?view=Grid%20view", headers=headers)
    projects = []
    for i in response.json()['records']:
        projects.append(i['fields']['Project Name'])

    return render_template('airtable.html', projects = projects)

@app.route('/')
def home():
    return render_template('hub.html')

@app.route('/themes')
def theme():
    return render_template('projects.html')


@app.route('/guides')
def guide():
    projects = []
    for key, value in sorted(projectData.items()):
        print(key,value)
        projects.append((key,value['name']))

    return render_template('guides.html',projects = projects)


@app.route('/guides/', defaults={'project': 1})
@app.route('/guides/<int:project>')
def show_project(project):
    return render_template('project.html',
        access_key=access_key,
        project_data = projectData[project]
    )


if __name__ == "__main__":
    app.run(port=5000,debug = True)
