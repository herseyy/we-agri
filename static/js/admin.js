 (function() {
    "use strict";

    const select = (el, all = false) => {
      el = el.trim()
      if (all) {
        return [...document.querySelectorAll(el)]
      } else {
        return document.querySelector(el)
      }
    }

    const on = (type, el, listener, all = false) => {
      if (all) {
        select(el, all).forEach(e => e.addEventListener(type, listener))
      } else {
        select(el, all).addEventListener(type, listener)
      }
    }

    if (select('.toggle-sidebar-btn')) {
      on('click', '.toggle-sidebar-btn', function(e) {
        select('body').classList.toggle('toggle-sidebar')
      })
    }

}) ();


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
    var minptime = document.getElementById('inputminp_time').value;
    var maxptime = document.getElementById('inputmaxp_time').value;

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
    if(minptime == ""){
        errormsg.innerHTML= "Enter maximum rain tolerance"
    }
    if(maxptime == ""){
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
        "min_planting_time": minptime,
        "max_planting_time": maxptime,
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
            minptime = ""; 
            maxptime = ""; 
          }
        }).catch((error) => {
          // console.error('Error:', error);
        });
    
}

//users
const user_url = 'http://127.0.0.1:8000/filter_users';


function getallusers(){
  
  let q = document.getElementById('q').value;
  let upperAge = document.getElementById('upperAge').value;
  let lowerAge = document.getElementById('lowerAge').value;
  let country = document.getElementById('country').value;
  let state = document.getElementById('state').value;
  let city = document.getElementById('city').value;
  let isactive = document.getElementById('isactive').value;
  let ispublic = document.getElementById('ispublic').value;

  var inp_obj = {}
    
  if (q != ""){
      inp_obj = Object.assign({"q":q}, inp_obj)
  }
  if (upperAge != ""){
      inp_obj = Object.assign({"upperAge":upperAge}, inp_obj)
  }
  if (lowerAge != ""){
      inp_obj = Object.assign({"lowerAge":lowerAge}, inp_obj)
  }
  if (country != ""){
      inp_obj = Object.assign({"country":country}, inp_obj)
  }
  if (state != ""){
      inp_obj = Object.assign({"state":state}, inp_obj)
  }
  if (city != ""){
      inp_obj = Object.assign({"city":city}, inp_obj)
  }
  if (isactive != ""){
      inp_obj = Object.assign({"is_active":isactive}, inp_obj)
  }
  if (ispublic != ""){
      inp_obj = Object.assign({"is_public":ispublic}, inp_obj)
  }
  
  console.log(inp_obj)

  let query = Object.keys(inp_obj)
    .map(k =>encodeURIComponent(k) + '=' + encodeURIComponent(inp_obj[k]))
    .join('&');
    
        const filterusers_url = "http://127.0.0.1:8000/filter_users?" + query
        console.log(filterusers_url)

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
                <td id="plantcol">${plants}</td>
                <td>
                    <button class="btn" id="editbtn" onclick="updateuser()">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn" id="deletebtn" onclick="deleteuser()">
                        <i class="fa-sharp fa-solid fa-trash"></i>
                    </button>
                </td>
              </tr>`;
            
        })/* .catch(error => console.log("ERROR")) */;
        
        usersTable.innerHTML = userDisplay;
    })
    
};/* 
getallusers(); */



//plant filter 

function getPlants(){

  let fruit = "";
  let vegetable = ""; 
  let summer = "";
  let rainy = "";
  let ptime_range = document.getElementById('p_time').value;
  var split = ptime_range.split(',');

  for (i in checkbox()){
      // console.log(checkbox()[i])
      if (checkbox()[i] == "catFruit") {
          fruit = "fruit"
          // console.log(checkbox()[i])
      }
      if (checkbox()[i] == "catVeggie") {
          vegetable = "vegetable"
          // console.log(checkbox()[i])
      }
      if (checkbox()[i] == "summerTrue") {
          summer = true
          // console.log(checkbox()[i])
      }
      if (checkbox()[i] == "rainyTrue") {
          rainy = true
          // console.log(checkbox()[i])
      }
  }


  var inp_obj = {}
  
  if (psearch != ""){
      inp_obj = Object.assign({"name":psearch}, inp_obj)
  }
  if (ptime_range != ""){
      inp_obj = Object.assign({"upper_p_time":split[1]}, inp_obj)
  }
  if (ptime_range != ""){
      inp_obj = Object.assign({"lower_p_time":split[0]}, inp_obj)
  }
  if (rainy != ""){
      inp_obj = Object.assign({"rainy_season":rainy}, inp_obj)
  }
  if (summer != ""){
      inp_obj = Object.assign({"summer":summer}, inp_obj)
  }
  if (fruit && vegetable){
      // both checked ang category
  }
  else{
      if(fruit != ""){
          inp_obj = Object.assign({"category":fruit}, inp_obj)
      }
      if(vegetable != ""){
          inp_obj = Object.assign({"category":vegetable}, inp_obj)
      }
  };

  // console.log(allPlants_url)
  
  let query = Object.keys(inp_obj)
      .map(k =>encodeURIComponent(k) + '=' + encodeURIComponent(inp_obj[k]))
      .join('&');
  
      const filter_url = "http://127.0.0.1:8000/filter_plants?" + query
      console.log(filter_url)

  // console.log(inp_obj)
  
  fetch(filter_url)
  .then(res => {
      return res.json()
    })
  
  .then(data =>{
    getallusers();
      // console.log(data)
      const plantcol = document.getElementById("plantcol"); 
      plantcol.innerHTML='';

      let plantDisplay = data.map((object)=> {
          const {name, category/* , min_temp, max_temp, min_humidity, max_humidity, min_rain_tolerance, max_rain_tolerance, min_planting_time, max_planting_time, rainy_season, summer, p_info */} = object;
          
          

          /* return */ `
            <div class="plants"> [$ {name}, $ {category}]</div>`
          
      })/* .catch(error => console.log("ERROR")) */;

      document.getElementById('catFruit').value = "";
      document.getElementById('catVeggie').value = "";
      document.getElementById('summerTrue').value = "";
      document.getElementById('rainyTrue').value = "";

      /* plantcol.innerHTML = plantDisplay; */
      
  }) 
};
/* getPlants(); */


// update user
function updateuser(){

};


//delete user 
function deleteuser(){

  /* let pass_ = document.getElementById('pass_').value;
  var msgdelete = document.getElementById('msgdelete');


  if (pass_ == ""){
    msgdelete.innerHTML="Enter pass_ to delete";
  }

  var inp_obj = {
    "pass_":pass_,
  }

  fetch("/delete_user",{
    method: 'DELETE',
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    },
    body: JSON.stringify(inp_obj)
  })
  .then(res => res.json())
  .then(data => {
    console.log(data)
    msgdelete.innerHTML = data["status"]
    msgdelete.style.display = "inline-block"
    msgdelete.style.width = "100%"
    if (data["status"] == "success"){
      // console.log(data["status"])
      msgdelete.setAttribute('class', 'alert alert-success');
      document.getElementById("pass_").value = "";
    } else {
      msg.setAttribute('class', 'alert alert-danger');
    }

  })
  .catch(error => console.log("ERROR")) ; */
};