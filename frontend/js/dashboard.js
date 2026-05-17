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


        $("#upper-nav a,#profileBtn").click(function (e) {
            e.preventDefault(); 
            
            if($(this).hasClass("nav-link")){
                $(".nav-link").removeClass("active");
                $(this).addClass("active");
            }

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
        logoutUser()
    }
});



//Handle all AJAX responses globally
$(document).ajaxError(function(event, jqXHR, ajaxSettings, thrownError) {

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
                    localStorage.setItem('access_token', response.access);
                    console.log('Token refreshed successfully');
                },
                error: function() {
                    logoutUser()
                }
            });
        } else {
            logoutUser();
        }
    }
});