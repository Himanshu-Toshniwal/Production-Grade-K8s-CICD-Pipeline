// Admin Dashboard JavaScript

let currentTab = 'products';

document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
    loadOrders();
    loadUsers();
});

// ==================== TAB MANAGEMENT ====================

function showTab(tab) {
    // Hide all tabs
    document.getElementById('productsTab').classList.add('hidden');
    document.getElementById('ordersTab').classList.add('hidden');
    document.getElementById('usersTab').classList.add('hidden');
    
    // Show selected tab
    document.getElementById(tab + 'Tab').classList.remove('hidden');
    currentTab = tab;
    
    // Update tab buttons
    document.querySelectorAll('nav button').forEach(btn => {
        btn.classList.remove('text-blue-600', 'border-b-2', 'border-blue-600');
        btn.classList.add('text-gray-600');
    });
    
    event.target.classList.remove('text-gray-600');
    event.target.classList.add('text-blue-600', 'border-b-2', 'border-blue-600');
}

// ==================== PRODUCTS MANAGEMENT ====================

async function loadProducts() {
    try {
        const response = await fetch('/api/admin/products');
        const products = await response.json();
        renderProductsTable(products);
    } catch (error) {
        console.error('Failed to load products:', error);
    }
}

function renderProductsTable(products) {
    const table = document.getElementById('productsTable');
    
    if (products.length === 0) {
        table.innerHTML = '<p class="text-gray-500 text-center py-8">No products found</p>';
        return;
    }
    
    table.innerHTML = `
        <div class="overflow-x-auto">
            <table class="min-w-full bg-white border">
                <thead class="bg-gray-100">
                    <tr>
                        <th class="px-4 py-2 border text-left">ID</th>
                        <th class="px-4 py-2 border text-left">Name</th>
                        <th class="px-4 py-2 border text-left">Category</th>
                        <th class="px-4 py-2 border text-left">Price</th>
                        <th class="px-4 py-2 border text-left">Stock</th>
                        <th class="px-4 py-2 border text-left">Rating</th>
                        <th class="px-4 py-2 border text-left">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${products.map(product => `
                        <tr class="hover:bg-gray-50">
                            <td class="px-4 py-2 border">${product.id}</td>
                            <td class="px-4 py-2 border">${product.name}</td>
                            <td class="px-4 py-2 border">${product.category}</td>
                            <td class="px-4 py-2 border">$${product.price}</td>
                            <td class="px-4 py-2 border">
                                <span class="px-2 py-1 rounded text-xs ${product.stock > 0 ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}">
                                    ${product.stock}
                                </span>
                            </td>
                            <td class="px-4 py-2 border">${product.rating}</td>
                            <td class="px-4 py-2 border">
                                <button onclick="editProduct(${product.id})" class="text-blue-600 hover:text-blue-800 mr-2">
                                    <i class="fas fa-edit"></i>
                                </button>
                                <button onclick="deleteProduct(${product.id})" class="text-red-600 hover:text-red-800">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

function showAddProductModal() {
    const modal = `
        <div id="productModal" class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
            <div class="bg-white rounded-lg w-full max-w-2xl mx-4 max-h-screen overflow-y-auto">
                <div class="p-6 border-b flex justify-between items-center">
                    <h3 class="text-lg font-semibold">Add New Product</h3>
                    <button onclick="closeProductModal()" class="text-gray-500 hover:text-gray-700">
                        <i class="fas fa-times text-xl"></i>
                    </button>
                </div>
                <div class="p-6">
                    <form id="productForm" onsubmit="saveProduct(event)">
                        <div class="grid grid-cols-2 gap-4 mb-4">
                            <div>
                                <label class="block text-sm font-medium mb-2">Product Name</label>
                                <input type="text" id="productName" required class="w-full px-3 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block text-sm font-medium mb-2">Category</label>
                                <select id="productCategory" class="w-full px-3 py-2 border rounded-lg">
                                    <option value="Electronics">Electronics</option>
                                    <option value="Fashion">Fashion</option>
                                    <option value="Home">Home</option>
                                    <option value="Sports">Sports</option>
                                    <option value="Books">Books</option>
                                    <option value="Toys">Toys</option>
                                </select>
                            </div>
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium mb-2">Description</label>
                            <textarea id="productDescription" rows="3" class="w-full px-3 py-2 border rounded-lg"></textarea>
                        </div>
                        <div class="grid grid-cols-2 gap-4 mb-4">
                            <div>
                                <label class="block text-sm font-medium mb-2">Price ($)</label>
                                <input type="number" id="productPrice" step="0.01" required class="w-full px-3 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block text-sm font-medium mb-2">Stock</label>
                                <input type="number" id="productStock" required class="w-full px-3 py-2 border rounded-lg">
                            </div>
                        </div>
                        <div class="mb-4">
                            <label class="block text-sm font-medium mb-2">Image URL</label>
                            <input type="url" id="productImage" placeholder="Leave empty for category default" class="w-full px-3 py-2 border rounded-lg">
                            <p class="text-xs text-gray-500 mt-1">Leave empty to use category-specific default image</p>
                        </div>
                        <div class="mb-6">
                            <label class="block text-sm font-medium mb-2">Features (comma-separated)</label>
                            <input type="text" id="productFeatures" placeholder="Feature 1, Feature 2, Feature 3" class="w-full px-3 py-2 border rounded-lg">
                        </div>
                        <button type="submit" class="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700">
                            <i class="fas fa-save mr-2"></i>Save Product
                        </button>
                    </form>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modal);
}

function closeProductModal() {
    document.getElementById('productModal')?.remove();
}

async function saveProduct(event) {
    event.preventDefault();
    
    const category = document.getElementById('productCategory').value;
    let imageUrl = document.getElementById('productImage').value;
    
    // If no image URL provided, use category-specific default
    if (!imageUrl) {
        const categoryImages = {
            'Electronics': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400&h=300&fit=crop',
            'Fashion': 'https://images.unsplash.com/photo-1445205170230-053b83016050?w=400&h=300&fit=crop',
            'Home': 'https://images.unsplash.com/photo-1484101403633-562f891dc89a?w=400&h=300&fit=crop',
            'Sports': 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=400&h=300&fit=crop',
            'Books': 'https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400&h=300&fit=crop',
            'Toys': 'https://images.unsplash.com/photo-1558060370-d644479cb6f7?w=400&h=300&fit=crop'
        };
        imageUrl = categoryImages[category] || 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop';
    }
    
    const productData = {
        name: document.getElementById('productName').value,
        description: document.getElementById('productDescription').value,
        price: document.getElementById('productPrice').value,
        stock: document.getElementById('productStock').value,
        category: category,
        image_url: imageUrl,
        features: document.getElementById('productFeatures').value
    };
    
    try {
        const response = await fetch('/api/admin/products', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(productData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Product added successfully!', 'success');
            closeProductModal();
            loadProducts();
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        showNotification('Failed to add product', 'error');
    }
}

async function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) return;
    
    try {
        const response = await fetch(`/api/admin/products/${productId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Product deleted successfully!', 'success');
            loadProducts();
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        showNotification('Failed to delete product', 'error');
    }
}

// ==================== ORDERS MANAGEMENT ====================

async function loadOrders() {
    try {
        const response = await fetch('/api/admin/orders');
        const orders = await response.json();
        renderOrdersTable(orders);
    } catch (error) {
        console.error('Failed to load orders:', error);
    }
}

function renderOrdersTable(orders) {
    const table = document.getElementById('ordersTable');
    
    if (orders.length === 0) {
        table.innerHTML = '<p class="text-gray-500 text-center py-8">No orders found</p>';
        return;
    }
    
    table.innerHTML = `
        <div class="overflow-x-auto">
            <table class="min-w-full bg-white border">
                <thead class="bg-gray-100">
                    <tr>
                        <th class="px-4 py-2 border text-left">Order #</th>
                        <th class="px-4 py-2 border text-left">Customer</th>
                        <th class="px-4 py-2 border text-left">Amount</th>
                        <th class="px-4 py-2 border text-left">Status</th>
                        <th class="px-4 py-2 border text-left">Payment</th>
                        <th class="px-4 py-2 border text-left">Date</th>
                        <th class="px-4 py-2 border text-left">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${orders.map(order => `
                        <tr class="hover:bg-gray-50">
                            <td class="px-4 py-2 border font-mono text-sm">${order.order_number}</td>
                            <td class="px-4 py-2 border">${order.user_email}</td>
                            <td class="px-4 py-2 border">$${order.total_amount.toFixed(2)}</td>
                            <td class="px-4 py-2 border">
                                <select onchange="updateOrderStatus(${order.id}, this.value)" 
                                        class="px-2 py-1 rounded text-xs border ${getStatusColor(order.status)}">
                                    <option value="pending" ${order.status === 'pending' ? 'selected' : ''}>Pending</option>
                                    <option value="confirmed" ${order.status === 'confirmed' ? 'selected' : ''}>Confirmed</option>
                                    <option value="shipped" ${order.status === 'shipped' ? 'selected' : ''}>Shipped</option>
                                    <option value="delivered" ${order.status === 'delivered' ? 'selected' : ''}>Delivered</option>
                                    <option value="cancelled" ${order.status === 'cancelled' ? 'selected' : ''}>Cancelled</option>
                                </select>
                            </td>
                            <td class="px-4 py-2 border">
                                <span class="px-2 py-1 rounded text-xs ${order.payment_status === 'completed' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}">
                                    ${order.payment_status}
                                </span>
                            </td>
                            <td class="px-4 py-2 border text-sm">${order.created_at}</td>
                            <td class="px-4 py-2 border">
                                <button onclick="viewOrderDetails(${order.id})" class="text-blue-600 hover:text-blue-800">
                                    <i class="fas fa-eye"></i>
                                </button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

function getStatusColor(status) {
    const colors = {
        'pending': 'bg-yellow-100 text-yellow-800',
        'confirmed': 'bg-blue-100 text-blue-800',
        'shipped': 'bg-purple-100 text-purple-800',
        'delivered': 'bg-green-100 text-green-800',
        'cancelled': 'bg-red-100 text-red-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
}

async function updateOrderStatus(orderId, newStatus) {
    try {
        const response = await fetch(`/api/admin/orders/${orderId}/status`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({status: newStatus})
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Order status updated!', 'success');
        } else {
            showNotification(data.message, 'error');
            loadOrders(); // Reload to reset
        }
    } catch (error) {
        showNotification('Failed to update order status', 'error');
        loadOrders();
    }
}

// ==================== USERS MANAGEMENT ====================

async function loadUsers() {
    try {
        const response = await fetch('/api/admin/users');
        const users = await response.json();
        renderUsersTable(users);
    } catch (error) {
        console.error('Failed to load users:', error);
    }
}

function renderUsersTable(users) {
    const table = document.getElementById('usersTable');
    
    if (users.length === 0) {
        table.innerHTML = '<p class="text-gray-500 text-center py-8">No users found</p>';
        return;
    }
    
    table.innerHTML = `
        <div class="overflow-x-auto">
            <table class="min-w-full bg-white border">
                <thead class="bg-gray-100">
                    <tr>
                        <th class="px-4 py-2 border text-left">ID</th>
                        <th class="px-4 py-2 border text-left">Username</th>
                        <th class="px-4 py-2 border text-left">Email</th>
                        <th class="px-4 py-2 border text-left">Role</th>
                        <th class="px-4 py-2 border text-left">Orders</th>
                        <th class="px-4 py-2 border text-left">Joined</th>
                    </tr>
                </thead>
                <tbody>
                    ${users.map(user => `
                        <tr class="hover:bg-gray-50">
                            <td class="px-4 py-2 border">${user.id}</td>
                            <td class="px-4 py-2 border">${user.username}</td>
                            <td class="px-4 py-2 border">${user.email}</td>
                            <td class="px-4 py-2 border">
                                <span class="px-2 py-1 rounded text-xs ${user.is_admin ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'}">
                                    ${user.is_admin ? 'Admin' : 'Customer'}
                                </span>
                            </td>
                            <td class="px-4 py-2 border">${user.total_orders}</td>
                            <td class="px-4 py-2 border">${user.created_at}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
}

// ==================== HELPERS ====================

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
    }`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => notification.remove(), 3000);
}
