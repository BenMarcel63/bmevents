console.log("login.js loaded");

const loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", async (e) => {

    e.preventDefault();

    console.log("Login button clicked");

    const data = {
        email: document.getElementById("loginEmail").value,
        password: document.getElementById("loginPassword").value
    };

    console.log(data);

    try {

        const response = await fetch("http://localhost:5000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        console.log("Status:", response.status);

        const text = await response.text();
        console.log("Server replied:", text);

    } catch (err) {
        console.error(err);
    }

});