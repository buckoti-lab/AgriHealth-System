$(document).ready(function(){
    $("#registerForm").on("submit", function(e){
        e.preventDefault();
        
        const registerData = {
            username: $("#username").val(),
            email: $("#email").val(),
            password: $("#password").val()
        };
        
        $.ajax({
            url:`${BASE_URL}/api/auth/register/`,
            method: "POST",
            contentType: "application/json",  
            data: JSON.stringify(registerData),   
            success: function(res){
                 if(res.success){
                    swal.fire("Success!",res.message,"success").then(() => window.location.href = "login.html");
                 }
            },
            error: function(xhr, status, error){
                let errorMessage = "Register failed";
                if (xhr.responseJSON) {
                    errorMessage = JSON.stringify(xhr.responseJSON);
                } else {
                    errorMessage = xhr.responseText;
                }
                Swal.fire("Error!", "Something went wrong!:" + errorMessage, "error");
            }
        });
    });
});