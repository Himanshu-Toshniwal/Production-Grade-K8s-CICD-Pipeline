// Global state
let currentUser = null;
let products = [];
let cart = [];
let wishlist = [];

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    loadProducts();
    loadCart();
});

// ==================== AUTHENTICATION ====================

async function checkAuth() {
    try {
        const response = await fetch('/api/current-user');
        const data = await response.json();
        
        if (data.authenticated) {
            currentUser = data.user;
            updateUserUI();
            loadWishlist();
        }
    } catch (error) {
        console.error('Auth check failed:', error);
    }
}

function updateUserUI() {
    if (currentUser) {
        document.getElementById('userName').textContent = currentUser.username;
        document.getElementById('userEmail').textContent = currentUser.email;
        document.getElementById('loginBtn').classList.add('hidden');
        document.getElementById('ordersBtn').classList.remove('hidden');
        document.getElementById('logoutBtn').classList.remove('hidden');
        
        if (currentUser.is_admin) {
            document.getElementById('adminBtn').classList.remove('hidden');
        }
    } else {
        document.getElementById('userName').textContent = 'Guest';
        document.getElementById('userEmail').textContent = 'Not logged in';
        document.getElementById('loginBtn').classList.remove('hidden');
        document.getElementById('ordersBtn').classList.add('hidden');
        document.getElementById('adminBtn').classList.add('hidden');
        document.getElementById('logoutBtn').classList.add('hidden');
    }
}

async function login() {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    if (!email || !password) {
        showNotification('Please fill all fields', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email, password})
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentUser = data.user;
            updateUserUI();
            hideLoginModal();
            showNotification('Login successful!', 'success');
            loadWishlist();
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        showNotification('Login failed', 'error');
    }
}

async function register() {
    const username = document.getElementById('registerUsername').value;
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    
    if (!username || !email || !password) {
        showNotification('Please fill all fields', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, email, password})
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentUser = data.user;
            updateUserUI();
            hideLoginModal();
            showNotification('Registration successful! Welcome!', 'success');
            loadWishlist();
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        showNotification('Registration failed', 'error');
    }
}

async function logout() {
    try {
        await fetch('/api/logout', {method: 'POST'});
        currentUser = null;
        wishlist = [];
        updateUserUI();
        updateWishlistUI();
        showNotification('Logged out successfully', 'success');
    } catch (error) {
        showNotification('Logout failed', 'error');
    }
}

// ==================== PRODUCTS ====================

async function loadProducts() {
    try {
        const response = await fetch('/api/products');
        products = await response.json();
        renderProducts(products);
    } catch (error) {
        console.error('Failed to load products:', error);
    }
}

function renderProducts(productsToRender) {
    const grid = document.getElementById('productsGrid');
    
    grid.innerHTML = productsToRender.map(product => `
        <div class="bg-white rounded-lg shadow-md product-card border border-gray-200 relative" data-category="${product.category}">
            ${!product.inStock ? '<div class="absolute top-2 left-2 bg-gray-500 text-white px-2 py-1 rounded text-xs">Out of Stock</div>' : ''}
            
            <button onclick="toggleWishlistItem(${product.id})" class="absolute top-2 right-2 p-2 rounded-full bg-white shadow-md">
                <i id="wishlistIcon-${product.id}" class="far fa-heart text-gray-400 hover:text-red-500"></i>
            </button>

            <img src="${product.image}" alt="${product.name}" class="w-full h-48 object-cover rounded-t-lg">
            <div class="p-4">
                <div class="flex justify-between items-start mb-2">
                    <h3 class="text-lg font-semibold text-gray-800">${product.name}</h3>
                    <span class="text-green-600 font-bold">$${product.price}</span>
                </div>
                <p class="text-gray-600 text-sm mb-3">${product.description}</p>
                
                <div class="mb-3">
                    <div class="flex flex-wrap gap-1">
                        ${product.features.map(f => `<span class="bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded">${f}</span>`).join('')}
                    </div>
                </div>
                
                <div class="flex justify-between items-center">
                    <div class="flex items-center">
                        ${renderStars(product.rating)}
                        <span class="text-sm text-gray-500 ml-1">${product.rating}</span>
                    </div>
                    <button onclick="addToCart(${product.id})" 
                            class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 ${!product.inStock ? 'opacity-50 cursor-not-allowed' : ''}"
                            ${!product.inStock ? 'disabled' : ''}>
                        <i class="fas fa-cart-plus mr-2"></i>${product.inStock ? 'Add to Cart' : 'Out of Stock'}
                    </button>
                </div>
            </div>
        </div>
    `).join('');
    
    updateWishlistIcons();
}

function renderStars(rating) {
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        stars += `<i class="fa${i <= rating ? 's' : 'r'} fa-star text-yellow-400"></i>`;
    }
    return stars;
}

function filterProducts(category) {
    // Clear search input
    const searchInput = document.getElementById('searchInput');
    if (searchInput) searchInput.value = '';
    
    // Scroll to products section
    document.getElementById('products')?.scrollIntoView({behavior: 'smooth'});
    
    if (category === 'all') {
        renderProducts(products);
    } else {
        const filtered = products.filter(p => p.category === category);
        renderProducts(filtered);
    }
    
    // Update active filter button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('bg-blue-600', 'text-white');
        btn.classList.add('bg-gray-200', 'text-gray-700');
    });
}

// Search functionality
document.getElementById('searchInput')?.addEventListener('input', function(e) {
    const searchTerm = e.target.value.toLowerCase().trim();
    
    if (searchTerm === '') {
        // Show all products if search is empty
        renderProducts(products);
        return;
    }
    
    const filtered = products.filter(p => 
        p.name.toLowerCase().includes(searchTerm) || 
        p.description.toLowerCase().includes(searchTerm) ||
        p.category.toLowerCase().includes(searchTerm) ||
        (p.features && p.features.some(f => f.toLowerCase().includes(searchTerm)))
    );
    
    renderProducts(filtered);
    
    // Show message if no results
    if (filtered.length === 0) {
        document.getElementById('productsGrid').innerHTML = `
            <div class="col-span-full text-center py-12">
                <i class="fas fa-search text-6xl text-gray-300 mb-4"></i>
                <h3 class="text-xl font-semibold text-gray-700 mb-2">No products found</h3>
                <p class="text-gray-500">Try searching with different keywords</p>
                <button onclick="document.getElementById('searchInput').value=''; renderProducts(products)" 
                        class="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700">
                    Clear Search
                </button>
            </div>
        `;
    }
});

// ==================== CART ====================

async function loadCart() {
    try {
        const response = await fetch('/api/cart');
        cart = await response.json();
        updateCartUI();
    } catch (error) {
        console.error('Failed to load cart:', error);
    }
}

async function addToCart(productId) {
    try {
        const response = await fetch('/api/cart/add', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({product_id: productId})
        });
        
        const data = await response.json();
        
        if (data.success) {
            cart = data.cart;
            updateCartUI();
            showNotification('Added to cart!', 'success');
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        showNotification('Failed to add to cart', 'error');
    }
}

async function removeFromCart(productId) {
    try {
        const response = await fetch('/api/cart/remove', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({product_id: productId})
        });
        
        const data = await response.json();
        cart = data.cart;
        updateCartUI();
    } catch (error) {
        console.error('Failed to remove from cart:', error);
    }
}

async function updateQuantity(productId, quantity) {
    if (quantity < 1) {
        removeFromCart(productId);
        return;
    }
    
    try {
        const response = await fetch('/api/cart/update', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({product_id: productId, quantity})
        });
        
        const data = await response.json();
        
        if (data.success) {
            cart = data.cart;
            updateCartUI();
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        console.error('Failed to update quantity:', error);
    }
}

function updateCartUI() {
    const cartCount = document.getElementById('cartCount');
    const cartItems = document.getElementById('cartItems');
    const cartTotal = document.getElementById('cartTotal');
    
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<div class="text-center text-gray-500 py-8"><i class="fas fa-shopping-cart text-4xl mb-4 text-gray-300"></i><p>Your cart is empty</p></div>';
    } else {
        const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        
        cartItems.innerHTML = cart.map(item => `
            <div class="flex items-center border-b border-gray-200 py-4">
                <img src="${item.image}" alt="${item.name}" class="w-16 h-16 object-cover rounded">
                <div class="flex-1 ml-4">
                    <h4 class="font-semibold">${item.name}</h4>
                    <p class="text-green-600 font-bold">$${item.price}</p>
                    <div class="flex items-center mt-2">
                        <button onclick="updateQuantity(${item.id}, ${item.quantity - 1})" class="px-2 py-1 bg-gray-200 rounded-l">-</button>
                        <span class="px-3 py-1 bg-gray-100">${item.quantity}</span>
                        <button onclick="updateQuantity(${item.id}, ${item.quantity + 1})" class="px-2 py-1 bg-gray-200 rounded-r">+</button>
                        <button onclick="removeFromCart(${item.id})" class="ml-4 text-red-500 hover:text-red-700">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
        
        cartTotal.textContent = `$${total.toFixed(2)}`;
    }
}

function toggleCart() {
    const sidebar = document.getElementById('cartSidebar');
    const overlay = document.getElementById('overlay');
    sidebar.classList.toggle('active');
    overlay.classList.toggle('hidden');
}

// ==================== WISHLIST ====================

async function loadWishlist() {
    if (!currentUser) return;
    
    try {
        const response = await fetch('/api/wishlist');
        wishlist = await response.json();
        updateWishlistUI();
        updateWishlistIcons();
    } catch (error) {
        console.error('Failed to load wishlist:', error);
    }
}

async function toggleWishlistItem(productId) {
    if (!currentUser) {
        showNotification('Please login to use wishlist', 'error');
        showLoginModal();
        return;
    }
    
    try {
        const response = await fetch('/api/wishlist/toggle', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({product_id: productId})
        });
        
        const data = await response.json();
        
        if (data.success) {
            wishlist = data.wishlist;
            updateWishlistUI();
            updateWishlistIcons();
            showNotification(data.message, 'success');
        }
    } catch (error) {
        showNotification('Failed to update wishlist', 'error');
    }
}

function updateWishlistUI() {
    const wishlistCount = document.getElementById('wishlistCount');
    const wishlistItems = document.getElementById('wishlistItems');
    
    wishlistCount.textContent = wishlist.length;
    
    if (wishlist.length === 0) {
        wishlistItems.innerHTML = '<div class="text-center text-gray-500 py-8"><i class="fas fa-heart text-4xl mb-4 text-gray-300"></i><p>Your wishlist is empty</p></div>';
    } else {
        wishlistItems.innerHTML = wishlist.map(item => `
            <div class="flex items-center border-b border-gray-200 py-4">
                <img src="${item.image}" alt="${item.name}" class="w-16 h-16 object-cover rounded">
                <div class="flex-1 ml-4">
                    <h4 class="font-semibold">${item.name}</h4>
                    <p class="text-green-600 font-bold">$${item.price}</p>
                    <div class="flex space-x-2 mt-2">
                        <button onclick="addToCart(${item.id})" class="flex-1 bg-blue-600 text-white py-1 px-3 rounded text-sm hover:bg-blue-700">
                            Add to Cart
                        </button>
                        <button onclick="toggleWishlistItem(${item.id})" class="bg-red-500 text-white py-1 px-3 rounded text-sm hover:bg-red-600">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }
}

function updateWishlistIcons() {
    wishlist.forEach(item => {
        const icon = document.getElementById(`wishlistIcon-${item.id}`);
        if (icon) {
            icon.classList.remove('far', 'text-gray-400');
            icon.classList.add('fas', 'text-red-500');
        }
    });
}

function toggleWishlist() {
    if (!currentUser) {
        showNotification('Please login to view wishlist', 'error');
        showLoginModal();
        return;
    }
    
    const sidebar = document.getElementById('wishlistSidebar');
    const overlay = document.getElementById('overlay');
    sidebar.classList.toggle('active');
    overlay.classList.toggle('hidden');
}

// ==================== CHECKOUT ====================

function proceedToCheckout() {
    if (!currentUser) {
        showNotification('Please login to checkout', 'error');
        showLoginModal();
        return;
    }
    
    if (cart.length === 0) {
        showNotification('Your cart is empty', 'error');
        return;
    }
    
    toggleCart();
    showCheckoutModal();
}

function showCheckoutModal() {
    document.getElementById('checkoutModal').classList.remove('hidden');
    document.getElementById('overlay').classList.remove('hidden');
    
    // Pre-fill user email
    if (currentUser) {
        document.getElementById('shippingEmail').value = currentUser.email;
    }
}

function hideCheckoutModal() {
    document.getElementById('checkoutModal').classList.add('hidden');
    document.getElementById('overlay').classList.add('hidden');
}

document.getElementById('checkoutForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const shippingData = {
        shipping_name: document.getElementById('shippingName').value,
        shipping_email: document.getElementById('shippingEmail').value,
        shipping_phone: document.getElementById('shippingPhone').value,
        shipping_address: document.getElementById('shippingAddress').value,
        shipping_city: document.getElementById('shippingCity').value,
        shipping_state: document.getElementById('shippingState').value,
        shipping_zip: document.getElementById('shippingZip').value,
        shipping_country: document.getElementById('shippingCountry').value
    };
    
    try {
        const response = await fetch('/api/checkout', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(shippingData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            hideCheckoutModal();
            showNotification(`Order placed successfully! Order #${data.order_number}`, 'success');
            cart = [];
            updateCartUI();
            
            // Reset form
            document.getElementById('checkoutForm').reset();
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        showNotification('Checkout failed', 'error');
    }
});

// ==================== UI HELPERS ====================

function toggleUserMenu() {
    document.getElementById('userMenu').classList.toggle('hidden');
}

function showLoginModal() {
    document.getElementById('loginModal').classList.remove('hidden');
    document.getElementById('overlay').classList.remove('hidden');
    showLoginForm();
}

function hideLoginModal() {
    document.getElementById('loginModal').classList.add('hidden');
    document.getElementById('overlay').classList.add('hidden');
}

function showLoginForm() {
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('registerForm').classList.add('hidden');
    document.getElementById('modalTitle').textContent = 'Login';
}

function showRegisterForm() {
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.remove('hidden');
    document.getElementById('modalTitle').textContent = 'Register';
}

function showOrders() {
    window.location.href = '/orders';
}

function showAdminPanel() {
    window.location.href = '/admin';
}

function scrollToProducts() {
    document.getElementById('products').scrollIntoView({behavior: 'smooth'});
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
    }`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 3000);
}

// Close overlay on click
document.getElementById('overlay')?.addEventListener('click', function() {
    document.getElementById('cartSidebar').classList.remove('active');
    document.getElementById('wishlistSidebar').classList.remove('active');
    document.getElementById('loginModal').classList.add('hidden');
    document.getElementById('checkoutModal').classList.add('hidden');
    this.classList.add('hidden');
});
