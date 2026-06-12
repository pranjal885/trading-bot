import sys
import argparse
from dotenv import load_dotenv
from colorama import init, Fore, Style

from bot.client import get_binance_client
from bot.orders import place_market_order, place_limit_order
from bot.validators import (
    ValidationError,
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price
)
from bot.logging_config import setup_logging

# Initialize colorama for colored terminal outputs
init(autoreset=True)

def execute_order(logger, symbol: str, side: str, order_type: str, quantity: float, price: float):
    """
    Connects to the API client, sends the order request, and displays the outcome.
    """
    try:
        # Create the testnet client wrapper
        client = get_binance_client()
        
        # Send order to Binance testnet
        if order_type == "MARKET":
            response = place_market_order(client, symbol, side, quantity)
        else:
            response = place_limit_order(client, symbol, side, quantity, price)
            
        # Extract variables from response payload
        res_symbol = response.get("symbol", symbol)
        res_side = response.get("side", side)
        res_type = response.get("type", order_type)
        res_qty = response.get("origQty", quantity)
        
        order_id = response.get("orderId", "N/A")
        status = response.get("status", "N/A")
        executed_qty = response.get("executedQty", "0")
        avg_price = response.get("avgPrice", "0.00000")
        
        # Print SUCCESS formatting exactly per requirements
        print(f"\n{Fore.GREEN}===================={Style.RESET_ALL}")
        print(f"{Fore.GREEN}ORDER SUCCESS{Style.RESET_ALL}")
        print(f"{Fore.GREEN}===================={Style.RESET_ALL}\n")
        print(f"Symbol: {res_symbol}")
        print(f"Side: {res_side}")
        print(f"Type: {res_type}")
        print(f"Quantity: {res_qty}\n")
        print(f"Order ID: {order_id}")
        print(f"Status: {status}")
        print(f"Executed Quantity: {executed_qty}")
        print(f"Average Price: {avg_price}")
        
    except Exception as e:
        reason = str(e)
        # Identify standard exception sources to give user-friendly explanations
        if "APIError" in type(e).__name__:
            reason = f"Binance API Error: {reason}"
        elif "ConnectionError" in type(e).__name__ or "requests.exceptions" in type(e).__module__:
            reason = f"Network/Connection Error. Verify Internet connection. {reason}"
        
        logger.error(f"Order Execution Failed: {reason}")
        print(f"\n{Fore.RED}ORDER FAILED{Style.RESET_ALL}")
        print(f"Reason: {reason}")
        sys.exit(1)


def run_interactive_mode(logger):
    """
    Runs an interactive terminal CLI prompting the user for order fields step-by-step
    with active validation loops.
    """
    print(f"\n{Fore.CYAN}==================================================")
    print("      Binance Futures Testnet Interactive Bot     ")
    print(f"=================================================={Style.RESET_ALL}")
    
    # 1. Prompt Symbol
    while True:
        try:
            val = input(f"{Fore.YELLOW}Enter Symbol (e.g. BTCUSDT): {Style.RESET_ALL}").strip()
            symbol = validate_symbol(val)
            break
        except ValidationError as e:
            print(f"{Fore.RED}Validation Error: {e} Please try again.{Style.RESET_ALL}")
            
    # 2. Prompt Side
    while True:
        try:
            val = input(f"{Fore.YELLOW}Enter Side (BUY or SELL): {Style.RESET_ALL}").strip()
            side = validate_side(val)
            break
        except ValidationError as e:
            print(f"{Fore.RED}Validation Error: {e} Please try again.{Style.RESET_ALL}")
            
    # 3. Prompt Order Type
    while True:
        try:
            val = input(f"{Fore.YELLOW}Enter Order Type (MARKET or LIMIT): {Style.RESET_ALL}").strip()
            order_type = validate_order_type(val)
            break
        except ValidationError as e:
            print(f"{Fore.RED}Validation Error: {e} Please try again.{Style.RESET_ALL}")
            
    # 4. Prompt Quantity
    while True:
        try:
            val = input(f"{Fore.YELLOW}Enter Quantity (e.g. 0.001): {Style.RESET_ALL}").strip()
            quantity = validate_quantity(val)
            break
        except ValidationError as e:
            print(f"{Fore.RED}Validation Error: {e} Please try again.{Style.RESET_ALL}")
            
    # 5. Prompt Price if LIMIT order
    price = None
    if order_type == "LIMIT":
        while True:
            try:
                val = input(f"{Fore.YELLOW}Enter Price (required for LIMIT): {Style.RESET_ALL}").strip()
                price = validate_price(val, order_type)
                break
            except ValidationError as e:
                print(f"{Fore.RED}Validation Error: {e} Please try again.{Style.RESET_ALL}")
                
    # Summary of parsed inputs
    print(f"\n{Fore.CYAN}--- Order Details Summary ---{Style.RESET_ALL}")
    print(f"Symbol:   {symbol}")
    print(f"Side:     {side}")
    print(f"Type:     {order_type}")
    print(f"Quantity: {quantity}")
    if price is not None:
        print(f"Price:    {price}")
    print(f"{Fore.CYAN}----------------------------{Style.RESET_ALL}")
    
    confirm = input(f"\n{Fore.YELLOW}Confirm placing order? (y/N): {Style.RESET_ALL}").strip().lower()
    if confirm not in ["y", "yes"]:
        print(f"{Fore.RED}Order placement cancelled.{Style.RESET_ALL}")
        return
        
    execute_order(logger, symbol, side, order_type, quantity, price)


def main():
    logger = setup_logging()
    load_dotenv()
    
    # Check if CLI parameters are provided. If not, trigger interactive mode.
    if len(sys.argv) == 1:
        run_interactive_mode(logger)
        return
        
    # Configure command-line argument parser
    parser = argparse.ArgumentParser(
        description="CLI client for submitting MARKET/LIMIT orders on Binance Futures Testnet (USDT-M)."
    )
    parser.add_argument("--symbol", type=str, help="Contract symbol, e.g., BTCUSDT")
    parser.add_argument("--side", type=str, help="BUY or SELL")
    parser.add_argument("--type", type=str, help="MARKET or LIMIT")
    parser.add_argument("--quantity", type=str, help="Quantity to trade")
    parser.add_argument("--price", type=str, default=None, help="Price of limit order (required for LIMIT type)")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive user inputs menu")
    
    args = parser.parse_args()
    
    if args.interactive:
        run_interactive_mode(logger)
        return
        
    # Ensure all required inputs (symbol, side, type, quantity) are present for CLI mode
    missing_fields = []
    if not args.symbol: missing_fields.append("--symbol")
    if not args.side: missing_fields.append("--side")
    if not args.type: missing_fields.append("--type")
    if not args.quantity: missing_fields.append("--quantity")
    
    if missing_fields:
        logger.error(f"CLI Missing required options: {', '.join(missing_fields)}")
        print(f"{Fore.RED}ORDER FAILED{Style.RESET_ALL}")
        print(f"Reason: Missing required CLI arguments: {', '.join(missing_fields)}")
        print("Use 'python cli.py --help' to see all usage options or run without arguments for interactive mode.")
        sys.exit(1)
        
    # Validate the CLI parameters
    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price, order_type)
    except ValidationError as e:
        logger.error(f"CLI Validation error: {e}")
        print(f"\n{Fore.RED}ORDER FAILED{Style.RESET_ALL}")
        print(f"Reason: {e}")
        sys.exit(1)
        
    # Execute validated order
    execute_order(logger, symbol, side, order_type, quantity, price)


if __name__ == "__main__":
    main()
