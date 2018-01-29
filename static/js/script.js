function firstStep(){
  var device_id = document.getElementById("device_id1").innerText;
  var funct = document.getElementById("function1").innerText;
  $.ajax({
    type: 'POST',
    url: "https://api.particle.io/v1/devices/"+device_id+"/"+funct,
    data: {
      access_token:"{{access_key}}",
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
  $.ajax({
    type: 'POST',
    url: "https://api.particle.io/v1/devices/"+device_idPrev+"/"+functPrev,
    data: {
      access_token:"{{access_key}}",
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
      access_token:"{{access_key}}",
      arg:"on"},
    success: function(data, status, xhr){
      console.log("ok")
    },
    error: function(xhr, status, err) {
      console.log("error")
    }
  });
};
