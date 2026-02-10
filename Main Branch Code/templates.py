# HTML Templates for the application

MAIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShopEasy - Enhanced E-commerce</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .product-card:hover { transform: translateY(-5px); transition: all 0.3s ease; }
        .cart-badge, .wishlist-badge { position: absolute; top: -8px; right: -8px; background: #ef4444; color: white; border-radius: 50%; width: 20px; height: 20px; font-size: 12px; display: flex; align-items: center; justify-content: center; }
        .wishlist-badge { background: #10b981; left: -8px; right: auto; }
        .sidebar { transform: translateX(100%); transition: transform 0.3s; }
        .sidebar.active { transform: translateX(0); }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between items-center py-4">
                <div class="flex items-center">
                    <i class="fas fa-shopping-bag text-blue-600 text-2xl mr-2"></i>
                    <span class="text-xl font-bold text-gray-800">ShopEasy</span>
                </div>
                
                <div class="flex-1 max-w-2xl mx-4">
                    <div class="relative">
                        <input type="text" id="searchInput" placeholder="Search products..." 
                               class="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:border-blue-500">
                        <i class="fas fa-search absolute right-3 top-3 text-gray-400"></i>
                    </div>
                </div>

                <div class="flex space-x-4">
                    <div class="relative">
                        <button onclick="toggleWishlist()" class="p-2 text-gray-600 hover:text-red-500 relative">
                            <i class="fas fa-heart text-xl"></i>
                            <span id="wishlistCount" class="wishlist-badge">0</span>
                        </button>
                    </div>
                    <div class="relative">
                        <button onclick="toggleCart()" class="p-2 text-gray-600 hover:text-blue-600 relative">
                            <i class="fas fa-shopping-cart text-xl"></i>
                            <span id="cartCount" class="cart-badge">0</span>
                        </button>
                    </div>
                    <div class="relative">
                        <button onclick="toggleUserMenu()" id="userMenuBtn" class="p-2 text-gray-600 hover:text-green-600">
                            <i class="fas fa-user-circle text-xl"></i>
                        </button>
                        <div id="userMenu" class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border hidden z-50">
                            <div class="p-4 border-b" id="userInfo">
                                <p class="font-semibold" id="userName">Guest</p>
                                <p class="text-sm text-gray-500" id="userEmail">Not logged in</p>
                            </div>
                            <div class="p-2">
                                <button onclick="showLoginModal()" id="loginBtn" class="w-full text-left px-4 py-2 text-sm hover:bg-gray-100 rounded">
                                    <i class="fas fa-sign-in-alt mr-2"></i>Login
                                </button>
                                <a href="/orders" id="ordersBtn" class="w-full text-left px-4 py-2 text-sm hover:bg-gray-100 rounded hidden block">
                                    <i class="fas fa-box mr-2"></i>My Orders
                                </a>
                                <button onclick="showAdminPanel()" id="adminBtn" class="w-full text-left px-4 py-2 text-sm hover:bg-gray-100 rounded hidden">
                                    <i class="fas fa-cog mr-2"></i>Admin Panel
                                </button>
                                <button onclick="logout()" id="logoutBtn" class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100 rounded hidden">
                                    <i class="fas fa-sign-out-alt mr-2"></i>Logout
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-16">
        <div class="max-w-7xl mx-auto px-4 text-center">
            <h1 class="text-4xl md:text-6xl font-bold mb-4">Welcome to ShopEasy</h1>
            <p class="text-xl mb-8">🎉 Now with Database, Authentication, Payments & Admin Panel!</p>
            <button onclick="scrollToProducts()" class="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100">
                Start Shopping
            </button>
        </div>
    </section>

    <!-- Products Section -->
    <section id="products" class="max-w-7xl mx-auto px-4 py-12">
        <h2 class="text-3xl font-bold text-gray-800 mb-8 text-center">Featured Products</h2>
        
        <div class="flex flex-wrap justify-center gap-2 mb-8">
            <button onclick="filterProducts('all')" class="filter-btn px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
                <i class="fas fa-th mr-1"></i>All
            </button>
            <button onclick="filterProducts('Electronics')" class="filter-btn px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition">
                <i class="fas fa-laptop mr-1"></i>Electronics
            </button>
            <button onclick="filterProducts('Fashion')" class="filter-btn px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition">
                <i class="fas fa-tshirt mr-1"></i>Fashion
            </button>
            <button onclick="filterProducts('Home')" class="filter-btn px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition">
                <i class="fas fa-couch mr-1"></i>Home
            </button>
            <button onclick="filterProducts('Sports')" class="filter-btn px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition">
                <i class="fas fa-dumbbell mr-1"></i>Sports
            </button>
            <button onclick="filterProducts('Books')" class="filter-btn px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition">
                <i class="fas fa-book mr-1"></i>Books
            </button>
            <button onclick="filterProducts('Toys')" class="filter-btn px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition">
                <i class="fas fa-gamepad mr-1"></i>Toys
            </button>
        </div>

        <div id="productsGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"></div>
    </section>

    <!-- Cart Sidebar -->
    <div id="cartSidebar" class="fixed top-0 right-0 h-full w-96 bg-white shadow-2xl sidebar z-50">
        <div class="p-4 border-b flex justify-between items-center">
            <h3 class="text-lg font-semibold">Shopping Cart</h3>
            <button onclick="toggleCart()" class="text-gray-500 hover:text-gray-700">
                <i class="fas fa-times text-xl"></i>
            </button>
        </div>
        <div id="cartItems" class="p-4 h-3/4 overflow-y-auto"></div>
        <div class="absolute bottom-0 left-0 right-0 p-4 border-t bg-white">
            <div class="flex justify-between mb-4">
                <span class="font-semibold">Total:</span>
                <span id="cartTotal" class="font-bold text-lg">$0.00</span>
            </div>
            <button onclick="proceedToCheckout()" class="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700">
                <i class="fas fa-credit-card mr-2"></i>Checkout
            </button>
        </div>
    </div>

    <!-- Wishlist Sidebar -->
    <div id="wishlistSidebar" class="fixed top-0 right-0 h-full w-96 bg-white shadow-2xl sidebar z-50">
        <div class="p-4 border-b flex justify-between items-center">
            <h3 class="text-lg font-semibold">Wishlist</h3>
            <button onclick="toggleWishlist()" class="text-gray-500 hover:text-gray-700">
                <i class="fas fa-times text-xl"></i>
            </button>
        </div>
        <div id="wishlistItems" class="p-4 h-full overflow-y-auto"></div>
    </div>

    <!-- Login/Register Modal -->
    <div id="loginModal" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50 flex items-center justify-center">
        <div class="bg-white rounded-lg w-full max-w-md mx-4">
            <div class="p-6 border-b flex justify-between items-center">
                <h3 class="text-lg font-semibold" id="modalTitle">Login</h3>
                <button onclick="hideLoginModal()" class="text-gray-500 hover:text-gray-700">
                    <i class="fas fa-times text-xl"></i>
                </button>
            </div>
            <div class="p-6">
                <div id="loginForm">
                    <div class="mb-4">
                        <label class="block text-sm font-medium mb-2">Email</label>
                        <input type="email" id="loginEmail" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
                    </div>
                    <div class="mb-6">
                        <label class="block text-sm font-medium mb-2">Password</label>
                        <input type="password" id="loginPassword" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
                    </div>
                    <button onclick="login()" class="w-full bg-blue-600 text-white py-2 rounded-lg font-semibold hover:bg-blue-700 mb-2">
                        Login
                    </button>
                    <button onclick="showRegisterForm()" class="w-full bg-gray-200 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-300">
                        Create Account
                    </button>
                </div>
                <div id="registerForm" class="hidden">
                    <div class="mb-4">
                        <label class="block text-sm font-medium mb-2">Username</label>
                        <input type="text" id="registerUsername" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
                    </div>
                    <div class="mb-4">
                        <label class="block text-sm font-medium mb-2">Email</label>
                        <input type="email" id="registerEmail" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
                    </div>
                    <div class="mb-6">
                        <label class="block text-sm font-medium mb-2">Password</label>
                        <input type="password" id="registerPassword" class="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500">
                    </div>
                    <button onclick="register()" class="w-full bg-green-600 text-white py-2 rounded-lg font-semibold hover:bg-green-700 mb-2">
                        Register
                    </button>
                    <button onclick="showLoginForm()" class="w-full bg-gray-200 text-gray-700 py-2 rounded-lg font-semibold hover:bg-gray-300">
                        Back to Login
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- Checkout Modal -->
    <div id="checkoutModal" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50 flex items-center justify-center overflow-y-auto">
        <div class="bg-white rounded-lg w-full max-w-2xl mx-4 my-8">
            <div class="p-6 border-b flex justify-between items-center">
                <h3 class="text-lg font-semibold">Checkout</h3>
                <button onclick="hideCheckoutModal()" class="text-gray-500 hover:text-gray-700">
                    <i class="fas fa-times text-xl"></i>
                </button>
            </div>
            <div class="p-6">
                <form id="checkoutForm">
                    <h4 class="font-semibold mb-4">Shipping Information</h4>
                    <div class="grid grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium mb-2">Full Name</label>
                            <input type="text" id="shippingName" required class="w-full px-3 py-2 border rounded-lg">
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-2">Email</label>
                            <input type="email" id="shippingEmail" required class="w-full px-3 py-2 border rounded-lg">
                        </div>
                    </div>
                    <div class="mb-4">
                        <label class="block text-sm font-medium mb-2">Phone</label>
                        <input type="tel" id="shippingPhone" required class="w-full px-3 py-2 border rounded-lg">
                    </div>
                    <div class="mb-4">
                        <label class="block text-sm font-medium mb-2">Address</label>
                        <textarea id="shippingAddress" required class="w-full px-3 py-2 border rounded-lg" rows="2"></textarea>
                    </div>
                    <div class="grid grid-cols-2 gap-4 mb-4">
                        <div>
                            <label class="block text-sm font-medium mb-2">City</label>
                            <input type="text" id="shippingCity" required class="w-full px-3 py-2 border rounded-lg">
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-2">State</label>
                            <input type="text" id="shippingState" required class="w-full px-3 py-2 border rounded-lg">
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-4 mb-6">
                        <div>
                            <label class="block text-sm font-medium mb-2">ZIP Code</label>
                            <input type="text" id="shippingZip" required class="w-full px-3 py-2 border rounded-lg">
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-2">Country</label>
                            <input type="text" id="shippingCountry" required class="w-full px-3 py-2 border rounded-lg">
                        </div>
                    </div>
                    <button type="submit" class="w-full bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700">
                        <i class="fas fa-lock mr-2"></i>Place Order
                    </button>
                </form>
            </div>
        </div>
    </div>

    <div id="overlay" class="fixed inset-0 bg-black bg-opacity-50 hidden z-40"></div>

    <script src="/static/app.js"></script>
</body>
</html>
"""

ADMIN_DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard - ShopEasy</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
</head>
<body class="bg-gray-100">
    <div class="min-h-screen">
        <!-- Header -->
        <nav class="bg-white shadow-lg">
            <div class="max-w-7xl mx-auto px-4 py-4">
                <div class="flex justify-between items-center">
                    <h1 class="text-2xl font-bold text-gray-800">
                        <i class="fas fa-cog text-blue-600 mr-2"></i>Admin Dashboard
                    </h1>
                    <a href="/" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                        <i class="fas fa-home mr-2"></i>Back to Store
                    </a>
                </div>
            </div>
        </nav>

        <!-- Stats -->
        <div class="max-w-7xl mx-auto px-4 py-8">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div class="bg-white p-6 rounded-lg shadow">
                    <div class="flex items-center">
                        <div class="p-3 bg-blue-100 rounded-full">
                            <i class="fas fa-users text-blue-600 text-2xl"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-gray-500 text-sm">Total Users</p>
                            <p class="text-2xl font-bold">{{ total_users }}</p>
                        </div>
                    </div>
                </div>
                <div class="bg-white p-6 rounded-lg shadow">
                    <div class="flex items-center">
                        <div class="p-3 bg-green-100 rounded-full">
                            <i class="fas fa-box text-green-600 text-2xl"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-gray-500 text-sm">Total Products</p>
                            <p class="text-2xl font-bold">{{ total_products }}</p>
                        </div>
                    </div>
                </div>
                <div class="bg-white p-6 rounded-lg shadow">
                    <div class="flex items-center">
                        <div class="p-3 bg-purple-100 rounded-full">
                            <i class="fas fa-shopping-cart text-purple-600 text-2xl"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-gray-500 text-sm">Total Orders</p>
                            <p class="text-2xl font-bold">{{ total_orders }}</p>
                        </div>
                    </div>
                </div>
                <div class="bg-white p-6 rounded-lg shadow">
                    <div class="flex items-center">
                        <div class="p-3 bg-yellow-100 rounded-full">
                            <i class="fas fa-dollar-sign text-yellow-600 text-2xl"></i>
                        </div>
                        <div class="ml-4">
                            <p class="text-gray-500 text-sm">Total Revenue</p>
                            <p class="text-2xl font-bold">${{ "%.2f"|format(total_revenue) }}</p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tabs -->
            <div class="bg-white rounded-lg shadow mb-8">
                <div class="border-b">
                    <nav class="flex">
                        <button onclick="showTab('products')" class="px-6 py-4 font-semibold text-blue-600 border-b-2 border-blue-600">
                            Products
                        </button>
                        <button onclick="showTab('orders')" class="px-6 py-4 font-semibold text-gray-600 hover:text-blue-600">
                            Orders
                        </button>
                        <button onclick="showTab('users')" class="px-6 py-4 font-semibold text-gray-600 hover:text-blue-600">
                            Users
                        </button>
                    </nav>
                </div>

                <div class="p-6">
                    <div id="productsTab">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="text-xl font-bold">Products Management</h3>
                            <button onclick="showAddProductModal()" class="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700">
                                <i class="fas fa-plus mr-2"></i>Add Product
                            </button>
                        </div>
                        <div id="productsTable"></div>
                    </div>

                    <div id="ordersTab" class="hidden">
                        <h3 class="text-xl font-bold mb-4">Recent Orders</h3>
                        <div id="ordersTable"></div>
                    </div>

                    <div id="usersTab" class="hidden">
                        <h3 class="text-xl font-bold mb-4">Users</h3>
                        <div id="usersTable"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="/static/admin.js"></script>
</body>
</html>
"""
