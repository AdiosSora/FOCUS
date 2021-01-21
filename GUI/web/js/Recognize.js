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
      window.close();
    }

    /*
    function window.onbeforeunload(){
      eel.py_sysclose();
    }
    */
    eel.expose(set_elapsedtime);
    function set_elapsedtime(elapsedtime) {
        document.getElementById("elapsedtime").innerHTML = "elapsedtime:" + elapsedtime + "s";
    }

    eel.expose(set_base64image);
    function set_base64image(base64image) {
        document.getElementById("python_video").src = base64image;
    }

    eel.expose(set_posegauge);
    function set_posegauge(name_pose){
      switch(name_pose){
        case "Palm":
          if(document.getElementById("pose_palm").classList.contains('pose_highlight')==false){
            document.getElementById("pose_palm").classList.add("pose_highlight");
            document.getElementById("pose_rock").classList.remove("pose_highlight");
            document.getElementById("pose_gun").classList.remove("pose_highlight");
            document.getElementById("pose_three").classList.remove("pose_highlight");
            document.getElementById("pose_peace").classList.remove("pose_highlight");
            document.getElementById("pose_dang").classList.remove("pose_highlight");
            document.getElementById("pose_one").classList.remove("pose_highlight");
          }
          break;
        case "Rock":
          if(document.getElementById("pose_rock").classList.contains('pose_highlight')==false){
            document.getElementById("pose_palm").classList.remove("pose_highlight");
            document.getElementById("pose_rock").classList.add("pose_highlight");
            document.getElementById("pose_gun").classList.remove("pose_highlight");
            document.getElementById("pose_three").classList.remove("pose_highlight");
            document.getElementById("pose_peace").classList.remove("pose_highlight");
            document.getElementById("pose_dang").classList.remove("pose_highlight");
            document.getElementById("pose_one").classList.remove("pose_highlight");
          }
            break;
        case "Gun":
          if(document.getElementById("pose_gun").classList.contains('pose_highlight')==false){
            document.getElementById("pose_palm").classList.remove("pose_highlight");
            document.getElementById("pose_rock").classList.remove("pose_highlight");
            document.getElementById("pose_gun").classList.add("pose_highlight");
            document.getElementById("pose_three").classList.remove("pose_highlight");
            document.getElementById("pose_peace").classList.remove("pose_highlight");
            document.getElementById("pose_dang").classList.remove("pose_highlight");
            document.getElementById("pose_one").classList.remove("pose_highlight");
          }
          break;
        case "Three":
          if(document.getElementById("pose_three").classList.contains('pose_highlight')==false){
            document.getElementById("pose_palm").classList.remove("pose_highlight");
            document.getElementById("pose_rock").classList.remove("pose_highlight");
            document.getElementById("pose_gun").classList.remove("pose_highlight");
            document.getElementById("pose_three").classList.add("pose_highlight");
            document.getElementById("pose_peace").classList.remove("pose_highlight");
            document.getElementById("pose_dang").classList.remove("pose_highlight");
            document.getElementById("pose_one").classList.remove("pose_highlight");
          }
          break;
        case "Peace":
          if(document.getElementById("pose_peace").classList.contains('pose_highlight')==false){
            document.getElementById("pose_palm").classList.remove("pose_highlight");
            document.getElementById("pose_rock").classList.remove("pose_highlight");
            document.getElementById("pose_gun").classList.remove("pose_highlight");
            document.getElementById("pose_three").classList.remove("pose_highlight");
            document.getElementById("pose_peace").classList.add("pose_highlight");
            document.getElementById("pose_dang").classList.remove("pose_highlight");
            document.getElementById("pose_one").classList.remove("pose_highlight");
          }
          break;
        case "Dang":
          if(document.getElementById("pose_dang").classList.contains('pose_highlight')==false){
            document.getElementById("pose_palm").classList.remove("pose_highlight");
            document.getElementById("pose_rock").classList.remove("pose_highlight");
            document.getElementById("pose_gun").classList.remove("pose_highlight");
            document.getElementById("pose_three").classList.remove("pose_highlight");
            document.getElementById("pose_peace").classList.remove("pose_highlight");
            document.getElementById("pose_dang").classList.add("pose_highlight");
            document.getElementById("pose_one").classList.remove("pose_highlight");
          }
          break;
        case "One":
          if(document.getElementById("pose_one").classList.contains('pose_highlight')==false){
            document.getElementById("pose_palm").classList.remove("pose_highlight");
            document.getElementById("pose_rock").classList.remove("pose_highlight");
            document.getElementById("pose_gun").classList.remove("pose_highlight");
            document.getElementById("pose_three").classList.remove("pose_highlight");
            document.getElementById("pose_peace").classList.remove("pose_highlight");
            document.getElementById("pose_dang").classList.remove("pose_highlight");
            document.getElementById("pose_one").classList.add("pose_highlight");
          }
          break;
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

    function end_ok(){
      eel.py_sysclose();
      window.close();
    }

    function end_no(){
      window.close();
    }

    eel.expose(focusSwitch);
    function focusSwitch(width, height, focus_flg){
      //const headIndex = document.getElementById("headIndex");
      //const endIndex = document.getElementById("endIndex");
      //const focusEnd = document.getElementById("focusEnd");
      //const poseGuage = document.getElementById("poseGuage");

      if(focus_flg == 1){
        window.resizeTo(400, 200)
        window.moveTo(width, height)
        console.log("focus_flg is 1");
      }else{
        //headIndex.style.visibility ="visible";
        window.resizeTo(1025,775)
        window.moveTo(width/4, height/4)
        console.log("focus_flg is 0");
      }
    }
