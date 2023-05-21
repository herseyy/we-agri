(function() {
    "use strict";
 /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

})

/* hide other sections  */

function openforms(){
    document.getElementById('forms').style.display='block';
    document.getElementById('users').style.display='none';
};

function openusers(){
    document.getElementById('users').style.display='block';
    document.getElementById('forms').style.display='none';
};

// forms
function checkbox() {
    var checkboxes = document.getElementsByName("checkbox");
    let checked_filter = [];
    for (var checkbox of checkboxes) {
        if (checkbox.checked) {
            // console.log(checkbox.id)
            checked_filter.push(checkbox.id);
            checked_filter.sort();
        }
    }
    // console.log(checked_filter)

    return checked_filter
}

function createPlants(){
    var errormsg = document.getElementById('errormsg');

    let inpsummer = "";
    let inprain = "";
    var pname = document.getElementById('inputName').value;
    var cat = document.getElementById('inputCat').value;
    var pinfo = document.getElementById('inputpinfo').value;
    var mintemp = document.getElementById('inputmin_temp').value;
    var maxtemp = document.getElementById('inputmax_temp').value;
    var minhum = document.getElementById('inputmin_hum').value;
    var maxhum = document.getElementById('inputmax_hum').value;
    var minraintol = document.getElementById('inputmin_raintol').value;
    var maxraintol = document.getElementById('inputmax_raintol').value;
    var ptime = document.getElementById('inputp_time').value;

    for (i in checkbox()){
        if (checkbox()[i] == "inputsummer") {
            inpsummer = true
        }
        if (checkbox()[i] == "inputrain") {
            inprain = true
        }
    }

    if(pname == ""){
        errormsg.innerHTML= "Enter a name"
    }
    if(mintemp == ""){
        errormsg.innerHTML= "Enter minimum temperature"
    }
    if(maxtemp == ""){
        errormsg.innerHTML= "Enter maximum temperature"
    }
    if(minhum == ""){
        errormsg.innerHTML= "Enter minimum humidity"
    }
    if(maxhum == ""){
        errormsg.innerHTML= "Enter maximum humidity"
    }
    if(minraintol == ""){
        errormsg.innerHTML= "Enter minimum rain tolerance"
    }
    if(maxraintol == ""){
        errormsg.innerHTML= "Enter maximum rain tolerance"
    }

    var inp_obj = {
        "name": pname,
        "category": cat,
        "p_info": pinfo,
        "min_temp": mintemp,
        "max_temp": maxtemp,
        "min_humidity": minhum,
        "max_humidity": maxhum,
        "min_rain_tolerance": minraintol,
        "max_rain_tolerance": maxraintol,
        "p_time": ptime,
        "summer": inpsummer,
        "rainy_season": inprain,
      };

      fetch('/create_plant', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(inp_obj)
      })
        .then(res => res.json())
        .then(data => {
          console.log(data)
          if (data['detail']) {
            errormsg.innerHTML = data['detail']
            errormsg.style.visibility = "visible"
            errormsg.style.width = "100%"
            errormsg.setAttribute('class', 'alert alert-danger');
          }
          else {
            errormsg.innerHTML = "Success"
            errormsg.style.visibility = "visible"
            errormsg.style.width = "100%"
            errormsg.setAttribute('class', 'alert alert-success');
    
            pname = ""; 
            cat = ""; 
            pinfo = ""; 
            mintemp = ""; 
            maxtemp = ""; 
            minhum = ""; 
            maxhum = ""; 
            minraintol = ""; 
            maxraintol = ""; 
            ptime = ""; 
          }
        }).catch((error) => {
          // console.error('Error:', error);
        });
    
}

//users
const user_url = 'http://127.0.0.1:8000/filter_users';

function getallusers(){
    fetch(user_url)
    .then(res => {
        return res.json()
      })
    
    .then(data =>{
        // console.log(data)
        const usersTable = document.getElementById("usersTable");
        usersTable.innerHTML='';

        let userDisplay = data.map((object)=> {
            const {id, username, birthday, country, state, city, is_active, is_public, plants} = object;
           
            return `
                <tr>
                <td>${id}</td>
                <td>${username}</td>
                <td>${birthday}</td>
                <td>${country}</td>
                <td>${state}</td>
                <td> ${city}</td>
                <td>${is_active}</td>
                <td>${is_public}</td>
                <td>${plants}</td>
                </tr>`;
            
        })/* .catch(error => console.log("ERROR")) */;
        
        usersTable.innerHTML = userDisplay;
    })
    
};
getallusers();