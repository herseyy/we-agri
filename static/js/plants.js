// for every plantItem

var plantData = document.getElementsByClassName('plantItem');
/* 
for (var i=0; i<plantData.length;i++){
    var plantName = document.createElement("div");
    var plantCat = document.createElement("div");
    var plantTemp = document.createElement("div");
    var plantHumid = document.createElement("div");
    var plantRain = document.createElement("div");
    var plantGrowth = document.createElement("div");
    var plantSzn = document.createElement("div");
    plantName.id = "plantName";
    plantCat.id = "plantCat";
    plantTemp.id = "plantTemp";
    plantHumid.id = "plantHumid";
    plantRain.id = "plantRain";
    plantGrowth.id = "plantGrowth";
    plantSzn.id = "plantSzn";
    plantName.innerHTML = "Name:";
    plantCat.innerHTML = "Category:";
    plantTemp.innerHTML = "Temperature:";
    plantHumid.innerHTML = "Humidity:";
    plantRain.innerHTML = "Rain Tolerance:";
    plantGrowth.innerHTML = "Growth Time:";
    plantSzn.innerHTML = "Season:";
    plantData[i].appendChild(plantName,plantCat,plantTemp, plantHumid, plantRain, plantGrowth, plantSzn)
} */

function createpDiv(text) {
    var pdiv = document.createElement('div')
    pdiv.textcontent = text;
    return pdiv;
}

var data = [
    createpDiv('Name:'),
    createpDiv('Category:'),
    createpDiv('Temperature:'),
    createpDiv('Humidity:'),
    createpDiv('Rain Tolerance:'),
    createpDiv('Growth Time:'),
    createpDiv('Season:')
]

data.forEach(function(pdiv){
    plantData.appendChild(pdiv);
});