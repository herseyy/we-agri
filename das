[1mdiff --git a/pages/admin.html b/pages/admin.html[m
[1mindex 68d4332..21fe5ed 100644[m
[1m--- a/pages/admin.html[m
[1m+++ b/pages/admin.html[m
[36m@@ -43,13 +43,8 @@[m
                     </li>[m
         [m
                     <li>[m
[31m-<<<<<<< HEAD[m
[31m-                      <a class="dropdown-item d-flex align-items-center" href="/profile">[m
[31m-                        <i class="fa-solid fa-user-vneck"></i>[m
[31m-=======[m
                       <a class="dropdown-item d-flex align-items-center" href="profile.html">[m
                         <i class='bx bx-user-circle' ></i>[m
[31m->>>>>>> f66117c714734c56b95d2716a2a070817e030650[m
                         <span>My Profile</span>[m
                       </a>[m
                     </li>[m
[36m@@ -105,7 +100,7 @@[m
             <li class="nav-heading">Pages</li>[m
 [m
             <li class="nav-item">[m
[31m-                <a class="nav-link collapsed" href="/profile">[m
[32m+[m[32m                <a class="nav-link collapsed" onclick="check_token()">[m
                     <i class="fa-regular fa-user"></i>[m
                     <span>Profile</span>[m
                 </a>[m
[36m@@ -155,7 +150,7 @@[m
                           <h5 class="card-title">Create Plant</h5>[m
             [m
                           <!-- createplant Form -->[m
[31m-                          <form id="createplant" class="row g-3">[m
[32m+[m[32m                          <div id="createplant" class="row g-3">[m
                             <div class="col-12 d-flex">[m
                               <label for="inputName" class="form-label col-3">Name</label>[m
                               <input type="text" class="form-control" id="inputName">[m
[36m@@ -226,16 +221,16 @@[m
                                     </div>[m
                                 </div>[m
                             </div>[m
[31m-                            <div class="col-12 d-flex">[m
[31m-                                <label for="imgFile" class="form-label col-3">Add image</label>[m
[31m-                                <input type="file" id="imgFile" name="imgFile">[m
[31m-                            </div>[m
[31m-                            <div id="errormsg" class="col-12"></div>[m
[32m+[m[32m                            <div id="errormsg" class="col-12 alert alert-danger"></div>[m
                             <div class="text-center">[m
[31m-                              <button type="submit" class="btn btn-success" onclick="createPlants()">Submit</button>[m
[32m+[m[32m                              <button class="btn btn-success" onclick="createPlants()">Save</button>[m
                               <button type="reset" class="btn btn-secondary">Reset</button>[m
                             </div>[m
[31m-                          </form><!-- createplant Form -->[m
[32m+[m[32m                            <div class="col-12 d-flex" id="add_img">[m
[32m+[m[32m                                <label for="imgFile" class="form-label col-3">Add image</label>[m
[32m+[m[32m                                <input type="file" id="imgFile" name="imgFile">[m
[32m+[m[32m                            </div>[m
[32m+[m[32m                          </div><!-- createplant Form -->[m
             [m
                         </div>[m
                       </div>[m
[1mdiff --git a/static/js/admin.js b/static/js/admin.js[m
[1mindex c37f3b4..2b08174 100644[m
[1m--- a/static/js/admin.js[m
[1m+++ b/static/js/admin.js[m
[36m@@ -27,6 +27,23 @@[m
 }) ();[m
 [m
 [m
[32m+[m[32mfunction check_token(){[m
[32m+[m[32mfetch("/")[m
[32m+[m[32m  .then(response => response.json())[m
[32m+[m[32m  .then(data => {[m
[32m+[m[32m  console.log(data)[m
[32m+[m[32m  if (data['detail']){[m
[32m+[m[32m    window.location.href = '../login';[m
[32m+[m[32m  }[m
[32m+[m[32m  else {[m
[32m+[m[32m    window.location.href = '../profile';[m
[32m+[m[32m  }[m
[32m+[m[32m  }).catch((error) => {[m
[32m+[m[32m      console.error('Error:', error);[m
[32m+[m[32m    });[m
[32m+[m[32m}[m
[32m+[m
[32m+[m
 /* hide other sections  */[m
 [m
 function openforms(){[m
[1mdiff --git a/static/js/profile.js b/static/js/profile.js[m
[1mindex 4dff0cc..d7d9791 100644[m
[1m--- a/static/js/profile.js[m
[1m+++ b/static/js/profile.js[m
[36m@@ -1,3 +1,24 @@[m
[32m+[m[32mfunction check_token(){[m
[32m+[m[32m  fetch("/")[m
[32m+[m[32m    .then(response => response.json())[m
[32m+[m[32m    .then(data => {[m
[32m+[m[32m    console.log(data)[m
[32m+[m[32m    if (data['detail']){[m
[32m+[m[32m      window.location.href = '../';[m
[32m+[m[32m    }[m
[32m+[m[32m    else {[m
[32m+[m[32m      window.location.href = '../profile';[m
[32m+[m[32m    }[m
[32m+[m[32m    }).catch((error) => {[m
[32m+[m[32m        console.error('Error:', error);[m
[32m+[m[32m      });[m
[32m+[m[32m}[m
[32m+[m
[32m+[m[32mcheck_token()[m
[32m+[m
[32m+[m
[32m+[m
[32m+[m
 let locationButton = document.getElementById("get-location");[m
 let locationDiv = document.getElementById("location-details");[m
 [m
[36m@@ -603,4 +624,4 @@[m [mfunction logout() {[m
     window.location.href = '../login';[m
   })[m
   .catch(error => console.log("ERROR")) [m
[31m-}[m
\ No newline at end of file[m
[32m+[m[32m}[m
