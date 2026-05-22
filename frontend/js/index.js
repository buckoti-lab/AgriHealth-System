$(document).ready(function () {

    loadVegetables();

});

/* LOAD VEGETABLES */

function loadVegetables() {

    $.ajax({
        url: `${BASE_URL}/api/vegetable/list/`,
        method: "GET",

        success: function (response) {

            $("#cropList").html("");

            response.data.forEach(crop => {

                $("#cropList").append(`

                    <div class="crop-item"
                         onclick="loadDiseases('${crop.crop}', '${crop.description}')">

                        <h4>${crop.crop}</h4>

                        <p>${crop.description}</p>

                    </div>

                `);

            });

        },

        error: function () {

            alert("Failed to load vegetables");

        }

    });

}

/* LOAD DISEASES */

function loadDiseases(cropName, cropDescription) {

    $.ajax({

        url: `${BASE_URL}/api/disease/list/${cropName}`,
        method: "GET",

        success: function (response) {

            let html = `

                <h2>${cropName}</h2>

                <p>${cropDescription}</p>

                <hr>

                <h4>Common Diseases</h4>

            `;

            if (response.data.length === 0) {

                html += `

                    <p>No diseases found.</p>

                `;

            } else {

                response.data.forEach(disease => {

                    html += `

                        <div class="disease-card">

                            <div class="disease-name">
                                ${disease.name}
                            </div>

                            <p>
                                ${disease.description}
                            </p>

                        </div>

                    `;

                });

            }

            $("#cropDetails").html(html);

        },

        error: function () {

            alert("Failed to load diseases");

        }

    });

}