document.addEventListener('click', async (e) => {
  // Increase quantity
  if(e.target.matches('.btn-qty-increase')){
    const slug = e.target.dataset.slug;
    const input = document.getElementById('qty-'+slug);
    input.value = parseInt(input.value || 0) + 1;
  }

  // Decrease quantity
  if(e.target.matches('.btn-qty-decrease')){
    const slug = e.target.dataset.slug;
    const input = document.getElementById('qty-'+slug);
    input.value = Math.max(1, parseInt(input.value || 1) - 1);
  }

  // Add to cart
  if(e.target.matches('.btn-add-to-cart')){
    const slug = e.target.dataset.slug;
    const input = document.getElementById('qty-'+slug);
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
    } catch(err){
      alert('Failed to add to cart.');
      console.error(err);
    }
  }
});

// Update cart count in navbar
function updateNavCart(count){
  const badge = document.querySelector('.navbar .badge');
  if(badge) badge.textContent = count;
}
