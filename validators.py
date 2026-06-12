class ValidationError(ValueError):
    """Exception raised when CLI or interactive input fails validation checks."""
    pass

def validate_symbol(symbol: str) -> str:
    """
    Validates that the symbol is non-empty and a valid string format.
    """
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol cannot be empty and must be a string.")
    
    cleaned = symbol.strip().upper()
    if not cleaned:
        raise ValidationError("Symbol cannot consist only of spaces.")
    
    return cleaned

def validate_side(side: str) -> str:
    """
    Validates that the trade side is either BUY or SELL.
    """
    if not side or not isinstance(side, str):
        raise ValidationError("Trade side must be a string (BUY or SELL).")
        
    cleaned = side.strip().upper()
    if cleaned not in ["BUY", "SELL"]:
        raise ValidationError(f"Invalid side '{cleaned}'. Must be 'BUY' or 'SELL'.")
        
    return cleaned

def validate_order_type(order_type: str) -> str:
    """
    Validates that the order type is either MARKET or LIMIT.
    """
    if not order_type or not isinstance(order_type, str):
        raise ValidationError("Order type must be a string (MARKET or LIMIT).")
        
    cleaned = order_type.strip().upper()
    if cleaned not in ["MARKET", "LIMIT"]:
        raise ValidationError(f"Invalid order type '{cleaned}'. Must be 'MARKET' or 'LIMIT'.")
        
    return cleaned

def validate_quantity(quantity_str: str) -> float:
    """
    Validates that the quantity is a positive float number.
    """
    if quantity_str is None:
        raise ValidationError("Quantity is required.")
        
    try:
        quantity = float(quantity_str)
    except ValueError:
        raise ValidationError(f"Invalid quantity '{quantity_str}'. It must be a valid number.")
        
    if quantity <= 0:
        raise ValidationError(f"Quantity must be strictly greater than 0. Got: {quantity}")
        
    return quantity

def validate_price(price_str: str, order_type: str) -> float:
    """
    Validates the price parameter.
    Required and must be > 0 for LIMIT orders.
    Optional and ignored/validated if passed for MARKET orders.
    """
    order_type_upper = order_type.strip().upper()
    
    if order_type_upper == "LIMIT":
        if price_str is None or price_str == "":
            raise ValidationError("Price is required for LIMIT orders.")
        try:
            price = float(price_str)
        except ValueError:
            raise ValidationError(f"Invalid price '{price_str}'. It must be a valid number for LIMIT orders.")
            
        if price <= 0:
            raise ValidationError(f"Price must be strictly greater than 0 for LIMIT orders. Got: {price}")
        return price
        
    else:  # MARKET order
        if price_str is not None and price_str != "":
            # If user provided a price for a market order, we validate it but warn or return it
            try:
                price = float(price_str)
                if price <= 0:
                    raise ValidationError(f"If price is provided for MARKET orders, it must be greater than 0. Got: {price}")
                return price
            except ValueError:
                raise ValidationError(f"Invalid price '{price_str}'. It must be a valid number.")
        return None
