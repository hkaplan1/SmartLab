function firstStep(){
  var device_id = document.getElementById("device_id1").innerText;
  var funct = document.getElementById("function1").innerText;
  var access = document.getElementById("access_token").innerText;
  $.ajax({
    type: 'POST',
    url: "https://api.particle.io/v1/devices/"+device_id+"/"+funct,
    data: {
      access_token:access,
      arg:"on"},
    success: function(data, status, xhr){
      console.log("ok")
    },
    error: function(xhr, status, err) {
      console.log("error")

    }
  });
};

function postForms(step){
  var step = step.toString();
  var stepPrev = (step-1).toString();
  var id1="device_id"+step;
  var id2 = "function"+step;
  var id3= "device_id"+stepPrev;
  var id4 = "function"+stepPrev;
  var device_id = document.getElementById(id1).innerText;
  var funct = document.getElementById(id2).innerText;
  var device_idPrev = document.getElementById(id3).innerText;
  var functPrev = document.getElementById(id4).innerText;
  var access = document.getElementById("access_token").innerText;
  $.ajax({
    type: 'POST',
    url: "https://api.particle.io/v1/devices/"+device_idPrev+"/"+functPrev,
    data: {
      access_token:access,
      arg:"off"},
    success: function(data, status, xhr){
      console.log("ok")
    },
    error: function(xhr, status, err) {
      console.log("error")
    }
  });
  $.ajax({
    type: 'POST',
    url: "https://api.particle.io/v1/devices/"+device_id+"/"+funct,
    data: {
      access_token:access,
      arg:"on"},
    success: function(data, status, xhr){
      console.log("ok")
    },
    error: function(xhr, status, err) {
      console.log("error")
    }
  });
};

function end(){
  var device_id = document.getElementById("device_idLast").innerText;
  var funct = document.getElementById("functionLast").innerText;
  var access = document.getElementById("access_token").innerText;
  $.ajax({
    type: 'POST',
    url: "https://api.particle.io/v1/devices/"+device_id+"/"+funct,
    data: {
      access_token:access,
      arg:"off"},
    success: function(data, status, xhr){
      console.log("ok")
    },
    error: function(xhr, status, err) {
      console.log("error")

    }
  });
};


function searchProjects() {
    // Declare variables
    var input, filter, ul, li, a, i;
    input = document.getElementById('myInput');
    filter = input.value.toUpperCase();
    ul = document.getElementById("myUL");
    li = ul.getElementsByTagName('li');

    // Loop through all list items, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
        a = li[i].getElementsByTagName("a")[0];
        if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
        } else {
            li[i].style.display = "none";
        }
    }
}
