function getCSRFToken() {
    let cookieValue = null;
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith("csrftoken=")) {
            cookieValue = cookie.substring("csrftoken=".length);
            break;
        }
    }
    return cookieValue;
}

function placeOrder() {
    axios.post("/checkout/", {}, {
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (response.data.success) {
            alert("✅ Order placed successfully!");
            window.location.href = response.data.redirect || "/"; // fallback
        } else {
            alert("❌ Failed to place order: " + (response.data.error || "Unknown error"));
        }
    })
    .catch(error => {
        console.error("Checkout error:", error);
        alert("⚠️ Server error while placing order.");
    });
}
