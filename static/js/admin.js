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


function check_token(){
fetch("/")
  .then(response => response.json())
  .then(data => {
  console.log(data)
  if (data['detail']){
    window.location.href = '../login';
  }
  else {
    window.location.href = '../profile';
  }
  }).catch((error) => {
      console.error('Error:', error);
    });
}


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



// function previewFile() {
//     const preview = document.querySelector('img');
//     const file = document.querySelector('input[type=file]').files[0];
//     const reader = new FileReader();
//     reader.addEventListener("load", function() {
//         preview.src = reader.result; // show image in <img> tag
//         uploadFile(file)
//     }, false);
//     if (file) {
//         reader.readAsDataURL(file);
//     }
// }

function uploadFile(name) {
  const file = document.querySelector('input[type=file]').files[0];
  var formData = new FormData();
  formData.append('file', file);
  fetch(`/upload/${name}`, {
          method: 'POST',
          body: formData,
      })
      .then(response => {
          console.log(response);
      })
      .catch(error => {
          console.error(error);
      });
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
        else {
          inpsummer = false
        }
        if (checkbox()[i] == "inputrain") {
            inprain = true
        }
        else {
          inprain = false
        }
    }

    if(maxptime == ""){
        errormsg.innerHTML= "Enter maximum planting time"
        errormsg.setAttribute("class", "col-12 alert alert-danger")
    }
    if(minptime == ""){
        errormsg.innerHTML= "Enter minimum planting time"
        errormsg.setAttribute("class", "col-12 alert alert-danger")
    }
    if(maxraintol == ""){
        errormsg.innerHTML= "Enter maximum rain tolerance"
        errormsg.setAttribute("class", "col-12 alert alert-danger")
    }
    if(mintemp == ""){
        errormsg.innerHTML= "Enter minimum temperature"
        errormsg.setAttribute("class", "col-12 alert alert-danger")
    }
    if(maxtemp == ""){
        errormsg.innerHTML= "Enter maximum temperature"
        errormsg.setAttribute("class", "col-12 alert alert-danger")
    }
    if(minhum == ""){
        errormsg.innerHTML= "Enter minimum humidity"
        errormsg.setAttribute("class", "col-12 alert alert-danger")
    }
    if(maxhum == ""){
        errormsg.innerHTML= "Enter maximum humidity"
        errormsg.setAttribute("class", "col-12 alert alert-danger")
    }
    if(minraintol == ""){
        errormsg.innerHTML= "Enter minimum rain tolerance"
        errormsg.setAttribute("class", "col-12 alert alert-danger")
    }
    if(pname == ""){
        errormsg.innerHTML= "Enter a name"
        errormsg.setAttribute("class", "col-12 alert alert-danger")
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

      uploadFile(pname)

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
            return 0
          }
          else {
            errormsg.innerHTML = "Success"
            errormsg.style.visibility = "visible"
            errormsg.style.width = "100%"
            errormsg.setAttribute('class', 'alert alert-success');


            window.location.href = '../admin';

          }
        }).catch((error) => {
          // console.error('Error:', error);
        });
    
}

//plants

const allPlants_url = "http://127.0.0.1:8000/filter_plants";

//plant filter 

function getPlants(){

  let fruit = "";
  let vegetable = "";
  let tree = "";
  let summer = "";
  let rainy = "";
  let psearch = document.getElementById('plantSearch').value;

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
      if (checkbox()[i] == "catTree") {
          tree = "tree"
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
  console.log(inp_obj)

  if (psearch != ""){
      inp_obj = Object.assign({"name":psearch}, inp_obj)
  }
  if (rainy != ""){
      inp_obj = Object.assign({"rainy_season":rainy}, inp_obj)
  }
  if (summer != ""){
      inp_obj = Object.assign({"summer":summer}, inp_obj)
  }
  if (fruit && vegetable && tree){
      // both checked ang category
  }
  else{
      if(fruit != ""){
          inp_obj = Object.assign({"category":fruit}, inp_obj)
      }
      if(vegetable != ""){
          inp_obj = Object.assign({"category":vegetable}, inp_obj)
      }
      if(tree != ""){
          inp_obj = Object.assign({"category":tree}, inp_obj)
      }
  };


  document.getElementById("plantSearch")
  .addEventListener("keyup", function(event) {
  event.preventDefault();
  if (event.key === 'Enter') {
      document.getElementById("searchBtn").click();
  }
});

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
    // console.log(data)
    const usersTable = document.getElementById("usersTable");
    usersTable.innerHTML='';
    i=0

    let userplantDisplay = data.map((object)=> {
        const {id, name, category, min_temp, max_temp, min_humidity, max_humidity, min_rain_tolerance, max_rain_tolerance, min_planting_time, max_planting_time, rainy_season, summer, p_info} = object;
        i++
        let printSeason;
            if (summer && rainy_season){
                printSeason = "Wet and Dry";
            } else if (summer && !rainy_season){
                printSeason = "Summer";
            }else if (!summer && rainy_season){
                printSeason = "Rainy";
            }else {
                printSeason = "Neither";
            }

        return `
          <tr>
            <td>${i}</td>
            <td>${name}</td>
            <td>${category}</td>
            <td>${p_info}</td>
            <td>${min_temp} - ${max_temp}</td>
            <td> ${min_humidity} - ${max_humidity}</td>
            <td>${min_rain_tolerance} - ${max_rain_tolerance}</td>
            <td>${min_planting_time} - ${max_planting_time}</td>
            <td>${printSeason}</td>
            <td>
                <button onclick="edit(${id})" class="btn" id="editbtn" data-bs-toggle="modal" data-bs-target="#editUserModal" >
                    <i class="fas fa-edit"></i>
                </button>
                <button onclick="delete_plant(${id})" class="btn" id="deletebtn" data-bs-toggle="modal" data-bs-target="#deleteuserModal">
                    <i class="fa-sharp fa-solid fa-trash"></i>
                </button>
            </td>
          </tr>`;
        
    }).join('')/* .catch(error => console.log("ERROR")) */;
    document.getElementById('catFruit').value = "";
    document.getElementById('catVeggie').value = "";
    document.getElementById('catTree').value = "";
    document.getElementById('summerTrue').value = "";
    document.getElementById('rainyTrue').value = "";

    usersTable.innerHTML = userplantDisplay;
    
}) 
};
getPlants();

// PLANT SEARCH
let autocomplete = (inp, arr) => {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  let currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
    let a, //OUTER html: variable for listed content with html-content
      b, // INNER html: filled with array-Data and html
      i, //Counter
      val = this.value;

    /*close any already open lists of autocompleted values*/
    closeAllLists();

    if (!val) {
      return false;
    }

    currentFocus = -1;

    /*create a DIV element that will contain the items (values):*/
    a = document.createElement("DIV");
    var parent_div = document.getElementById('plantsearchList');

    a.setAttribute("id", this.id + "autocomplete-list");
    a.setAttribute("class", "autocomplete-items list-group text-left");
    
    /*append the DIV element as a child of the autocomplete container:*/
    parent_div.appendChild(a);

    /*for each item in the array...*/
    for (i = 0; i < arr.length; i++) {
      /*check if the item starts with the same letters as the text field value:*/
      if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
        /*create a DIV element for each matching element:*/
        b = document.createElement("DIV");
        b.setAttribute("class", "list-group-item list-group-item-action");
        /*make the matching letters bold:*/
        b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
        b.innerHTML += arr[i].substr(val.length);
        /*insert a input field that will hold the current array item's value:*/
        b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
        /*execute a function when someone clicks on the item value (DIV element):*/
        b.addEventListener("click", function(e) {
          /*insert the value for the autocomplete text field:*/
          inp.value = this.getElementsByTagName("input")[0].value;
          /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
          closeAllLists();
        });
        a.appendChild(b);
      }
    }
  });
  
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
    var x = document.getElementById(this.id + "autocomplete-list");
    if (x) x = x.getElementsByTagName("div");
    if (e.keyCode == 40) {
      /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
      currentFocus++;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 38) {
      //up
      /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
      currentFocus--;
      /*and and make the current item more visible:*/
      addActive(x);
    } else if (e.keyCode == 13) {
      /*If the ENTER key is pressed, prevent the form from being submitted,*/
      e.preventDefault();
      if (currentFocus > -1) {
        /*and simulate a click on the "active" item:*/
        if (x) x[currentFocus].click();
      }
    }
  });
  
  let addActive = (x) => {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = x.length - 1;
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("active");
  }
  
  let removeActive = (x) => {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (let i = 0; i < x.length; i++) {
      x[i].classList.remove("active");
    }
  }
  
  let closeAllLists = (elmnt) => {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function(e) {
    closeAllLists(e.target);
  });
  
};


/*An array containing all the plant names in the db:*/
let plantList = [];

async function getPlantName(){
  fetch(allPlants_url)
  .then(res => {
      return res.json()
    })
  .then(data =>{

      let plantNameDisplay = data.map((object)=> {
          const {name} = object;
          return {name};
      })
      // console.log(plantNameDisplay);
      for (var p of plantNameDisplay){
          plantList.push(p.name);
          //console.log(p.name);
      }
  });
  
}
getPlantName();

/*initiate the autocomplete function on the "plantSearch" element, and pass along the countries array as possible autocomplete values:*/
autocomplete(document.getElementById("plantSearch"), plantList);



function edit(id) {
  fetch(`/plant/${id}`)
  .then(response => response.json())
  .then(data => {
    // console.log(data)
    document.getElementById("plant_id").innerHTML = id
    document.getElementById("editname").value = data.name
    document.getElementById("editcategory").value = data.category
    document.getElementById("editpinfo").value = data.p_info
    document.getElementById("editmintemp").value = data.min_temp
    document.getElementById("editmaxtemp").value = data.max_temp
    document.getElementById("editminhum").value = data.min_humidity
    document.getElementById("editmaxhum").value = data.max_humidity
    document.getElementById("editminraintol").value = data.min_rain_tolerance
    document.getElementById("editmaxraintol").value = data.max_rain_tolerance
    document.getElementById("editminptime").value = data.min_planting_time
    document.getElementById("editmaxptime").value = data.max_planting_time

    if (data.summer == true){
      document.getElementById("editsummer").checked = true;
    }
    else {
      document.getElementById("editsummer").checked = false;
    }
    if (data.rainy_season == true){
      document.getElementById("editrain").checked = true;
    }
    else{
      document.getElementById("editrain").checked = true;
    }

  }).catch((error) => {
    console.error("Error:", error);
  })
}

function update_plant(){

  id = document.getElementById("plant_id").innerHTML

  name = document.getElementById("editname").value
  category = document.getElementById("editcategory").value
  p_info = document.getElementById("editpinfo").value
  min_temp = document.getElementById("editmintemp").value
  max_temp = document.getElementById("editmaxtemp").value
  min_humid = document.getElementById("editminhum").value
  max_humid = document.getElementById("editmaxhum").value
  min_rain_tol = document.getElementById("editminraintol").value
  max_rain_tol = document.getElementById("editmaxraintol").value
  min_p_time = document.getElementById("editminptime").value
  max_p_time = document.getElementById("editmaxptime").value
  // summer = document.getElementById("editsummer").value
  // rainy_season = document.getElementById("editrain").value


  if (document.getElementById("editsummer").checked == true){
    summer = true
  } else {
    summer = false
  }
  if (document.getElementById("editrain").checked == true){
    rainy_season = true
  } else {
    rainy_season = false
  }

  inp_obj = {
    "name": name,
    "category": category,
    "p_info": p_info,
    "min_temp": min_temp,
    "max_temp": max_temp,
    "min_humidity": min_humid,
    "max_humidity": max_humid,
    "min_rain_tolerance": min_rain_tol,
    "max_rain_tolerance": max_rain_tol,
    "min_planting_time": min_p_time,
    "max_planting_time": max_p_time,
    "summer": summer,
    "rainy_season": rainy_season
  }

  fetch(`/update_plant/${id}`, {
    method: 'PATCH',
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    },
    body: JSON.stringify(inp_obj)
  })
  .then(res => res.json())
  .then(data => {
    console.log(data)
    getPlants()
  })
  .catch(error => console.log("ERROR"))

}

function delete_plant(id){
  fetch(`/plant/${id}`)
  .then(response => response.json())
  .then(data => {
    // console.log(data)
    document.getElementById("del_id").innerHTML = id
    document.getElementById("del_name").innerHTML = data.name
    document.getElementById("del_cat").innerHTML = data.category
    document.getElementById("del_info").innerHTML = data.p_info
    document.getElementById("del_temp").innerHTML = `${data.min_temp} - ${data.max_temp}`
    document.getElementById("del_humid").innerHTML = `${data.min_humidity} - ${data.min_humidity}`
    document.getElementById("del_rain").innerHTML = `${data.min_rain_tolerance} - ${data.max_rain_tolerance}`
    document.getElementById("del_p").innerHTML = `${data.min_planting_time} - ${data.min_planting_time}`

    if (data.summer == true && data.rainy_season == true)
      document.getElementById("del_season").innerHTML = "Wet and Dry"
    else if (data.summer == true) {
      document.getElementById("del_season").innerHTML = "Summer"
    } else {
      document.getElementById("del_season").innerHTML = "Rainy"
    }

  }).catch((error) => {
    console.error("Error:", error);
  })
}

function delete_c(){
  id = document.getElementById("del_id").innerHTML
  id_ = Number(id)
  // console.log(typeof id_)
  // console.log(id)
  fetch(`/delete_plant/${id_}`, {
    method: 'DELETE',
    headers: {
      'Content-type': 'application/json; charset=UTF-8'
    },
    // body: JSON.stringify(inp_obj)
  })
  .then(res => res.json())
  .then(data => {
    console.log(data)
    document.getElementById("del_msg").style.display = "block";
  })
  .catch(error => console.log("ERROR")) 
}