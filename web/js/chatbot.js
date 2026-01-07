console.log("✅ chatbot.js loaded");

window.askChatbot = async function () {

    const input = document.getElementById("chat-input");
    const output = document.getElementById("chat-response");

    if (!input) {
        console.error("❌ chat-input not found in HTML");
        return;
    }

    const query = input.value;

    if (!query) {
        output.innerHTML = "❌ Please ask something.";
        return;
    }

    try {
        const res = await fetch("https://agrimind-oxrb.onrender.com/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query })
        });

        const data = await res.json();
        output.innerHTML = "🤖 " + data.response;

    } catch (e) {
        console.error(e);
        output.innerHTML = "❌ Backend not reachable.";
    }
};
