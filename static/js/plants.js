function checkbox() {
    var checkboxes = document.getElementsByName("checkbox");
    let checked_symptoms = [];
    for (var checkbox of checkboxes) {
        if (checkbox.checked) {
            // console.log(checkbox.id)
            checked_symptoms.push(checkbox.id);
            checked_symptoms.sort();
        }
    }
    // console.log(checked_symptoms)

    return checked_symptoms
}

//checkbox 

function getPlants(){

    let fruit = "";
    let vegetable = ""; 
    let summer = "";
    let rainy = "";

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

    const allPlants_url = "http://127.0.0.1:8000/filter_plants";

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
            const {name, category,min_temp, max_temp, min_humidity, max_humidity, rain_tolerance, planting_time, rainy_season, summer} = object;
            
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
                <div class="plantItem col-lg-3 rounded-3 m-2 p-2 align-items-center">
                    <div class="plantName">Name: ${name}</div>
                    <div class="plantCat">Category: ${category}</div>
                    <div class="plantTemp">Temperature: ${min_temp} - ${max_temp} &degC </div>
                    <div class="plantHumid">Humidity: ${min_humidity} - ${max_humidity}% </div>
                    <div class="plantRain">Rain Tolerance: ${rain_tolerance}mm</div>
                    <div class="plantGrowth">Growth time: ${planting_time}</div>
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
