$(document).ready(function(){
    $("#registerForm").on("submit", function(e){
        e.preventDefault();
        
        // Create JSON object instead of FormData
        const registerData = {
            username: $("#username").val(),
            email: $("#email").val(),
            password: $("#password").val()
        };
        
        $.ajax({
            // url: "http://127.0.0.1:8000/api/login/",  // Match your backend URL
            url:"http://127.0.0.1:8000/api/auth/register/",
            method: "POST",
            contentType: "application/json",  
            data: JSON.stringify(registerData),   
            success: function(res){
                //Handling backend returns access/refresh tokens
                 if(res.success){
                    swal.fire("Success!",res.message,"success").then(() => window.location.href = "login.html");
                 }
            },
            error: function(xhr, status, error){
                let errorMessage = "Register failed";
                if (xhr.responseJSON) {
                    // Handle DRF validation errors
                    errorMessage = JSON.stringify(xhr.responseJSON);
                } else {
                    errorMessage = xhr.responseText;
                }
                Swal.fire("Error!", "Something went wrong!:" + errorMessage, "error");
            }
        });
    });
});