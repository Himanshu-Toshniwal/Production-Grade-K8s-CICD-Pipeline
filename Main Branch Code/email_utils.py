from flask_mail import Mail, Message
from flask import render_template_string
from threading import Thread

mail = Mail()

def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {e}")

def send_email(subject, recipient, html_body, app):
    """Send email with HTML body"""
    msg = Message(subject, recipients=[recipient])
    msg.html = html_body
    
    # Send asynchronously
    Thread(target=send_async_email, args=(app, msg)).start()

def send_order_confirmation_email(order, app):
    """Send order confirmation email"""
    subject = f"Order Confirmation - {order.order_number}"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .order-details {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .item {{ border-bottom: 1px solid #eee; padding: 10px 0; }}
            .total {{ font-size: 20px; font-weight: bold; color: #667eea; margin-top: 20px; }}
            .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
            .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Order Confirmed!</h1>
                <p>Thank you for your purchase</p>
            </div>
            <div class="content">
                <p>Hi {order.shipping_name},</p>
                <p>Your order has been confirmed and will be shipped soon.</p>
                
                <div class="order-details">
                    <h3>Order Details</h3>
                    <p><strong>Order Number:</strong> {order.order_number}</p>
                    <p><strong>Order Date:</strong> {order.created_at.strftime('%B %d, %Y')}</p>
                    
                    <h4 style="margin-top: 20px;">Items:</h4>
                    {''.join([f'<div class="item"><strong>{item.product.name}</strong> x {item.quantity} - ${item.price * item.quantity:.2f}</div>' for item in order.items])}
                    
                    <div class="total">
                        Total: ${order.total_amount:.2f}
                    </div>
                </div>
                
                <div class="order-details">
                    <h3>Shipping Address</h3>
                    <p>{order.shipping_address}<br>
                    {order.shipping_city}, {order.shipping_state} {order.shipping_zip}<br>
                    {order.shipping_country}</p>
                </div>
                
                <p>We'll send you another email when your order ships.</p>
                
                <center>
                    <a href="#" class="button">Track Your Order</a>
                </center>
            </div>
            <div class="footer">
                <p>© 2024 ShopEasy. All rights reserved.</p>
                <p>If you have any questions, contact us at support@shopeasy.com</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    send_email(subject, order.shipping_email, html_body, app)

def send_password_reset_email(user, reset_token, app):
    """Send password reset email"""
    subject = "Password Reset Request"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #667eea; color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
            .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔐 Password Reset</h1>
            </div>
            <div class="content">
                <p>Hi {user.username},</p>
                <p>You requested to reset your password. Click the button below to reset it:</p>
                
                <center>
                    <a href="http://localhost:5000/reset-password/{reset_token}" class="button">Reset Password</a>
                </center>
                
                <div class="warning">
                    <strong>⚠️ Security Notice:</strong><br>
                    This link will expire in 1 hour. If you didn't request this, please ignore this email.
                </div>
                
                <p>If the button doesn't work, copy and paste this link:<br>
                http://localhost:5000/reset-password/{reset_token}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    send_email(subject, user.email, html_body, app)

def send_welcome_email(user, app):
    """Send welcome email to new users"""
    subject = f"Welcome to ShopEasy, {user.username}!"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
            .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
            .features {{ background: white; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .feature-item {{ padding: 10px 0; border-bottom: 1px solid #eee; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Welcome to ShopEasy!</h1>
                <p>Your account has been created successfully</p>
            </div>
            <div class="content">
                <p>Hi {user.username},</p>
                <p>Thank you for joining ShopEasy! We're excited to have you as part of our community.</p>
                
                <div class="features">
                    <h3>What you can do now:</h3>
                    <div class="feature-item">🛍️ Browse thousands of products</div>
                    <div class="feature-item">❤️ Save items to your wishlist</div>
                    <div class="feature-item">📦 Track your orders in real-time</div>
                    <div class="feature-item">⭐ Write reviews and ratings</div>
                    <div class="feature-item">🎁 Get exclusive deals and offers</div>
                </div>
                
                <center>
                    <a href="http://localhost:5000" class="button">Start Shopping</a>
                </center>
                
                <p style="margin-top: 30px;">If you have any questions, feel free to reach out to our support team.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    send_email(subject, user.email, html_body, app)
