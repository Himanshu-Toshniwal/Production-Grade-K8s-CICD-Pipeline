import stripe
from flask import current_app

def init_stripe():
    """Initialize Stripe with secret key"""
    stripe.api_key = current_app.config['STRIPE_SECRET_KEY']

def create_payment_intent(amount, currency='usd', metadata=None):
    """
    Create a Stripe payment intent
    
    Args:
        amount: Amount in cents (e.g., 1000 = $10.00)
        currency: Currency code (default: 'usd')
        metadata: Additional data to attach to payment
    
    Returns:
        Payment intent object or None if error
    """
    try:
        init_stripe()
        
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Convert to cents
            currency=currency,
            metadata=metadata or {},
            automatic_payment_methods={
                'enabled': True,
            }
        )
        
        return intent
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return None

def confirm_payment(payment_intent_id):
    """
    Confirm a payment intent
    
    Args:
        payment_intent_id: Stripe payment intent ID
    
    Returns:
        True if successful, False otherwise
    """
    try:
        init_stripe()
        
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if intent.status == 'succeeded':
            return True
        
        return False
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return False

def create_checkout_session(line_items, success_url, cancel_url, metadata=None):
    """
    Create a Stripe checkout session
    
    Args:
        line_items: List of items with price and quantity
        success_url: URL to redirect after successful payment
        cancel_url: URL to redirect if payment cancelled
        metadata: Additional data
    
    Returns:
        Checkout session object or None if error
    """
    try:
        init_stripe()
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
            metadata=metadata or {}
        )
        
        return session
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return None

def refund_payment(payment_intent_id, amount=None):
    """
    Refund a payment
    
    Args:
        payment_intent_id: Stripe payment intent ID
        amount: Amount to refund in cents (None = full refund)
    
    Returns:
        Refund object or None if error
    """
    try:
        init_stripe()
        
        refund_params = {'payment_intent': payment_intent_id}
        if amount:
            refund_params['amount'] = int(amount * 100)
        
        refund = stripe.Refund.create(**refund_params)
        
        return refund
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return None

def get_payment_status(payment_intent_id):
    """
    Get payment status
    
    Args:
        payment_intent_id: Stripe payment intent ID
    
    Returns:
        Status string or None if error
    """
    try:
        init_stripe()
        
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return intent.status
    except stripe.error.StripeError as e:
        print(f"Stripe error: {e}")
        return None
