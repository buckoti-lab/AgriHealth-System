loadRecent()

$("#uploadForm").on("submit",function(e){
    e.preventDefault()

     const formData = new FormData(this)

     $.ajax({
        url:`${BASE_URL}/api/ai/predict/`,
        method:"post",
        data:formData,
        processData:false,
        contentType:false,
        headers: {
            Authorization: `Bearer ${token}`
            // "Content-Type": "multipart/form-data",
          },
        success: function(res){
            if(res.success){
                console.log(res)
                updateResult(res.data)

            }else{
                swal.fire("Error!","An error occured!: "+xhr.responseText,"error");
            }
        },
        error:function(xhr,status,error){
           swal.fire("Error!","Failed to predict: "+xhr.responseText+"Error: "+error,"error");
        }
        
     })
})

// $.get("http://127.0.0.1:8000/api/ai/predictions/recent",function(data){
//     let index = recentData.length;
//     recentData.push(data);

//     $("#recentTable").prepend(`
//         <tr>
//             <td><i class="fa fa-image img-icon" data-id="${index}"></i></td>
//             <td>${data.vegetable}</td>
//             <td>${data.disease}</td>
//             <td><button class="btn btn-sm btn-info viewBtn" data-id="${index}">VIEW</button></td>
//             <td>${data.time}</td>
//         </tr>
//     `);
// })

function loadRecent(){
    $.ajax({
        url: "http://127.0.0.1:8000/api/ai/predictions/recent",
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`
        },
        success: function(res){
            if(res.success){
                res.data.forEach(item => {
                    let index = recentData.length;
                    recentData.push(item);

                    $("#recentTable").prepend(`
                        <tr>
                            <td><i class="fa fa-image img-icon" data-id="${index}"></i></td>
                            <td>${item.vegetable}</td>
                            <td>${item.disease}</td>
                            <td><button class="btn btn-sm btn-info viewBtn" data-id="${index}">VIEW</button></td>
                            <td>${item.time_ago}</td>
                        </tr>
                    `);
                });
            }
        },
        error: function(xhr){
            console.log(xhr.responseText);
        }
    });
}

// Update Result Panel
function updateResult(res_data) {
    console.log(res_data);
    res_data.forEach(d => {
        $("#veg").text(d.vegetable)
        $("#disease").text(d.disease)
        $("#treatmentList").empty()
        if(d.treatments){
            d.treatments.forEach(t => {
                $("#treatmentList").append(`<li>${t.solution}</li>`);
            });
        }else{
            $("#treatmentList").append(`<li>No treatment details for detected disease diesease</li>`);
        }
    })
    
    $("#recentTable").empty()
    loadRecent()
}

// Add to recent Table
// function updateRecent(data) {
//     let index = recentData.length;
//     recentData.push(data);

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

// VIEW button OR image click
$(document).on("click", ".viewBtn", function () {
    let id = $(this).data("id");
    let data = recentData[id];
    
    $("#homeTreatments").empty();

    if(data.treatments && data.treatments.length > 0){
        console.log("This is my data"+data.treatments)
        data.treatments.forEach(t => {
            console.log(t.solution)
            $("#homeTreatments").append(`<li>${t.solution}</li>`);
        });
    }else{
         $("#homeTreatments").append(`<li>No treatments details for this disease</li>`);
    }

    // let modal = new bootstrap.Modal(document.getElementById('treatmentModal'));
    $("#homeTreatmentsModal").modal("show")
    // modal.show();
});


$(document).on("click","#recentTable .img-icon", function () {
    let id = $(this).data("id");
    let data = recentData[id];
    alert("Image clicked"+BASE_URL+data.image)

    $("#homeImage").attr("src", BASE_URL+data.image);
    // let modal = new bootstrap.Modal(document.getElementById('viewModal'));
    $("#homeImageModal").modal("show")
    // modal.show();
});


// $("#predictBtn").on("click",function(e){
//     e.preventDefault()

//     // const formData = new FormData(this)

//     alert("Button clicked")
// })