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

loadHealth();
loadRecipes();