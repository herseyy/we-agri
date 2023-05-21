const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
});

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
  var msg = document.getElementById("msg_s")
  switch (error.code) {
    case error.PERMISSION_DENIED:
      console.log("lol")
      msg.innerHTML = "Please allow access to location"
      msg.style.visibility = "visible"
      msg.style.width = "100%"
      msg.setAttribute('class', 'alert alert-danger');
      // locationDiv.innerText = "Please allow access to location";
      break;
    case error.POSITION_UNAVAILABLE:
      msg.innerHTML = "Location Information unavailable"
      msg.style.visibility = "visible"
      msg.style.width = "100%"
      msg.setAttribute('class', 'alert alert-danger');
      //usually fired for firefox
      // locationDiv.innerText = "Location Information unavailable";
      break;
    case error.TIMEOUT:
      msg.innerHTML = "The request to get user location timed out"
      msg.style.visibility = "visible"
      msg.style.width = "100%"
      msg.setAttribute('class', 'alert alert-danger');
      // locationDiv.innerText = "The request to get user location timed out";
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



function btn_login(){
  var username = document.getElementById("username_l").value;
  var password = document.getElementById("password_l").value;

  var msg = document.getElementById("msg_l")

  if (username == ""){
    msg.innerHTML = "Username cannot be empty"
    msg.style.visibility = "visible"
    msg.style.width = "100%"
    msg.setAttribute('class', 'alert alert-danger');
    return 0
  }
  if (password == ""){
    msg.innerHTML = "Password cannot be empty"
    msg.style.visibility = "visible"
    msg.style.width = "100%"
    msg.setAttribute('class', 'alert alert-danger');
    return 0
  }

  var inp_obj = {
    "username" : username,
    "password" : password
  }

  fetch('/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(inp_obj)
  })
    .then(res => res.json())
    .then(data => {
      // console.log(data)
      if (data['detail']) {
        msg.innerHTML = data['detail']
        msg.style.visibility = "visible"
        msg.style.width = "100%"
        msg.setAttribute('class', 'alert alert-danger');
      }
      else {
        msg.innerHTML = "Success"
        msg.style.visibility = "visible"
        msg.style.width = "100%"
        msg.setAttribute('class', 'alert alert-success');
        window.location.href = '../profile';
      }
    }).catch((error) => {
      // console.error('Error:', error);
    });
}


function btn_signin() {
  var username = document.getElementById("username_s").value
  var password = document.getElementById("password_s").value
  var password1 = document.getElementById("password_s1").value
  var loc = locationDiv.innerHTML

  var msg = document.getElementById("msg_s")


  if (username == "") {
    msg.innerHTML = "Username cannot be empty"
    msg.style.visibility = "visible"
    msg.style.width = "100%"
    msg.setAttribute('class', 'alert alert-danger');
    return 0
  }
  if (password == "") {
    msg.innerHTML = "Enter your password"
    msg.style.visibility = "visible"
    msg.style.width = "100%"
    msg.setAttribute('class', 'alert alert-danger');
    return 0
  }
  if (password.length < 5) {
    msg.innerHTML = "Password too short"
    msg.style.visibility = "visible"
    msg.style.width = "100%"
    msg.setAttribute('class', 'alert alert-danger');
    return 0
  }
  if (password != password1) {
    msg.innerHTML = "Password don't match"
    msg.style.visibility = "visible"
    msg.style.width = "100%"
    msg.setAttribute('class', 'alert alert-danger');
    return 0
  }
  if (loc == "") {
    msg.innerHTML = "Location cannot be empty"
    msg.style.visibility = "visible"
    msg.style.width = "100%"
    msg.setAttribute('class', 'alert alert-danger');
    return 0
  }

  // console.log("aa")
  locc = loc.split(",")
  // console.log(loc.split(","))
  city = locc[0]
  state = locc[1]
  country = locc[2]
  // console.log(city, state, country)
  var inp_obj = {
    "username": username,
    "pass_to_hash": password,
    "country": country,
    "state": state,
    "city": city,
  }

  fetch('/create_user', {
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
        msg.innerHTML = data['detail']
        msg.style.visibility = "visible"
        msg.style.width = "100%"
        msg.setAttribute('class', 'alert alert-danger');
      }
      else {
        msg.innerHTML = "Success"
        msg.style.visibility = "visible"
        msg.style.width = "100%"
        msg.setAttribute('class', 'alert alert-success');

        document.getElementById("username_s").value =
        document.getElementById("password_s").value =
        document.getElementById("password_s1").value = 
        locationDiv.innerHTML = ""
        document.getElementById("get-location").style.display = "inline-block";
      }
    }).catch((error) => {
      // console.error('Error:', error);
    });
}