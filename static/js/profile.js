let locationButton = document.getElementById("get-location");
let locationDiv = document.getElementById("location-details");

locationButton.addEventListener("click", () => {
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
  let response = await fetch(
    `https://nominatim.openstreetmap.org/reverse?lat=${position.coords.latitude}&lon=${position.coords.longitude}&format=json`
  );
  //store response object
  let data = await response.json();
  locationDiv.innerText = `${data.address.city}, ${data.address.country}`;
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
}



//edit profile
const changepass_url = "http://127.0.0.1:8000/change_pass";

async function changepass(){
  $("#changepassModal").find("button[name=passwordupdate]").on("click", function() {
    const user_update_url = "/update/" + id
    console.log(user_update_url)

    let newPass = document.getElementById('newPass').value;
    let newPassConfirm = document.getElementById('newPassConfirm').value;

    var inp_obj = {}

    
    if (newPass != "") {
      inp_obj = Object.assign({"new_pass1": new_password}, inp_obj)
    }
    if (newPassConfirm != "") {
      inp_obj = Object.assign({"new_pass2": newPassConfirm}, inp_obj)
    } 
    console.log(inp_obj)

    fetch('/change_pass', {
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
    location.href = "/update_user";
  });
};
