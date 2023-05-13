

// database

getPlants();
    async function getPlants(){
        const response = await fetch('http://127.0.0.1:8000/get_all_user_plants')
        console.log(response);
        const plant = await response.json();
        console.log(plant);
        length = data.drinks.length;
        console.log(plant);
        var plantData="";
        for (i=0; i<length; i++){
            let printSeason;
            if(plant.plant[i].summer == true && plant.plant[i].rainy_season == true) {
                plantSeason = "Wet and Dry Season";
            }
            if(plant.plant[i].rainy_season == true && plant.plant[i].summer != true){
                plantSeason = "Rainy";
            }
            if(plant.plant[i].summer == true && plant.plant[i].rainy_season != true){
                plantSeason = "Summer";
            }

            plantData+= '<div class="plantItem col-lg-3 rounded-3 m-2 p-2 align-items-center">';
            plantData+= '<div class="plantName">Name: '+ plant.plant[i].name +'</div>';
            plantData+= '<div class="plantCat">Category: '+ plant.plant[i].category +'</div>';
            plantData+= '<div class="plantTemp">Temperature: '+ plant.plant[i].min_temp + ' - ' + plant.plant[i].max_temp +'</div>';
            plantData+= '<div class="plantHumid">Humidity: '+ plant.plant[i].min_humidity + ' - ' + plant.plant[i].max_humidity +'</div>';
            plantData+= '<div class="plantRain">Rain Tolerance: '+ plant.plant[i].rain_tolerance +'</div>';
            plantData+= '<div class="plantGrowth">Growth time: '+ plant.plant[i].planting_time +'</div>';
            plantData+= '<div class="plantSzn">Season: '+ printSeason +'</div>';
            plantData+= '</div>';
        }
        document.getElementById("plantsDb").innerHTML=plantData;
    }

/* .then (res => {
    if (res.ok){
        console.log('SUCCESS')
    } else {
        console.log('Not Successful')
    }
    res.json()
})
.then(data => console.log(data))
.catch(error => console.log('ERROR'))

    } */


