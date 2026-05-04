/* =========================
   FETCH HISTORY DATA
========================= */
function loadHistory() {
    $.ajax({
        url: `${BASE_URL}/api/ai/predictions/history`,
        method: "GET",
        headers: {
            Authorization: `Bearer ${token}`
        },
        success: function (res) {
            console.log(res)
            if (res.success) {
                allData = res.data || [];
                filteredData = [...allData];
                renderTable(filteredData);
            }
        },
        error: function (xhr) {
            console.log(xhr.responseText);
        }
    });
}

/* =========================
   RENDER TABLE
========================= */
function renderTable(data) {
    $("#historyTable").empty();

    if (!data || data.length === 0) {
        $("#historyTable").html(`
            <tr>
                <td colspan="6" class="text-center">No data found</td>
            </tr>
        `);
        $("#count").text(0);
        return;
    }

    data.forEach((item) => {
        $("#historyTable").append(`
            <tr>
                <td><i class="fa fa-image img-icon" data-id="${item.id}"></i></td>
                <td>${item.vegetable}</td>
                <td>${item.disease}</td>
                <td><span class="view-btn" data-id="${item.id}">👁 VIEW</span></td>
                <td><i class="fa fa-trash text-danger delete-btn" data-id="${item.id}"></i></td>
                <td>${item.time_ago}</td>
            </tr>
        `);
    });

    $("#count").text(data.length);
}

/* =========================
   SEARCH
========================= */
$("#searchInput").on("keyup", function () {
    let value = $(this).val().toLowerCase();

    filteredData = allData.filter(item =>
        (item.disease || "").toLowerCase().includes(value) ||
        (item.vegetable || "").toLowerCase().includes(value)
    );

    renderTable(filteredData);
});

/* =========================
   FILTER DATA
========================= */
$("#filterSelect").change(function () {
    let value = $(this).val();
    
    if (!value) {
        filteredData = [...allData];
    } else {
        const now = new Date();
        
        filteredData = allData.filter(item => {
            const itemDate = new Date(item.date);
            const diffTime = now - itemDate;
            const diffDays = diffTime / (1000 * 60 * 60 * 24);
            
            switch(value) {
                case "1_day":
                    return diffDays <= 1;
                case "7_days":
                    return diffDays <= 7;
                case "30_days":
                    return diffDays <= 30;
                case "90_days":
                    return diffDays <= 90;
                case "365_days":
                    return diffDays <= 365;
                default:
                    return true;
            }
        });
    }
    
    renderTable(filteredData);
});

/* =========================
   VIEW DETAILS (BOOTSTRAP MODAL)
========================= */
$(document).on("click", ".view-btn", function () {
    let id = $(this).data("id");
    let data = allData.find(item => item.id == id);

    if (!data) return;

    $("#historyTreatments").empty();

    if (data.treatments && data.treatments.length > 0) {
        console.log(data.treatments)
        data.treatments.forEach(t => {
            $("#historyTreatments").append(`<li>${t.solution}</li>`);
        });
    } else {
        $("#historyTreatments").append(`<li>No treatment details available</li>`);
    }

    $("#viewTreatsModal").modal("show")
});


$(document).on("click","#historyTable .img-icon", function () {
    let id = $(this).data("id");
    let data = allData.find(item => item.id == id);

    if (!data) return;

    $("#modalImage").attr("src", BASE_URL+data.image || "");
    $("#modalImage").attr("alt", data.vegetable || "Vegetable image");

    $("#viewImageModal").modal("show")
});

/* =========================
   DELETE ITEM (With Backend Sync)
========================= */
$(document).on("click", ".delete-btn", function () {
    let id = $(this).data("id");

    Swal.fire({
        title: "Are you sure?",
        text: "This prediction will be permanently deleted!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#d33",
        cancelButtonColor: "#3085d6",
        confirmButtonText: "Yes, delete it!"
    }).then((result) => {
        if (result.isConfirmed) {
            $.ajax({
                url: `${BASE_URL}/api/ai/predictions/${id}/`,
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${token}`
                },
                success: function(res) {
                    allData = allData.filter(item => item.id != id);
                    filteredData = filteredData.filter(item => item.id != id);
                    renderTable(filteredData);
                    
                    Swal.fire("Deleted!", "Prediction has been deleted.", "success");
                },
                error: function(xhr) {
                    console.log(xhr.responseText);
                    Swal.fire("Error!", "Failed to delete prediction.", "error");
                }
            });
        }
    });
});

/* =========================
   INITIAL LOAD
========================= */
loadHistory();