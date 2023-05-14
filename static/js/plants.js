

const plantDb = document.getElementById("plantsDb");

// database
const allPlants_url = "http://127.0.0.1:8000/filter_plants";

    async function getPlants(){
        const res = await fetch(allPlants_url)
        const data = await res.json();
        return data
    }
    async function displayAllPlants(){
        const payload = await getPlants();
        
        let plantDisplay = payload.map((object)=> {
            const {name, category,min_temp, max_temp, min_humidity, max_humidity, rain_tolerance, planting_time, rainy_season, summer} = object;
            let printSeason;
            if (summer == true && rainy_season == true){
                printSeason = "Wet and Dry Season";
            } else if (summer == true && rainy_season == false){
                printSeason = "Summer";
            }else if (summer == false && rainy_season == true){
                printSeason = "Rainy";
            }else {
                printSeason = "unidentified";
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
                </div>
            `;
            
        }).join("");
        plantDb.innerHTML = plantDisplay;
        
    }
    displayAllPlants();

/* 
.then (res => {
    if (res.ok){
        console.log('SUCCESS')
    } else {
        console.log('Not Successful')
    }
    res.json()
})
.then(data => console.log(data))
.catch(error => console.log('ERROR'))  */