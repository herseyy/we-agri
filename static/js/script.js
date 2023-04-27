// signup precise location btn
let x = document.getElementById("location");
function getPreciseLocation(){
    if(navigator.geolocation){
        navigator.geolocation.getCurrentPosition(showExactPosition)
    }else{
        x.innerHTML = "Geolocation is not supported"
    }
}

function showExactPosition(position){
    x.innerHTML= `Latitude: ${position.coords.latitude} <br> Longitude: ${position.coords.longitude}`;
}
        
// sign up submit form
let signupUname = document.getElementById('typeNameX');
let signupPword = document.getElementById('password');
let confirmPword = document.getElementById('confirm_password');
let rTime = 3;

function redirectLogin() {
    document.getElementById('signupcontent').style.display='none'; 
    document.getElementById('logincontent').style.display='block';
    document.getElementById('signupValue').innerText = "";
}

function clearSigninInput(){
    signupUname.value = "";
    signupPword.value = "";
    confirmPword.value = "";
}

function submitForm(){
    if (signupUname.value == "" || signupPword.value == "" || confirmPword.value == ""){
        document.getElementById('signupValue').innerText = "Please input a value."; 
    } else if (signupPword.value != confirmPword.value){
        document.getElementById('signupValue').innerText = "Certain values do not match.";
    } else{
        //document.getElementById('signupcontent').submit();
        document.getElementById('signupValue').innerText = "Sign up successful! Redirecting...";
        clearSigninInput();
        setTimeout(redirectLogin, rTime*1000);
    }
}

