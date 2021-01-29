function clickBtn1(){
  const hidden_box = document.getElementById("hidden_box");

  if(hidden_box.style.display=="block"){
    hidden_box.style.display ="none";
  }else{
   hidden_box.style.display ="block";
  }
}

eel.expose(endSwitch);
function endSwitch(){
  /*FOCUS終了フラグを立てた後、元の値に戻す*/
  eel.sysclose_switch(0);
}

eel.expose(closeSwitch);
function closeSwitch(){
  //×ボタンが押されたフラグ(1)を元に戻す(0)
  eel.close_switch(0);
}

eel.expose(windowclose);
function windowclose(){
  // pythonからwindowを閉じる関数
  window.close();
}

eel.expose(set_posegauge);
function set_posegauge(name_pose){
  const pose_palm = document.getElementById("pose_palm");
  const pose_rock = document.getElementById("pose_rock");
  const pose_gun = document.getElementById("pose_gun");
  const pose_three = document.getElementById("pose_three");
  const pose_peace = document.getElementById("pose_peace");
  const pose_dang = document.getElementById("pose_dang");
  const pose_one = document.getElementById("pose_one");
  const idf_hand = document.getElementById("idf_hand")
  switch(name_pose){
    case "Palm":
      if(pose_palm.classList.contains('pose_highlight')==false){
        pose_palm.classList.add("pose_highlight");
        pose_rock.classList.remove("pose_highlight");
        pose_gun.classList.remove("pose_highlight");
        pose_three.classList.remove("pose_highlight");
        pose_peace.classList.remove("pose_highlight");
        pose_dang.classList.remove("pose_highlight");
        pose_one.classList.remove("pose_highlight");
        idf_hand.innerHTML='<img id="idf_hand_img" src="../images/green_lamp.png" alt="" width="20px">手が検出されています。';
      }
      break;
    case "Rock":
      if(pose_rock.classList.contains('pose_highlight')==false){
        pose_palm.classList.remove("pose_highlight");
        pose_rock.classList.add("pose_highlight");
        pose_gun.classList.remove("pose_highlight");
        pose_three.classList.remove("pose_highlight");
        pose_peace.classList.remove("pose_highlight");
        pose_dang.classList.remove("pose_highlight");
        pose_one.classList.remove("pose_highlight");
        idf_hand.innerHTML='<img id="idf_hand_img" src="../images/green_lamp.png" alt="" width="20px">手が検出されています。';
      }
        break;
    case "Gun":
      if(pose_gun.classList.contains('pose_highlight')==false){
        pose_palm.classList.remove("pose_highlight");
        pose_rock.classList.remove("pose_highlight");
        pose_gun.classList.add("pose_highlight");
        pose_three.classList.remove("pose_highlight");
        pose_peace.classList.remove("pose_highlight");
        pose_dang.classList.remove("pose_highlight");
        pose_one.classList.remove("pose_highlight");
        idf_hand.innerHTML='<img id="idf_hand_img" src="../images/green_lamp.png" alt="" width="20px">手が検出されています。';
      }
      break;
    case "Three":
      if(pose_three.classList.contains('pose_highlight')==false){
        pose_palm.classList.remove("pose_highlight");
        pose_rock.classList.remove("pose_highlight");
        pose_gun.classList.remove("pose_highlight");
        pose_three.classList.add("pose_highlight");
        pose_peace.classList.remove("pose_highlight");
        pose_dang.classList.remove("pose_highlight");
        pose_one.classList.remove("pose_highlight");
        idf_hand.innerHTML='<img id="idf_hand_img" src="../images/green_lamp.png" alt="" width="20px">手が検出されています。';
      }
      break;
    case "Peace":
      if(pose_peace.classList.contains('pose_highlight')==false){
        pose_palm.classList.remove("pose_highlight");
        pose_rock.classList.remove("pose_highlight");
        pose_gun.classList.remove("pose_highlight");
        pose_three.classList.remove("pose_highlight");
        pose_peace.classList.add("pose_highlight");
        pose_dang.classList.remove("pose_highlight");
        pose_one.classList.remove("pose_highlight");
        idf_hand.innerHTML='<img id="idf_hand_img" src="../images/green_lamp.png" alt="" width="20px">手が検出されています。';
      }
      break;
    case "Dang":
      if(pose_dang.classList.contains('pose_highlight')==false){
        pose_palm.classList.remove("pose_highlight");
        pose_rock.classList.remove("pose_highlight");
        pose_gun.classList.remove("pose_highlight");
        pose_three.classList.remove("pose_highlight");
        pose_peace.classList.remove("pose_highlight");
        pose_dang.classList.add("pose_highlight");
        pose_one.classList.remove("pose_highlight");
        idf_hand.innerHTML='<img id="idf_hand_img" src="../images/green_lamp.png" alt="" width="20px">手が検出されています。';
      }
      break;
    case "One":
      if(pose_one.classList.contains('pose_highlight')==false){
        pose_palm.classList.remove("pose_highlight");
        pose_rock.classList.remove("pose_highlight");
        pose_gun.classList.remove("pose_highlight");
        pose_three.classList.remove("pose_highlight");
        pose_peace.classList.remove("pose_highlight");
        pose_dang.classList.remove("pose_highlight");
        pose_one.classList.add("pose_highlight");
        idf_hand.innerHTML='<img id="idf_hand_img" src="../images/green_lamp.png" alt="" width="20px">手が検出されています。';
      }
      break;
    case "None":
      pose_palm.classList.remove("pose_highlight");
      pose_rock.classList.remove("pose_highlight");
      pose_gun.classList.remove("pose_highlight");
      pose_three.classList.remove("pose_highlight");
      pose_peace.classList.remove("pose_highlight");
      pose_dang.classList.remove("pose_highlight");
      pose_dang.classList.remove("pose_highlight");
      idf_hand.innerHTML='<img id="idf_hand_img" src="../images/red_lamp.png" alt="" width="20px">手が検出されていません。';
  }
}

/*ここから試作用、不要になったら削除*/
/*eel.expose(test_clickBtn1);*/
function test_clickBtn1(){
  /*起動(テスト用ボタン)押下時*/
  eel.start_flg();
  // window.close();
}

/*eel.expose(test_clickBtn2);*/
function test_clickBtn2(){
  /*終了(テスト用ボタン)押下時*/
  eel.end_flg();
  window.close();
}

function endBtn(){
  eel.open_endpage();
}

eel.expose(focusSwitch);
function focusSwitch(width, height, focus_flg){
  if(focus_flg == 1){
    window.resizeTo(400, 200)
    window.moveTo(width-400,height-200)
    console.log("focus_flg is 1");
  }else{
    window.resizeTo(1025,775)
    window.moveTo(width/4, height/4)
    console.log("focus_flg is 0");
  }
}
