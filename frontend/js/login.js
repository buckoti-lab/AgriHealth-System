// const togglePassword = document.getElementById("togglePassword");
// const password = document.getElementById("password");

// togglePassword.addEventListener("click", function () {
//     const type = password.getAttribute("type") === "password" ? "text" : "password";
//     password.setAttribute("type", type);

//     this.classList.toggle("fa-eye-slash");
// });
// $(document).ready(function(){
//     $("#loginForm").on("submit",function(e){
//         e.preventDefault()

//         const formData = new FormData(this)

//         // let data = {
//         //     "username":$("#username").val(),
//         //     "password":$("#password").val()
//         // }
//         $.ajax({
//             url:"http://127.0.0.1:8000/api/auth/token/",
//             method:"post",
//             data:formData,
//             processData:false,
//             contentType:false,
//             success:function(res){
//                 if(res.success){
//                     window.location.href = "dashboard.html";
//                 }else{
//                    swal.fire("Error!",res.message,"error");
//                 }
//             },
//             error:function(xhr,error,status){
//                 swal.fire("Error!","Failed to login: "+xhr.responseText,"error");
//             }
            
//         })
//     })
// })

$(document).ready(function(){
    $("#loginForm").on("submit", function(e){
        e.preventDefault();
        
        // Create JSON object instead of FormData
        const loginData = {
            username: $("#username").val(),
            password: $("#password").val()
        };
        
        $.ajax({
            // url: "http://127.0.0.1:8000/api/login/",  // Match your backend URL
            url:"http://127.0.0.1:8000/api/auth/token/",
            method: "POST",
            contentType: "application/json",  
            data: JSON.stringify(loginData),   
            success: function(res){
                //Handling backend returns access/refresh tokens
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