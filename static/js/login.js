/* login */

document
.getElementById("login-form")
.addEventListener("submit", async (e) => {

    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const response = await fetch("/login", {

    method: "POST",

    credentials: "same-origin",

    headers: {
        "Content-Type": "application/json"
    },

    body: JSON.stringify({
        email,
        password
    })
});

    const data = await response.json();

    if (data.success) {

        window.location.href = "/dashboard";

    } else {

        alert(data.message);

    }
});
