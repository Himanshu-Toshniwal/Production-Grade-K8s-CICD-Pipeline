# Orders Page Template

ORDERS_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Orders - ShopEasy</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        .order-card:hover { transform: translateY(-2px); transition: all 0.3s; }
        .status-badge {
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }
        .status-pending { background: #fef3c7; color: #92400e; }
        .status-confirmed { background: #dbeafe; color: #1e40af; }
        .status-shipped { background: #e0e7ff; color: #4338ca; }
        .status-delivered { background: #d1fae5; color: #065f46; }
        .status-cancelled { background: #fee2e2; color: #991b1b; }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Navigation -->
    <nav class="bg-white shadow-lg">
        <div class="max-w-7xl mx-auto px-4 py-4">
            <div class="flex justify-between items-center">
                <div class="flex items-center">
                    <i class="fas fa-shopping-bag text-blue-600 text-2xl mr-2"></i>
                    <span class="text-xl font-bold">ShopEasy</span>
                </div>
                <div class="flex space-x-4">
                    <a href="/" class="text-gray-600 hover:text-blue-600">
                        <i class="fas fa-home mr-2"></i>Home
                    </a>
                    <a href="/orders" class="text-blue-600 font-semibold">
                        <i class="fas fa-box mr-2"></i>My Orders
                    </a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Orders Section -->
    <section class="max-w-7xl mx-auto px-4 py-12">
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-800 mb-2">My Orders</h1>
            <p class="text-gray-600">Track and manage your orders</p>
        </div>

        {% if orders %}
            <div class="space-y-4">
                {% for order in orders %}
                <div class="bg-white rounded-lg shadow-md p-6 order-card">
                    <div class="flex justify-between items-start mb-4">
                        <div>
                            <h3 class="text-lg font-semibold text-gray-800">Order #{{ order.order_number }}</h3>
                            <p class="text-sm text-gray-500">{{ order.created_at.strftime('%B %d, %Y at %I:%M %p') }}</p>
                        </div>
                        <div class="text-right">
                            <span class="status-badge status-{{ order.status }}">
                                {{ order.status.upper() }}
                            </span>
                            <p class="text-lg font-bold text-green-600 mt-2">${{ "%.2f"|format(order.total_amount) }}</p>
                        </div>
                    </div>

                    <!-- Order Items -->
                    <div class="border-t border-gray-200 pt-4 mb-4">
                        <h4 class="font-semibold mb-3">Items:</h4>
                        <div class="space-y-2">
                            {% for item in order.items %}
                            <div class="flex items-center justify-between">
                                <div class="flex items-center">
                                    <img src="{{ item.product.image_url }}" alt="{{ item.product.name }}" 
                                         class="w-12 h-12 object-cover rounded mr-3">
                                    <div>
                                        <p class="font-medium">{{ item.product.name }}</p>
                                        <p class="text-sm text-gray-500">Qty: {{ item.quantity }}</p>
                                    </div>
                                </div>
                                <p class="font-semibold">${{ "%.2f"|format(item.price * item.quantity) }}</p>
                            </div>
                            {% endfor %}
                        </div>
                    </div>

                    <!-- Shipping Info -->
                    <div class="border-t border-gray-200 pt-4 mb-4">
                        <h4 class="font-semibold mb-2">Shipping Address:</h4>
                        <p class="text-sm text-gray-600">
                            {{ order.shipping_name }}<br>
                            {{ order.shipping_address }}<br>
                            {{ order.shipping_city }}, {{ order.shipping_state }} {{ order.shipping_zip }}<br>
                            {{ order.shipping_country }}
                        </p>
                    </div>

                    <!-- Order Status Timeline -->
                    <div class="border-t border-gray-200 pt-4">
                        <h4 class="font-semibold mb-3">Order Status:</h4>
                        <div class="flex items-center justify-between">
                            <div class="flex-1 text-center">
                                <div class="w-8 h-8 mx-auto rounded-full flex items-center justify-center
                                    {{ 'bg-green-500 text-white' if order.status in ['confirmed', 'shipped', 'delivered'] else 'bg-gray-300' }}">
                                    <i class="fas fa-check text-sm"></i>
                                </div>
                                <p class="text-xs mt-1">Confirmed</p>
                            </div>
                            <div class="flex-1 h-1 {{ 'bg-green-500' if order.status in ['shipped', 'delivered'] else 'bg-gray-300' }}"></div>
                            <div class="flex-1 text-center">
                                <div class="w-8 h-8 mx-auto rounded-full flex items-center justify-center
                                    {{ 'bg-green-500 text-white' if order.status in ['shipped', 'delivered'] else 'bg-gray-300' }}">
                                    <i class="fas fa-truck text-sm"></i>
                                </div>
                                <p class="text-xs mt-1">Shipped</p>
                            </div>
                            <div class="flex-1 h-1 {{ 'bg-green-500' if order.status == 'delivered' else 'bg-gray-300' }}"></div>
                            <div class="flex-1 text-center">
                                <div class="w-8 h-8 mx-auto rounded-full flex items-center justify-center
                                    {{ 'bg-green-500 text-white' if order.status == 'delivered' else 'bg-gray-300' }}">
                                    <i class="fas fa-home text-sm"></i>
                                </div>
                                <p class="text-xs mt-1">Delivered</p>
                            </div>
                        </div>
                    </div>

                    <!-- Payment Status -->
                    <div class="border-t border-gray-200 pt-4 mt-4">
                        <div class="flex justify-between items-center">
                            <div>
                                <p class="text-sm text-gray-600">Payment Status:</p>
                                <span class="inline-block px-3 py-1 rounded-full text-sm font-semibold
                                    {{ 'bg-green-100 text-green-800' if order.payment_status == 'completed' else 'bg-yellow-100 text-yellow-800' }}">
                                    {{ order.payment_status.upper() }}
                                </span>
                            </div>
                            <div>
                                <p class="text-sm text-gray-600">Email sent to:</p>
                                <p class="font-medium">{{ order.shipping_email }}</p>
                            </div>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="bg-white rounded-lg shadow-md p-12 text-center">
                <i class="fas fa-box-open text-6xl text-gray-300 mb-4"></i>
                <h3 class="text-xl font-semibold text-gray-800 mb-2">No Orders Yet</h3>
                <p class="text-gray-600 mb-6">Start shopping to see your orders here!</p>
                <a href="/" class="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
                    <i class="fas fa-shopping-bag mr-2"></i>Start Shopping
                </a>
            </div>
        {% endif %}
    </section>

    <!-- Footer -->
    <footer class="bg-gray-800 text-white py-8 mt-12">
        <div class="max-w-7xl mx-auto px-4 text-center">
            <p>&copy; 2024 ShopEasy. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
"""
