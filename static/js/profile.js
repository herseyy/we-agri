let locationButton = document.getElementById("get-location");
let locationDiv = document.getElementById("location-details");


locationButton.addEventListener("click", () => {
  console.log("get loc")
  //Geolocation APU is used to get geographical position of a user and is available inside the navigator object
  if (navigator.geolocation) {
    //returns position(latitude and longitude) or error
    navigator.geolocation.getCurrentPosition(showLocation, checkError);
  } else {
    //For old browser i.e IE
    locationDiv.innerText = "The browser does not support geolocation";
  }
});


//Error Checks
const checkError = (error) => {
  switch (error.code) {
    case error.PERMISSION_DENIED:
      locationDiv.innerText = "Please allow access to location";
      break;
    case error.POSITION_UNAVAILABLE:
      //usually fired for firefox
      locationDiv.innerText = "Location Information unavailable";
      break;
    case error.TIMEOUT:
      locationDiv.innerText = "The request to get user location timed out";
  }
};
const showLocation = async (position) => {
  //We user the NOminatim API for getting actual addres from latitude and longitude
  document.getElementById("get-location").style.display = "none";
  var api_key = "2aefe52a593c0d988f240092f4dfa3c6" 
  var data_url = `http://api.openweathermap.org/geo/1.0/reverse?lat=${position.coords.latitude}&lon=${position.coords.longitude}&limit=1&appid=${api_key}`;

  fetch(data_url)
    .then(response => {
      return response.json();
    })
    .then(data => {
      console.log(data[0])
      locationDiv.innerText = `${data[0].name}, ${data[0].state}, ${data[0].country}`;
    })
};


function clickProfile(){
  document.getElementById('my_plants').style.display='none';
  document.getElementById('profile').style.display='block';
}

function clickMyPlants(){
  document.getElementById('profile').style.display='none';
  document.getElementById('my_plants').style.display='block';
}

//show profile
// async function getUser(){
//   fetch('/user/{username}', {
//     method: 'GET',
//     headers: {
//       'Content-type': 'application/json; charset=UTF-8'
//     },
//     body: JSON.stringify(inp_obj)
//   })
//   .then(res => {
//     return res.json()
//   })  
//   .then(data => {
//     const userData = document.getElementById('userData');
//     /* const  */
//     userData.innerHTML = "";
  
//       let userDisplay = data.map((object)=> {
//           const {username, birthday, province, city, /* is_active, is_public */} = object;
  
//           return `
//           <h2 id="usernameProfile">@ ${username}</h2>
//           <div class="data">
//               <table class="table" >
//                   <tbody>
//                       <tr>
//                           <td>Name:</td>
//                           <td id="fullname">"first_name" + "last_name"</td>
//                       </tr>
//                       <tr>
//                           <td>Birthday:</td>
//                           <td id="bday">${birthday}</td>
//                       </tr>
//                       <tr>
//                           <td>Location:</td>
//                           <td id="locationOutput">${city}, ${province}</td>
//                       </tr>
//                   </tbody>
//               </table>
//           </div>`;
          
//       })/* .catch(error => console.log("ERROR")) */
  
//       userData.innerHTML = userDisplay;
      
//   });
// };
// getUser();



//edit profile
// const changepass_url = "http://127.0.0.1:8000/change_pass";

// async function changepass(){
//   $("#changepassModal").find("button[name=passwordupdate]").on("click", function() {
//     const user_update_url = "/update/" + id
//     console.log(user_update_url)

//     let newPass = document.getElementById('newPass').value;
//     let newPassConfirm = document.getElementById('newPassConfirm').value;

//     var inp_obj = {}

    
//     if (newPass != "") {
//       inp_obj = Object.assign({"new_pass1": new_password}, inp_obj)
//     }
//     if (newPassConfirm != "") {
//       inp_obj = Object.assign({"new_pass2": newPassConfirm}, inp_obj)
//     } 
//     console.log(inp_obj)

//     fetch('/change_pass', {
//       method: 'PATCH',
//       headers: {
//         'Content-type': 'application/json; charset=UTF-8'
//       },
//       body: JSON.stringify(inp_obj)
//     })
//     .then(res => res.json())
//     .then(data => {
//       console.log(data)
//     })
//     .catch(error => console.log("ERROR")) 
//     location.href = "/update_user";
//   });
// };

function changepass() {
  // fetch("/")
  old_pass = document.getElementById("oldPass").value
  new_pass = document.getElementById("newPass").value
  c_new_pass = document.getElementById("newPassConfirm").value

  msg = document.getElementById("msg")


  console.log(old_pass)
  console.log(new_pass)
  console.log(c_new_pass)

  inp_obj = {
    "old_pass": old_pass,
    "new_pass1": new_pass,
    "new_pass2": c_new_pass
  }

  fetch("/change_pass", {
    method: 'PATCH',
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    },
    body: JSON.stringify(inp_obj)
  })
  .then(res => res.json())
  .then(data => {
    console.log(data)
    msg.innerHTML = data["status"]
    msg.style.display = "inline-block"
    msg.style.width = "100%"
    if (data["status"] == "success"){
      // console.log(data["status"])
      msg.setAttribute('class', 'alert alert-success');
      document.getElementById("oldPass").value = "";
      document.getElementById("newPass").value = "";
      document.getElementById("newPassConfirm").value = "";
    } else {
      msg.setAttribute('class', 'alert alert-danger');
    }
    // window.location.href = '../profile';


  })
  .catch(error => console.log("ERROR")) 
}


function close_pass() {
  msg = document.getElementById("msg").style.display = "none"
  document.getElementById("oldPass").value = "";
  document.getElementById("newPass").value = "";
  document.getElementById("newPassConfirm").value = "";
}


function get_current_user(){

  fetch("/user")
    .then(response => response.json())
    .then(data => {
      // console.log(data)

      var profile_info = document.getElementById("profile_info")
      profile_info.innerHTML = ""

      let display_user_info = `
        <h2 id="usernameProfile">@ ${data.username}</h2>
        <div class="data">
            <table class="table" >
                <tbody>
                    <tr>
                        <td>Name:</td>
                        <td id="fullname">${data.firstname} ${data.lastname}</td>
                    </tr>
                    <tr>
                        <td>Birthday:</td>
                        <td id="bday">${data.birthday}</td>
                    </tr>
                    <tr>
                        <td>Location:</td>
                        <td id="locationOutput">${data.city}, ${data.state}, ${data.country}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        `
      profile_info.innerHTML = display_user_info;
      msg = document.getElementById("msg_q").style.display = "none"

    }).catch((error) => {
      console.error("Error:", error);
    })
}

get_current_user()


function editBtn(){

  document.getElementById("get-location").style.display = "inline-block";

  fetch("/user")
    .then(response => response.json())
    .then(data => {
      console.log(data)

      var firstname = document.getElementById("firstname")
      firstname.value = data.firstname
      var lastname = document.getElementById("lastname")
      lastname.value = data.lastname
      var birthdate = document.getElementById("birthdate")
      birthdate.value = data.birthday
      var location_details = document.getElementById("location-details")
      location_details.innerHTML = `${data.city}, ${data.state}, ${data.country}`

    }).catch((error) => {
      console.error("Error:", error);
    })
}

function update_user_info(){
  var firstname = document.getElementById("firstname").value
  var lastname = document.getElementById("lastname").value
  var birthdate = document.getElementById("birthdate").value
  var loc = document.getElementById("location-details").innerHTML

  locc = loc.split(",")
  city = locc[0].trim()
  state = locc[1].trim()
  country = locc[2].trim()

  if (birthdate == ""){
    birthdate = null
  }


  // console.log(birthdate)
  inp_obj = {
    "firstname": firstname,
    "lastname": lastname,
    "birthday": birthdate,
    "country": country,
    "state": state,
    "city": city,
    "is_public": true,
  }

  fetch("/update_user", {
    method: 'PATCH',
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    },
    body: JSON.stringify(inp_obj)
  })
  .then(res => res.json())
  .then(data => {
    console.log(data)
    msg = document.getElementById("msg_q")
    msg.innerHTML = "Success"
    msg.style.display = "inline-block"
    msg.style.width = "100%"
    msg.setAttribute('class', 'alert alert-success');
    // window.location.href = '../profile';
  })
  .catch(error => console.log("ERROR")) 
}


function get_current_user_plants() {

  var cat = document.getElementById("userplantfiltercat").value
  var is_harvested = document.getElementById("userplantfilteri_h").value

  // console.log(cat)
  // console.log(is_harvested)

  inp_obj = {}

  if (cat != "") {
    inp_obj = Object.assign({"category": cat}, inp_obj)
  }

  if (is_harvested != ""){
        inp_obj = Object.assign({"is_harvested":is_harvested}, inp_obj)
    }

  let query = Object.keys(inp_obj)
               .map(k => encodeURIComponent(k) + '=' + encodeURIComponent(inp_obj[k]))
               .join('&');


  const filter_url = "/user/plants/filter?" + query

  // console.log(filter_url)
  

  fetch(filter_url)
  .then(response => response.json())
  .then(data => {
    // console.log(data)

    parent = document.getElementById('myPlantsTable')
    parent.innerHTML = ""
    document.getElementById("spn_plnts").innerHTML = data.length
    i = 0
    j = 0
    k = 0
    l = 0

    let today = new Date().toISOString().slice(0, 10)

    // console.log(today)

    let plantDisplay = data.map((object)=> {
      // console.log(object)
      i ++
      status = ''

      if (object.is_harvested == false) {      
        if (today < object.min_date_estimate_harvest) {
          j ++
          status = "not yet"
          var btn_ = `<button onclick="btn_click(this.id)" id="${object.id}" class="btn disabled">${status}</button>`
        }
        else if (today >= object.min_date_estimate_harvest && today <= object.max_date_estimate_harvest) {
          k ++
          status = "ready"
          // console.log("ready")

          // dapat blue itoooooo
          var btn_ = `<button onclick="btn_click(this.id)" id="${object.id}" class="btn btn-primary">${status}</button>`
        }
        else if (today > object.max_date_estimate_harvest) {

          inp_obj = {
            "is_harvested": true,
            "date_harvested": object.max_date_estimate_harvest
          }

          fetch(`/update_user_plant/${object.id}`, {
            method: 'PATCH',
            headers: {
              'Content-type': 'application/json; charset=UTF-8'
            },
            body: JSON.stringify(inp_obj)
          })
          .then(res => res.json())
          .then(data => {
            console.log(data)

          })
          .catch(error => console.log("ERROR"))
          get_current_user_plants()

          status = "harvested"
          l ++
          var btn_ = `<button onclick="btn_click(this.id)" id="${object.id}" class="btn btn-success">${status}</button>`
        }
      }
      else {
        status = "harvested"
        l ++
        var btn_ = `<button onclick="btn_click(this.id)" id="${object.id}" class="btn btn-success">${status}</button>`
      }



      // console.log(object)
      return `
              <tr>
                <td>${i}</td>
                <td>${object.name}</td>
                <td>${object.category}</td>
                <td>${btn_}</td>
                <td>${object.date_planted}</td>
                <td> ${object.min_date_estimate_harvest
                  } - ${object.max_date_estimate_harvest
                  }</td>
                <td>${object.date_harvested}</td>
              </tr>
            `
    })
    parent.innerHTML = plantDisplay;
    // document.getElementById("")
  })
  .catch((error) => {
      console.error('Error:', error);
    });
}

get_current_user_plants()


function btn_click(clicked_id) {
  // console.log(document.getElementById(clicked_id).innerHTML)
  btn_innerhtml = document.getElementById(clicked_id).innerHTML
  if (btn_innerhtml == "harvested") {
    console.log("already harvested")
  }
  else if (btn_innerhtml == "ready") {
    let today = new Date().toISOString().slice(0, 10)

    // console.log(today)
    inp_obj = {
      "is_harvested": true,
      "date_harvested": today
    }

    update_url = `/update_user_plant/${clicked_id}`


    fetch(update_url, {
      method: 'PATCH',
      headers: {
        'Content-type': 'application/json; charset=UTF-8'
      },
      body: JSON.stringify(inp_obj)
    })
    .then(res => res.json())
    .then(data => {
      console.log(data)

    })
    .catch(error => console.log("ERROR"))
    get_current_user_plants()
    // document.getElementById(clicked_id).innerHTML = "aaa"
    // console.log(document.getElementById(clicked_id).innerHTML)
    // btn_innerhtml = "Harvested"
    // console.log("lol")
    // document.getElementById(clicked_id).setAttribute('class', 'btn btn-success');
  }
}

function add_plant() {
  id = document.querySelector('input[name="plant"]:checked').id;
  cat = document.getElementById('addCat').value
  date = document.getElementById("addDatePlanted").value

  inp_obj = {
    "is_harvested": false,
    "date_planted": date
  }
  console.log(id)
  fetch(`/add_user_plant/${id}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(inp_obj)
  })
    .then(res => res.json())
    .then(data => {
      console.log(data)

    }).catch((error) => {
      console.error('Error:', error);
    });
  document.getElementById("msg_add").innerHTML = "success"
  let today = new Date().toISOString().slice(0, 10)
  document.getElementById('addCat').value = ""
  document.getElementById("addDatePlanted").value = today
  document.querySelector('input[name="plant"]:checked').checked = false;
}



function fetch_plants() {


  plants_url = "/filter_plants?"

  fetch(plants_url)
    .then(response => {
      return response.json();
    })
    .then(data => {
      console.log(data)

      const checklist = document.getElementById("checklist");
      checklist.innerHTML='';

      let plantDisplay = data.map((object)=> {

        console.log(object)
        return `<input type="radio" id="${object.id}" name="plant" value="${object.name}">
                <label for="${object.id}">${object.name}</label><br>`
// <input type="radio" id="html" name="fav_language" value="HTML">
//   <label for="html">HTML</label><br>
//   <input type="radio" id="css" name="fav_language" value="CSS">
//   <label for="css">CSS</label><br>
//   <input type="radio" id="javascript" name="fav_language" value="JavaScript">
//   <label for="javascript">JavaScript</label>
      })
      checklist.innerHTML = plantDisplay;
      let today = new Date().toISOString().slice(0, 10)

      document.getElementById('addDatePlanted').value = today
      document.getElementById("addCat").value = ""

    })
}


function listQ(){
  console.log(this.value)
  cat = this.value
  inp_obj = {}

  if (cat != ""){
    inp_obj = Object.assign({"category":cat}, inp_obj)
  }

  let query = Object.keys(inp_obj)
    .map(k =>encodeURIComponent(k) + '=' + encodeURIComponent(inp_obj[k]))
    .join('&');
  plants_url = "/filter_plants?" + query 

  fetch(plants_url)
  .then(response => {
    return response.json();
  })
  .then(data => {
   console.log(data)

    const checklist = document.getElementById("checklist");
    checklist.innerHTML='';

    let plantDisplay = data.map((object)=> {

      console.log(object)
      return `<input type="radio" id="${object.id}" name="plant" value="${object.name}">
              <label for="${object.id}">${object.name}</label><br>`

    })
    checklist.innerHTML = plantDisplay;
  })
}
document.getElementById("addCat").onchange = listQ;



// remove cookies
function logout() {
  fetch("/logout", {
    method: 'DELETE',
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    },
    body: JSON.stringify(inp_obj)
  })
  .then(res => res.json())
  .then(data => {
    console.log(data)
    window.location.href = '../login';
  })
  .catch(error => console.log("ERROR")) 
}