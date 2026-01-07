console.log("✅ fertilizer.js loaded");

async function recommendFertilizer() {
    const temperature = document.getElementById("temperature").value;
    const humidity = document.getElementById("humidity").value;
    const moisture = document.getElementById("moisture").value;
    const soil_type = document.getElementById("soil_type").value;
    const crop_type = document.getElementById("crop_type").value;
    const nitrogen = document.getElementById("nitrogen").value;
    const potassium = document.getElementById("potassium").value;
    const phosphorus = document.getElementById("phosphorus").value;

    const resultBox = document.getElementById("fertilizer-result");

    const url = `https://agrimind-oxrb.onrender.com/recommend_fertilizer?temperature=${temperature}&humidity=${humidity}&moisture=${moisture}&soil_type=${soil_type}&crop_type=${crop_type}&nitrogen=${nitrogen}&potassium=${potassium}&phosphorus=${phosphorus}`;

    try {
        const res = await fetch(url);
        const data = await res.json();

        if (!data.success) {
            resultBox.innerHTML = "❌ " + data.error;
            return;
        }

        resultBox.innerHTML = `✅ Recommended Fertilizer: <b>${data.fertilizer}</b>`;
    } catch (e) {
        resultBox.innerHTML = "❌ Backend not reachable.";
    }
}
