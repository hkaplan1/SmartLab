from flask import Flask, render_template
app = Flask(__name__)

access_key = "077ab2a1817aecb1dbacb4cc58439f447eeffc76"

device1 = "210042001747343338333633"
device2 = "340037001147353136383631"
# nested_dictionaries = {projectnumber:{step#:{device_id:x,command:y}}}
projectData = {1:
                [{"name":"Project 1"},
                 {"device_id":device1,"function":"step1"},
                 {"device_id":device1,"function":"step2"},

                 {"device_id":device2,"function":"step3"},
                 {"device_id":device2,"function":"step4"}],
               2:
                [{"name":"Project 2"},
                {"device_id":device1,"function":"step1"},
                {"device_id":device2,"function":"step3"},
                 {"device_id":device1,"function":"step2"},

                 {"device_id":device2,"function":"step4"}]
               }



@app.route('/')
def home():
    projects = []
    for key, value in sorted(projectData.items()):
        print(key,value)
        projects.append((key,value[0]['name']))

    return render_template('index.html',projects = projects)


@app.route('/projects/', defaults={'project': 1})
@app.route('/projects/<int:project>')
def show_users(project):
    return render_template('projects.html',
        access_key=access_key,
        project_data = projectData[project]
    )


if __name__ == "__main__":
    app.run(port=5000,debug = True)
