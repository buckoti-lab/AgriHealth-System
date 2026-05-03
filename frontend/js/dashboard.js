const BASE_URL = "http://127.0.0.1:8000";
const token = localStorage.getItem("access_token")
let allData = []
let filteredData = []
let recentData = [];

$(document).ready(function(e){
       $("#main-content").load("home.html", function(response, status, xhr) {
           if (status === "error") {
              $("#main-content").html("<p>Error loading dashboard content.</p>");
            }
        });


        $("#upper-nav a").click(function (e) {
        e.preventDefault(); 
        let pageName = $(this).data("content");
        if(pageName){
          let url = pageName+".html";
          $("#main-content").load(url, function(response, status, xhr) {
             if (status === "error") {
             $("#main-content").html("<p>Error loading content from: " + url + "and" +xhr.responseText+".</p>");
            }
          });
        }else{
            $(".side-submenu").not($(this).next()).slideUp();
            $(this).next(".side-submenu").slideToggle();
        }
     });

    $("#upper-content-profile").click(function(e){
      $("#profile-content").slideToggle();
     })
      
    $(window).click(function (e) {
      if ($(e.target).is("#profile-content")) $("#profile-content").slideUp();
    });
})


// let historyData = [];

// // Preview Image
// $("#imageInput").change(function () {
//     let reader = new FileReader();

//     reader.onload = function (e) {
//         $("#previewImage").attr("src", e.target.result).removeClass("d-none");
//     };

//     reader.readAsDataURL(this.files[0]);
// });


// // Predict Button (simulate API)
// $("#predictBtn").click(function () {

//     // 🔥 Fake API response (replace with real AJAX)
//     let response = {
//         vegetable: "Tomato",
//         disease: "Late Blight",
//         treatment: [
//             "Spray copper fungicide every 7–10 days",
//             "Remove infected leaves",
//             "Ensure proper spacing",
//             "Water at base only",
//             "Use resistant seeds next season"
//         ],
//         image: $("#previewImage").attr("src"),
//         time: "Just now"
//     };

//     updateResult(response);
//     addToHistory(response);
// });


// // Update Result Panel
// function updateResult(data) {
//     $("#veg").text(data.vegetable);
//     $("#disease").text(data.disease);

//     $("#treatmentList").empty();
//     data.treatment.forEach(t => {
//         $("#treatmentList").append(`<li>${t}</li>`);
//     });
// }


// // Add to History Table
// function addToHistory(data) {
//     let index = historyData.length;
//     historyData.push(data);

//     $("#historyTable").prepend(`
//         <tr>
//             <td><i class="fa fa-image img-icon" data-id="${index}"></i></td>
//             <td>${data.vegetable}</td>
//             <td>${data.disease}</td>
//             <td><button class="btn btn-sm btn-info viewBtn" data-id="${index}">VIEW</button></td>
//             <td>${data.time}</td>
//         </tr>
//     `);
// }


// // VIEW button OR image click
// $(document).on("click", ".viewBtn, .img-icon", function () {
//     let id = $(this).data("id");
//     let data = historyData[id];

//     $("#modalImage").attr("src", data.image);

//     $("#modalTreatment").empty();
//     data.treatment.forEach(t => {
//         $("#modalTreatment").append(`<li>${t}</li>`);
//     });

//     let modal = new bootstrap.Modal(document.getElementById('viewModal'));
//     modal.show();
// });

// $('.nav-link').click(function() {
//     $('.nav-link').removeClass('active');
//     $(this).addClass('active');
// });



// Toggle dropdown
$("#userIcon").click(function (e) {
    e.stopPropagation();
    $("#userMenu").toggle();
});

// Hide when clicking outside
$(document).click(function () {
    $("#userMenu").hide();
});

// Prevent closing when clicking inside menu
$("#userMenu").click(function (e) {
    e.stopPropagation();
});

// Profile click
$("#profileBtn").click(function () {
    alert("Go to profile page");
    // window.location.href = "/profile";
});


function logoutUser(){
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    // Redirect to login
    window.location.href = '/login.html';
}
// Logout click
$("#logoutBtn").click(function () {

    const refresh_token = localStorage.getItem('refresh_token');
    const access_token = localStorage.getItem('access_token');
    
    if (refresh_token) {
        $.ajax({
            url: `${BASE_URL}/api/logout/`,
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ refresh_token: refresh_token }),
            headers: {
                Authorization: `Bearer ${access_token}`
            },
            success: function(response) {
                if (response.success) {
                    logoutUser()
                }
            },
            error: function() {
                logoutUser()
            }
        });
    } else {
        // No refresh token, just redirect
        logoutUser()
    }
});



// ajax-setup.js - Handle all AJAX responses globally
$(document).ajaxError(function(event, jqXHR, ajaxSettings, thrownError) {
    // Checking for 401 Unauthorized
    if (jqXHR.status === 401) {
        console.log('Authentication failed - logging out');
               
        // Use refresh token
        var refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
            $.ajax({
                url: `${BASE_URL}/api/auth/token/refresh/`,
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ refresh: refreshToken }),
                success: function(response) {
                    // Successfully refreshed
                    localStorage.setItem('access_token', response.access);
                    // You might want to retry the original request here
                    console.log('Token refreshed successfully');
                },
                error: function() {
                    // Refresh failed - logout
                    logoutUser()
                }
            });
        } else {
            // No refresh token - immediate logout
            logoutUser();
        }
    }
});

// Also check before each AJAX request
// $(document).ajaxSend(function(event, jqXHR, ajaxOptions) {
//     var token = localStorage.getItem('access_token');
    
//     // Check if token is expired before sending
//     if (token && isTokenExpired(token)) {
//         console.log('Token expired before request - aborting');
//         logoutUser();
//         return false; // Abort the request
//     }
    
//     // Add token to headers if exists
//     if (token) {
//         jqXHR.setRequestHeader('Authorization', 'Bearer ' + token);
//     }
// });