$(document).ready(function(){
  var select = document.getElementById("selecter");
  var cnt = 0;
  navigator.mediaDevices.enumerateDevices()
  .then(function(devices) {
    devices.forEach(function(device) {
      if(device.kind == "videoinput"){
        var Id = device.deviceId;
        var Label;
        if(device.label.indexOf('(') != -1){
           Label = device.label.slice(0,device.label.indexOf('('));
           Label = document.createTextNode(String(cnt) + " : " + Label);
        }else{
           Label = document.createTextNode(String(cnt) + " : " + device.label);
        }
          console.log(device.label);
          $('#selector').append($('<option>').html(Label).val(Id));
          cnt += 1;

      }
    });
     // エラー発生時
  }).catch(function(err) {
    // console.error('カメラの接続に失敗しました', err);
});
});


//カメラプレビュー
  var constraints = { audio: false, video: {
      width: 1920,
      height: 1080,
  }}

  navigator.mediaDevices.getUserMedia(constraints)
    .then(function(stream) {
      var video = document.querySelector('video');
      video.srcObject = stream;
      video.onloadedmetadata = function(e) {
        video.play();
      };
    })
    .catch(function(err) {
      console.log(err.name + ": " + err.message);
    });

//セレクトしたカメラに切り替え
$(function($) {
    $('#selector').change(function() {
        constraints.video.deviceId = $('#selector option:selected').val();
        video.srcObject.getTracks().forEach(track => track.stop())
        navigator.mediaDevices.getUserMedia(constraints)
          .then(function(stream) {
            const video = document.querySelector('video');
            video.srcObject = stream;
            video.onloadedmetadata = function(e) {
              video.play();
            };
          })
          .catch(function(err) {
            console.log(err.name + ": " + err.message);
          });
    });

});

// // 確認ボタンを押したときにカメラが使用できるか確認

eel.expose(js_function);
function js_function(){
  return $('#selector option:selected').text().slice(0,1);
}

function clickBtn1(){
  eel.open_endpage();
}

function end_ok(){
  eel.py_sysclose();
  window.close();
}

function end_no(){
  window.close();
}

eel.expose(sys_close);
function sys_close() {
    window.close();
}

eel.expose(windowclose)
function windowclose(){
  window.close();
}

eel.expose(set_posegauge);
function set_posegauge(cnt_pose, name_pose){

  /*７割越えのポーズのゲージのみを取得したい場合はこれ*/
  var target = document.getElementById("poseGuage");

  target.innerHTML = cnt_pose + '回，' + name_pose + '<meter max= "100" min= "0" low= "20" high= "80" optimum= "90" value= ' + cnt_pose +'></meter>';

}
