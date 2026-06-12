import os
from binance.client import Client
from binance.exceptions import BinanceAPIException
from bot.logging_config import setup_logging

logger = setup_logging()

def get_binance_client() -> Client:
    """
    Initializes a python-binance Client configured for Futures Testnet.
    Credentials are read from environment variables.
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        err_msg = "BINANCE_API_KEY or BINANCE_API_SECRET is missing from the environment configuration."
        logger.error(f"Authentication Failure: {err_msg}")
        raise ValueError(err_msg)
        
    try:
        logger.info("Initializing Binance Futures Testnet Client...")
        # Initialize client with testnet enabled
        client = Client(api_key, api_secret, testnet=True)
        
        # Test connection by pinging the futures server
        client.futures_ping()
        logger.info("Successfully connected and authenticated with Binance Futures Testnet.")
        return client
        
    except BinanceAPIException as e:
        logger.error(f"Binance API Exception during client initialization: {e.status_code} - {e.message}")
        raise e
    except Exception as e:
        logger.error(f"Network or connection error during client initialization: {str(e)}")
        raise ConnectionError(f"Could not connect to Binance Futures Testnet: {str(e)}")
