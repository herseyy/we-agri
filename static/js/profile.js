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
  document.getElementById('settings').style.display='none'; 
  document.getElementById('profile').style.display='block';
}

function clickMyPlants(){
  document.getElementById('profile').style.display='none';
  document.getElementById('settings').style.display='none';
  document.getElementById('my_plants').style.display='block';
}

function clickSettings(){
  document.getElementById('profile').style.display='none';
  document.getElementById('my_plants').style.display='none';
  document.getElementById('settings').style.display='block';
}
 
$('.datepicker').datepicker({
  weekdaysShort: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
  showMonthsShort: true
})

//datepicker
// Strings and translations
monthsFull: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
'November', 'December'];
monthsShort: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
weekdaysFull: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
weekdaysShort: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
showMonthsShort: undefined;
showWeekdaysFull: undefined;

// Buttons
today: 'Today';
clear: 'Clear';
close: 'Close';

// Accessibility labels
labelMonthNext: 'Next month';
labelMonthPrev: 'Previous month';
labelMonthSelect: 'Select a month';
labelYearSelect: 'Select a year';

// Formats
format: 'd mmmm, yyyy';
formatSubmit: undefined;
hiddenPrefix: undefined;
hiddenSuffix: '_submit';
hiddenName: undefined;

// Editable input
editable: undefined;

// Dropdown selectors
selectYears: undefined;
selectMonths: undefined;

// First day of the week
firstDay: undefined;

// Date limits
min: undefined;
max: undefined;

// Disable dates
disable: undefined;

// Root picker container
container: undefined;

// Hidden input container
containerHidden: undefined;

// Close on a user action
closeOnSelect: true;
closeOnClear: true;

// Events
onStart: undefined;
onRender: undefined;
onOpen: undefined;
onClose: undefined;
onSet: undefined;
onStop: undefined;

// Classes
klass: {

  // The element states
  input: 'picker__input';
  active: 'picker__input--active';

  // The root picker and states *
  picker: 'picker';
  opened: 'picker--opened';
  focused: 'picker--focused';

  // The picker holder
  holder: 'picker__holder';

  // The picker frame, wrapper, and box
  frame: 'picker__frame';
  wrap: 'picker__wrap';
  box: 'picker__box';

  // The picker header
  header: 'picker__header';

  // Month navigation
  navPrev: 'picker__nav--prev';
  navNext: 'picker__nav--next';
  navDisabled: 'picker__nav--disabled';

  // Month & year labels
  month: 'picker__month';
  year: 'picker__year';

  // Month & year dropdowns
  selectMonth: 'picker__select--month';
  selectYear: 'picker__select--year';

  // Table of dates
  table: 'picker__table';

  // Weekday labels
  weekdays: 'picker__weekday';

  // Day states
  day: 'picker__day';
  disabled: 'picker__day--disabled';
  selected: 'picker__day--selected';
  highlighted: 'picker__day--highlighted';
  now: 'picker__day--today';
  infocus: 'picker__day--infocus';
  outfocus: 'picker__day--outfocus';

  // The picker footer
  footer: 'picker__footer';

  // Today, clear, & close buttons
  buttonClear: 'picker__button--clear';
  buttonClose: 'picker__button--close';
  buttonToday: 'picker__button--today';
}