console.log("✅ crop.js loaded");

/* IMPORTANT: attach to window */
window.recommendCrop = async function () {

    const district = document.getElementById("district")?.value;
    const N = document.getElementById("nitrogen")?.value;
    const P = document.getElementById("phosphorus")?.value;
    const K = document.getElementById("potassium")?.value;
    const ph = document.getElementById("ph")?.value;

    const resultBox = document.getElementById("result");

    if (!district || !N || !P || !K || !ph) {
        resultBox.innerHTML = "❌ Please fill all fields.";
        return;
    }

    const url = `https://agrimind-oxrb.onrender.com` +
                `?district=${district}&N=${N}&P=${P}&K=${K}&ph=${ph}`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (!data.success) {
            resultBox.innerHTML = "❌ " + data.error;
            return;
        }

        resultBox.innerHTML = `
            <b>${data.message}</b><br>
            🌱 Local crops: ${data.local_crops.join(", ")}
        `;

    } catch (err) {
        console.error(err);
        resultBox.innerHTML = "❌ Backend not reachable.";
    }
};
