loadProfile();

function loadProfile(){
    $.ajax({
        url: `${BASE_URL}/api/auth/profile/`,
        type:"GET",
        headers: {
            Authorization: `Bearer ${token}`
        },
        success: function(res){
            if(res.success){
                $("#editBtn").data("id", res.data.id)
                $("#email").text(res.data.email)
                $("#username").text(res.data.username)
            }
        },
        error: function(xhr,status,error){
            Swal.fire({
                title:"Sucess!",
                text:"Failed to fetch:"+xhr.responseText,
                icon:"success",
                confirmationButtonText:"ok"
            })
        }

    })

}

$(document).on("click", "#editBtn", function () {
    let id = $(this).data("id");
    const email = $("#email").text()
    const username = $("#username").text()
     
    $("#editId").val(id)
    $("#editEmail").val(email)
    $("#editUsername").val(username)

    $("#EditProfileModal").modal("show")
});



$(document).on("submit","#editprofileForm",function(e){
    e.preventDefault()
    
    const formData = new FormData(this);

    $.ajax({
        url: `${BASE_URL}/api/auth/edit/`,
        method:"PATCH",
        data:formData,
        processData:false,
        contentType:false,
        headers: {
            Authorization: `Bearer ${token}`
        },
        success:function(res){
            if(res.success){
                Swal.fire("Success!",res.message,"success")
            }
        },
        error: function(xhr){
            Swal.fire("Error!","Failed to update profile"+xhr.responseText,"error")
        }
    })
    
})
