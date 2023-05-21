(function() {
    "use strict";
 /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

})

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

function createPlants(){
    let inpsummer = "";
    let inprain = "";

    for (i in checkbox()){
        if (checkbox()[i] == "inputsummer") {
            inpsummer = true
        }
        if (checkbox()[i] == "inputrain") {
            inprain = true
        }
    }
}

//users
const user_url = 'http://127.0.0.1:8000/filter_users';

function getallusers(){
    fetch(user_url)
    .then(res => {
        return res.json()
      })
    
    .then(data =>{
        // console.log(data)
        const usersTable = document.getElementById("usersTable");
        usersTable.innerHTML='';

        let userDisplay = data.map((object)=> {
            const {id, username, birthday, country, state, city, is_active, is_public, plants} = object;
           
            return `
                <tr>
                <td>${id}</td>
                <td>${username}</td>
                <td>${birthday}</td>
                <td>${country}</td>
                <td>${state}</td>
                <td> ${city}</td>
                <td>${is_active}</td>
                <td>${is_public}</td>
                <td>${plants}</td>
                </tr>`;
            
        })/* .catch(error => console.log("ERROR")) */;
        
        usersTable.innerHTML = userDisplay;
    })
    
};
getallusers();
