const API_URL = "http://127.0.0.1:5000";

let token = "";


// REGISTER
async function register() {

    const username =
        document.getElementById("registerUsername").value;

    const password =
        document.getElementById("registerPassword").value;


    const response = await fetch(
        `${API_URL}/register`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username,
                password
            })
        }
    );

    const data = await response.json();

    alert(data.message);
}



// LOGIN
async function login() {

    const username =
        document.getElementById("loginUsername").value;

    const password =
        document.getElementById("loginPassword").value;


    const response = await fetch(
        `${API_URL}/login`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username,
                password
            })
        }
    );

    const data = await response.json();

    token = data.token;

    alert(data.message);
}



// FETCH PRODUCTS
async function fetchProducts() {

    const response = await fetch(
        `${API_URL}/products`
    );

    const products = await response.json();

    displayProducts(products);
}



// DISPLAY PRODUCTS
function displayProducts(products) {

    let table =
        document.getElementById("productTable");

    table.innerHTML = "";

    products.forEach(product => {

        table.innerHTML += `

        <tr>

            <td>${product.id}</td>

            <td>${product.name}</td>

            <td>${product.category}</td>

            <td>${product.quantity}</td>

            <td>${product.price}</td>

            <td>

                <button
                    class="btn btn-danger btn-sm"
                    onclick="deleteProduct(${product.id})"
                >
                    Delete
                </button>

            </td>

        </tr>
        `;
    });
}



// ADD PRODUCT
async function addProduct() {

    const name =
        document.getElementById("name").value;

    const category =
        document.getElementById("category").value;

    const quantity =
        document.getElementById("quantity").value;

    const price =
        document.getElementById("price").value;


    const response = await fetch(
        `${API_URL}/products`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },

            body: JSON.stringify({
                name,
                category,
                quantity: parseInt(quantity),
                price: parseFloat(price)
            })
        }
    );

    const data = await response.json();
    console.log(data);

    alert(data.message);

    fetchProducts();
}



// DELETE PRODUCT
async function deleteProduct(id) {

    await fetch(
        `${API_URL}/products/${id}`,
        {
            method: "DELETE"
        }
    );

    fetchProducts();
}



// SEARCH PRODUCT
async function searchProduct() {

    const name =
        document.getElementById("searchInput").value;

    const response = await fetch(
        `${API_URL}/products/search?name=${name}`
    );

    const products = await response.json();

    displayProducts(products);
}



fetchProducts();