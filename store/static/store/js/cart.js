// Update cart count in navbar
function updateNavCart(count) {
    const span = document.querySelector('a.nav-link[href$="/cart/"] .badge');
    if (span) span.textContent = count;
}

// Handle all cart actions
document.addEventListener('click', async (e) => {
    // Increase quantity
    if (e.target.matches('.btn-qty-increase')) {
        const slug = e.target.dataset.slug;
        const input = document.getElementById('cart-qty-' + slug);
        input.value = parseInt(input.value || 0) + 1;
        await updateQty(slug, input.value);
    }
    // Decrease quantity
    if (e.target.matches('.btn-qty-decrease')) {
        const slug = e.target.dataset.slug;
        const input = document.getElementById('cart-qty-' + slug);
        input.value = Math.max(1, parseInt(input.value || 1) - 1);
        await updateQty(slug, input.value);
    }
    // Add to cart
    if (e.target.matches('.btn-add-to-cart')) {
        const slug = e.target.dataset.slug;
        const input = document.getElementById('qty-' + slug);
        const qty = parseInt(input.value || 1);
        try {
            const res = await axios.post(`/cart/add/${slug}/`, `qty=${qty}`, {
                headers: {'Content-Type':'application/x-www-form-urlencoded'}
            });
            if(res.data.ok){
                updateNavCart(res.data.cart_count);
                e.target.textContent = 'Added ✓';
                setTimeout(()=> e.target.textContent = 'Add to Cart', 1200);
            }
        } catch(err) {
            alert('⚠️ Failed to add to cart.');
        }
    }
    // Remove item
    if(e.target.matches('.btn-remove')) {
        const slug = e.target.dataset.slug;
        try {
            const res = await axios.post(`/cart/remove/${slug}/`, {});
            if(res.data.ok){
                const row = document.querySelector(`tr[data-slug="${slug}"]`);
                if(row) row.remove();
                updateNavCart(res.data.cart_count);
                document.getElementById('subtotal').textContent = res.data.subtotal;
            }
        } catch(err) { console.error(err); }
    }
});

// Update quantity via AJAX
async function updateQty(slug, qty){
    try{
        const res = await axios.post(`/cart/set/${slug}/`, `qty=${qty}`, {
            headers:{'Content-Type':'application/x-www-form-urlencoded'}
        });
        if(res.data.ok){
            updateNavCart(res.data.cart_count);
            const row = document.querySelector(`tr[data-slug="${slug}"]`);
            if(row) row.querySelector('.line-total').textContent = res.data.line_total;
            document.getElementById('subtotal').textContent = res.data.subtotal;
        }
    } catch(e){ console.error(e); }
}

// Checkout
function placeOrder() {
    axios.post("/checkout/")
        .then(response => {
            if (response.data.success) {
                alert("✅ Order placed successfully!");
                window.location.href = "/";
            } else {
                alert("❌ Failed to place order: " + (response.data.error || ""));
            }
        })
        .catch(error => {
            console.error(error);
            alert("⚠️ Failed to place order (server error)");
        });
}
