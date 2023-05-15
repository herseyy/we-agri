const allPlants_url = "http://127.0.0.1:8000/filter_plants";

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

//checkbox 

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


    // var catFruit = document.getElementById('catFruit');
    // var catVeggie = document.getElementById('catVeggie');
    // var summerTrue = document.getElementById('summerTrue');
    // var rainyTrue = document.getElementById('rainyTrue');

    // console.log(catFruit.value)
    // database

    // let fruit = catFruit.value;
    // let vegetable = catVeggie.value; 
    // let summer = summerTrue.value;
    // let rainy = rainyTrue.value;
    // console.log(fruit)
    // console.log(vegetable)
    // console.log(summer)
    // console.log(rainy)

    var inp_obj = {}
    
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
    }

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
        const plantDb = document.getElementById("plantsDb");
        plantDb.innerHTML='';

        let plantDisplay = data.map((object)=> {
            const {name, category, min_temp, max_temp, min_humidity, max_humidity, rain_tolerance, planting_time, rainy_season, summer} = object;
            
            let printSeason;
                if (summer && rainy_season){
                    printSeason = "Wet and Dry Season";
                } else if (summer && !rainy_season){
                    printSeason = "Summer";
                }else if (!summer && rainy_season){
                    printSeason = "Rainy";
                }else {
                    printSeason = "Neither";
                }

            return `
                <div class="plantItem col-lg-3 rounded-3 m-2 p-1 align-items-center">
                    <div class="plantName">Name: ${name}</div>
                    <div class="plantCat">Category: ${category}</div>
                    <div class="plantTemp">Temperature: ${min_temp} - ${max_temp} &degC </div>
                    <div class="plantHumid">Humidity: ${min_humidity} - ${max_humidity}% </div>
                    <div class="plantRain">Rain Tolerance: ${rain_tolerance}mm</div>
                    <div class="plantGrowth">Growth time: ${planting_time} weeks</div>
                    <div class="plantSzn">Season: ${printSeason}</div>
                </div>`;
            
        })/* .catch(error => console.log("ERROR")) */;
        document.getElementById('catFruit').value = "";
        document.getElementById('catVeggie').value = "";
        document.getElementById('summerTrue').value = "";
        document.getElementById('rainyTrue').value = "";

        plantDb.innerHTML = plantDisplay;
        
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
      this.parentNode.appendChild(a);
  
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          b.setAttribute("class","list-group-item list-group-item-action");
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
        console.log(plantNameDisplay);
        for (var p of plantNameDisplay){
            plantList.push(p.name);
            //console.log(p.name);
        }
    });
    
}
  getPlantName();

  /*initiate the autocomplete function on the "plantSearch" element, and pass along the countries array as possible autocomplete values:*/
  autocomplete(document.getElementById("plantSearch"), plantList);
