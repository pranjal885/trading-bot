from binance.client import Client
from binance.exceptions import BinanceAPIException
from bot.logging_config import setup_logging

logger = setup_logging()

def place_market_order(client: Client, symbol: str, side: str, quantity: float) -> dict:
    """
    Places a MARKET order on Binance Futures Testnet.
    
    Parameters:
        client (Client): An initialized Binance API client.
        symbol (str): The trade pair symbol (e.g. 'BTCUSDT').
        side (str): The order side ('BUY' or 'SELL').
        quantity (float): The trade quantity.
        
    Returns:
        dict: The response dictionary from the Binance API.
    """
    logger.info(f"Preparing MARKET order: {side} {quantity} {symbol}")
    
    try:
        # Construct and send the market order request
        response = client.futures_create_order(
            symbol=symbol.upper(),
            side=side.upper(),
            type="MARKET",
            quantity=quantity
        )
        
        logger.info(f"MARKET order placed successfully. API Response: {response}")
        return response
        
    except BinanceAPIException as e:
        logger.error(f"Binance API Exception while placing MARKET order: Code: {e.status_code}, Message: {e.message}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error while placing MARKET order: {str(e)}")
        raise e


def place_limit_order(client: Client, symbol: str, side: str, quantity: float, price: float) -> dict:
    """
    Places a LIMIT order on Binance Futures Testnet with Time in Force 'GTC'.
    
    Parameters:
        client (Client): An initialized Binance API client.
        symbol (str): The trade pair symbol (e.g. 'BTCUSDT').
        side (str): The order side ('BUY' or 'SELL').
        quantity (float): The trade quantity.
        price (float): The order price.
        
    Returns:
        dict: The response dictionary from the Binance API.
    """
    logger.info(f"Preparing LIMIT order: {side} {quantity} {symbol} at price {price}")
    
    try:
        # Limit orders on futures require a timeInForce parameter. GTC (Good 'Til Cancelled) is standard.
        response = client.futures_create_order(
            symbol=symbol.upper(),
            side=side.upper(),
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price
        )
        
        logger.info(f"LIMIT order placed successfully. API Response: {response}")
        return response
        
    except BinanceAPIException as e:
        logger.error(f"Binance API Exception while placing LIMIT order: Code: {e.status_code}, Message: {e.message}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error while placing LIMIT order: {str(e)}")
        raise e
