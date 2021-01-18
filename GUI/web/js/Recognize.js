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
      document.getElementById("pose_text").innerHTML = name_pose + "取得";
      document.getElementById("pose_palm").classList.remove("pose_highlight");
      document.getElementById("pose_rock").classList.remove("pose_highlight");
      document.getElementById("pose_gun").classList.remove("pose_highlight");
      document.getElementById("pose_three").classList.remove("pose_highlight");
      document.getElementById("pose_peace").classList.remove("pose_highlight");
      document.getElementById("pose_dang").classList.remove("pose_highlight");
      document.getElementById("pose_one").classList.remove("pose_highlight");
      switch(name_pose){
        case "Palm":
          document.getElementById("pose_palm").classList.add("pose_highlight");
          break;
        case "Rock":
          document.getElementById("pose_rock").classList.add("pose_highlight");
          break;
        case "Gun":
          document.getElementById("pose_gun").classList.add("pose_highlight");
          break;
        case "Three":
          document.getElementById("pose_three").classList.add("pose_highlight");
          break;
        case "Peace":
          document.getElementById("pose_peace").classList.add("pose_highlight");
          break;
        case "Dang":
          document.getElementById("pose_dang").classList.add("pose_highlight");
          break;
        case "One":
          document.getElementById("pose_one").classList.add("pose_highlight");
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
        window.resizeTo(500, 150)
        window.moveTo(width, height)
        console.log("focus_flg is 1");
      }else{
        //headIndex.style.visibility ="visible";
        window.resizeTo(800,450)
        window.moveTo(width/4, height/4)
        console.log("focus_flg is 0");
      }
    }
