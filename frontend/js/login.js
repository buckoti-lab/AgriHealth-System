$(document).ready(function(){
    $("#loginForm").on("submit", function(e){
        e.preventDefault();


        $("#loginBtn")
            .html(`<span class="spinner-border spinner-border-sm"></span> Loading...`);
    
        const loginData = {
            username: $("#username").val(),
            password: $("#password").val()
        };
        
        $.ajax({
            url:`${BASE_URL}/api/auth/login/`,
            method: "POST",
            contentType: "application/json",  
            data: JSON.stringify(loginData),   
            success: function(res){
                if (res.access && res.refresh) {
    
                    localStorage.setItem('access_token', res.access);
                    localStorage.setItem('refresh_token', res.refresh);
                    window.location.href = "dashboard.html";
                } else {
                    Swal.fire("Error!", "Login failed:"+res.message, "error");
                }
            },
            error: function(xhr, status, error){
                let errorMessage = "Login failed";
                if (xhr.responseJSON) {
                    errorMessage = JSON.stringify(xhr.responseJSON);
                } else {
                    errorMessage = xhr.responseText;
                }
                Swal.fire("Error!", "Something went wrong!:" + errorMessage, "error");
            },
            complete: function(){
                $("#loginBtn").html(`Login`);
            }
        });
    });
});