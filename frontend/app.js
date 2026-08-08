async function loadHealth() {
    const response = await fetch("/api/health");
    const data = await response.json();

    document.getElementById("status").textContent =
        `API: ${data.status}, Datenbank: ${data.database}`;
}

async function loadRecipes() {
    const response = await fetch("/api/recipes");
    const data = await response.json();

    const list = document.getElementById("recipes");
    list.innerHTML = "";

    for (const recipe of data.recipes) {
        const item = document.createElement("li");
        item.textContent = `${recipe.title}: ${recipe.description}`;
        list.appendChild(item);
    }
}

const loginForm = document.getElementById("login-form");

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const identifier = document.getElementById("identifier").value;
    const userPassword = document.getElementById("user_password").value;

    const response = await fetch("/api/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            identifier: identifier,
            user_password: userPassword,
        }),
    });
    const data = await response.json();
    const message = document.getElementById("login-message");

    if (response.ok) {
        message.textContent = data.message;
    } else {
        message.textContent = data.detail;
    }
});

// loadHealth();
// loadRecipes();