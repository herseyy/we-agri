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
async function getUser(){
  fetch('/user/{username}', {
    method: 'GET',
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    },
    body: JSON.stringify(inp_obj)
  })
  .then(res => {
    return res.json()
  })  
  .then(data => {
    const userData = document.getElementById('userData');
    /* const  */
    userData.innerHTML = "";
  
      let userDisplay = data.map((object)=> {
          const {username, birthday, province, city, /* is_active, is_public */} = object;
  
          return `
          <h2 id="usernameProfile">@ ${username}</h2>
          <div class="data">
              <table class="table" >
                  <tbody>
                      <tr>
                          <td>Name:</td>
                          <td id="fullname">"first_name" + "last_name"</td>
                      </tr>
                      <tr>
                          <td>Birthday:</td>
                          <td id="bday">${birthday}</td>
                      </tr>
                      <tr>
                          <td>Location:</td>
                          <td id="locationOutput">${city}, ${province}</td>
                      </tr>
                  </tbody>
              </table>
          </div>`;
          
      })/* .catch(error => console.log("ERROR")) */
  
      userData.innerHTML = userDisplay;
      
  });
};
getUser();



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
      console.log(data)

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

      var firstname = document.getElementById("firstname")
      firstname.value = data.firstname
      var lastname = document.getElementById("lastname")
      lastname.value = data.lastname
      var birthdate = document.getElementById("birthdate")
      birthdate.value = data.birthdate
      var location_details = document.getElementById("location-details")
      location_details.innerHTML = `${data.city},${data.state},${data.country}`

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
      birthdate.value = data.birthdate
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
    window.location.href = '../profile';
  })
  .catch(error => console.log("ERROR")) 


}

// function update_user_info(){

// }
  // fetch("/")
  //   .then(response => response.json())
  //   .then(data => {
  //   console.log(data)
  //   if (data['detail']){
  //     window.location.href = '../login';
  //   }
  //   else {
  //     window.location.href = '../profile';
  //   }
  //   }).catch((error) => {
  //       console.error('Error:', error);
  //     });