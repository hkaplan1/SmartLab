from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

access_key = "077ab2a1817aecb1dbacb4cc58439f447eeffc76"

device1 = "210042001747343338333633"
device2 = "340037001147353136383631"
# nested_dictionaries = {projectnumber:{step#:{device_id:x,command:y}}}
projectData = {1:
                [{"device_id":device1,"function":"step1"},
                 {"device_id":device1,"function":"step2"},

                 {"device_id":device2,"function":"step3"},
                 {"device_id":device2,"function":"step4"}],
               2:
                [{"device_id":device1,"function":"step1"},
                {"device_id":device2,"function":"step3"},
                 {"device_id":device1,"function":"step2"},

                 {"device_id":device2,"function":"step4"}]
               }


@app.route('/project1')
def project1():
    return render_template('project1.html',access_key=access_key,project_data=projectData[1])

@app.route('/project2')
def project2():
    return render_template('project1.html',access_key=access_key,project_data=projectData[2])

if __name__ == "__main__":
    app.run(port=5000,debug = True)
