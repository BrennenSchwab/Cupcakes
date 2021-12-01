const URL = "http://127.0.0.1:5000/api"

/** generates the html for the cupcakes */

function generateHomeHTML(cupcake){

    return `
    <div cupcake-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-button">X</button>
      </li>
      <img class="Cupcake-image"
            src="${cupcake.image}"
            alt="(no image provided)">
    </div>
  `;
}


/** put existing cupcakes onto html */

async function showExistingCupcakes(){
    const resp = await axios.get(`${URL}/cupcakes`);

    for(let cData of resp.data.cupcakes){
        let newCupcake = $(generateHomeHTML(cData));
        $("#cupcake-inventory").append(newCupcake);
    }
}

/** handle cupcake adding form */

$("#cupcake-form").on("submit", async function(e) {
  e.preventDefault();

  let flavor = $("#form-flavor").val();
  let size = $("#form-size").val();
  let rating = $("#form-rating").val();
  let image = $("#form-image").val();

  const response = await axios.post(`${URL}/cupcakes`, {
    flavor, 
    size, 
    rating, 
    image
  });

  let newCupcake = $(generateHomeHTML(response.data.cupcake));
  $("#cupcake-inventory").append(newCupcake);
  $("#cupcake-form").trigger("reset");

});

/** handle delete cupcake for the above stated 'X' button */

$("#cupcake-inventory").on("click", ".delete-button", async function(e){
  e.preventDefault();
  
  let $cupcake = $(e.target).closest("div");
  let cupcakeID = $cupcake.attr("cupcake-id");

  await axios.delete(`${URL}/cupcakes/${cupcakeID}`);
  $cupcake.remove();
});

$(showExistingCupcakes);

