// require('dotenv').config()
// const api_key = process.env.API_KEY;
// console.log(api_key)

let searchInp = document.querySelector(".weather__search");
let city = document.querySelector(".weaher__city");
let day = document.querySelector(".weather__day");
let calendar = document.querySelector(".weather__calendar");
let humidity = document.querySelector(".humiditiy-value");
let wind = document.querySelector(".wind-value");
let pressure = document.querySelector(".pressure-value");
let image = document.querySelector(".weather__image");
let temperaature = document.querySelector(".temperature-value");
let forecastBlock = document.querySelector(".weather__forecast");
let suggestions = document.querySelector("#suggestions");


// API variable
let weatherAPIKey = "2aefe52a593c0d988f240092f4dfa3c6";
let weatherBaseEndpoint =
  "https://api.openweathermap.org/data/2.5/weather?units=metric&appid=" +
  weatherAPIKey;

let forecastBaseEndpoint =
  "https://api.openweathermap.org/data/2.5/forecast?units=metric&appid=" +
  weatherAPIKey;
let cityBaseEndpoint = "https://api.teleport.org/api/cities/?search=";
let cityToLongLat = "http://api.openweathermap.org/geo/1.0/direct?"



function getCityLoc(cityString) {
  fetch(`${cityToLongLat}q=${cityString}&limit=1&appid=${weatherAPIKey}`)
    .then(response => response.json())
    .then(data => {
      console.log(data)
      console.log(data[0].lon)
      console.log(data[0].lat)

      inp_obj = {
        lat: data[0].lat,
        lon: data[0].lon
      }
      
      let query = Object.keys(inp_obj)
        .map(k =>encodeURIComponent(k) + '=' + encodeURIComponent(inp_obj[k]))
        .join('&');
    
      const weurl = "http://127.0.0.1:8000/predict?" + query
      // console.log(weurl)
      fetch(weurl)
        .then(response => response.json())
        .then(data => {
          // console.log(data)
          document.getElementById("p1").innerHTML = data[0].plant
          document.getElementById("p2").innerHTML = data[1].plant
          document.getElementById("p3").innerHTML = data[2].plant
        }).catch((error) => {
        console.error('Error:', error);
      });

    }).catch((error) => {
        console.error('Error:', error);
      });
}

window.onbeforeunload = () => {
  for(const form of document.getElementsByTagName('form')) {
    form.reset();
  }
}


//  API Connection for weathet today seaction
let getWeatherByCityName = async (cityString) => {
  let city;
  if (cityString.includes(",")) {
    city =
      cityString.substring(0, cityString.indexOf(",")) +
      cityString.substring(cityString.lastIndexOf(","));
  } else {
    city = cityString;
  }
  let endpoint = weatherBaseEndpoint + "&q=" + city;
  let response = await fetch(endpoint);
  if (response.status !== 200) {
    alert("City not found !");
    return;
  }
  let weather = await response.json();
  return weather;
};

//  API Connection for forecast seaction
let getForecastByCityID = async (id) => {
  let endpoint = forecastBaseEndpoint + "&id=" + id;
  let result = await fetch(endpoint);
  let forecast = await result.json();
  let forecastList = forecast.list;
  let daily = [];

  forecastList.forEach((day) => {
    let date = new Date(day.dt_txt.replace(" ", "T"));
    let hours = date.getHours();
    if (hours === 12) {
      daily.push(day);
    }
  });
  return daily;
};

let weatherForCity = async (city) => {
  let weather = await getWeatherByCityName(city);
  getCityLoc(city)
  if (!weather) {
    return;
  }
  let cityID = weather.id;
  updateCurrentWeather(weather);
  let forecast = await getForecastByCityID(cityID);
  updateForecast(forecast);
};
//  set city weather info
searchInp.addEventListener("keydown", async (e) => {
  if (e.keyCode === 13) {
    weatherForCity(searchInp.value);
  }
});

// API Connection for search Imput
searchInp.addEventListener("input", async () => {
  let endpoint = cityBaseEndpoint + searchInp.value;
  let result = await (await fetch(endpoint)).json();
  suggestions.innerHTML = "";
  let cities = result._embedded["city:search-results"];
  let length = cities.length > 5 ? 5 : cities.length;
  for (let i = 0; i < length; i++) {
    let option = document.createElement("option");
    option.value = cities[i].matching_full_name;
    suggestions.appendChild(option);
  }
});

// update weather details
let updateCurrentWeather = (data) => {
  city.textContent = data.name + ", " + data.sys.country;
  day.textContent = dayOfWeak();
  calendar.textContent = calenderInfo();
  humidity.textContent = data.main.humidity;
  pressure.textContent = data.main.pressure;
  wind.textContent = windInfo(data);
  temperaature.textContent =
    data.main.temp > 0
      ? "+" + Math.round(data.main.temp)
      : Math.round(data.main.temp);

  let imgID = data.weather[0].id;
  // weatherImages.forEach((obj) => {
  //   // if (obj.ids.includes(imgID)) {
  //   //   image.src = obj.url;
  //   // }
  // });
};

// update forecast weather details
let updateForecast = (forecast) => {
  forecastBlock.innerHTML = "";
  forecast.forEach((day) => {
    let iconUrl =
      "http://openweathermap.org/img/wn/" + day.weather[0].icon + "@2x.png";
    let dayName = dayOfWeak(day.dt * 1000);
    let temperature =
      day.main.temp > 0
        ? "+" + Math.round(day.main.temp)
        : Math.round(day.main.temp);
    let forecatItem = `
            <article class="weather__forecast__item">
                <img src="${iconUrl}" alt="${day.weather[0].description}" class="weather__forecast__icon">
                <h3 class="weather__forecast__day">${dayName}</h3>
                <p class="weather__forecast__temperature"><span class="value">${temperature}</span> &deg;C</p>
            </article>
        `;
    forecastBlock.insertAdjacentHTML("beforeend", forecatItem);
  });
};

// get day info
let dayOfWeak = (dt = new Date().getTime()) => {
  return new Date(dt).toLocaleDateString("en-EN", { weekday: "long" });
};

// get calender info
let calenderInfo = () => {
  return new Date().toLocaleDateString("en-EN", { calendar: "long" });
};

// get wind info
let windInfo = (data) => {
  let windDirection;
  let deg = data.wind.deg;
  if (deg > 45 && deg <= 135) {
    windDirection = "East";
  } else if (deg > 135 && deg <= 225) {
    windDirection = "South";
  } else if (deg > 225 && deg <= 315) {
    windDirection = "West";
  } else {
    windDirection = "North";
  }
  return windDirection + ", " + data.wind.speed;
};

// initial city for cairo
let init = () => {
  weatherForCity("Batangas").then(() => (document.body.style.filter = "blur(0)"));
};

init();
