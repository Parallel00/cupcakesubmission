const BASE_URL = "http://localhost:5000/api";

async function showInitialCupcakes() {
  try {
    const response = await axios.get(`${BASE_URL}/cupcakes`);
    const cupcakes = response.data.cupcakes;
    cupcakes.forEach(cupcake => addCupcakeToUI(cupcake));
  } catch (error) {
    console.error("Error fetching cupcakes:", error);
  }
}

async function addNewCupcake(flavor, rating, size, image) {
  try {
    const response = await axios.post(`${BASE_URL}/cupcakes`, { flavor, rating, size, image });
    const newCupcake = response.data.cupcake;
    addCupcakeToUI(newCupcake);
    $("#new-cupcake-form").trigger("reset");
  } catch (error) {
    console.error("Error adding cupcake:", error);
  }
}

async function deleteCupcake(cupcakeId) {
  try {
    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $(`div[data-cupcake-id="${cupcakeId}"]`).remove();
  } catch (error) {
    console.error("Error deleting cupcake:", error);
  }
}

function addCupcakeToUI(cupcake) {
  const cupcakeHTML = `
    <div data-cupcake-id="${cupcake.id}">
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-button">X</button>
      </li>
      <img class="Cupcakeimage" src="${cupcake.image}" alt="(no image provided)">
    </div>
  `;
  $("#cupcakes-list").append(cupcakeHTML);
}

$("#new-cupcake-form").on("submit", function (evt) {
  evt.preventDefault();
  const flavor = $("#form-flavor").val();
  const rating = $("#form-rating").val();
  const size = $("#form-size").val();
  const image = $("#form-image").val();
  addNewCupcake(flavor, rating, size, image);
});

$("#cupcakes-list").on("click", ".delete-button", function (evt) {
  evt.preventDefault();
  const cupcakeId = $(evt.target).closest("div").data("cupcake-id");
  deleteCupcake(cupcakeId);
});

showInitialCupcakes();
