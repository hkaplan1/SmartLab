// $(document).ready( function(){
//   var step = document.getElementById('step').value;
//   console.log(step)
//   $('#forms').submit(function(step){
//     $.ajax({
//           type: 'POST',
//           async: false,
//           url: "https://api.particle.io/v1/devices/{{project_data[step-1]['device_id']}}/{{project_data[step-1]['function']}}?access_token={{access_key}}",
//           data: "off",
//           success: function(data, status, xhr){
//             alert('ok');
//           },
//           error: function(xhr, status, err) {
//             alert(status + ": " + err);
//           }
//     });
//     $.ajax({
//       type: 'POST',
//       async: false,
//       url: "https://api.particle.io/v1/devices/{{project_data[step]['device_id']}}/{{project_data[step]['function']}}?access_token={{access_key}}",
//       data: "on",
//       success: function(data, status, xhr){
//         alert('ok');
//       },
//       error: function(xhr, status, err) {
//         alert(status + ": " + err);
//       }
//     });
//
//   });
// });
