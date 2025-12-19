import os
from pathlib import Path
import time
import json
import urllib.request
import urllib.error
from typing import Dict, Optional

from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("Currency Converter")

# Simple in-memory cache for rates: { base: (timestamp, rates_dict) }
_RATES_CACHE: Dict[str, tuple[float, Dict[str, float]]] = {}
# Cache TTL in seconds
CACHE_TTL = 60 * 60  # 1 hour


def _fetch_rates_from_api(base: str, api_key: str) -> Dict[str, float]:
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base}"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            if resp.status != 200:
                raise RuntimeError(f"API request failed with status {resp.status}")
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP error from API: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error when contacting API: {e.reason}")
    except Exception as e:
        raise RuntimeError(f"Failed to fetch rates: {e}")

    # API returns a structure with 'result' and 'conversion_rates'
    if data.get("result") == "error":
        raise RuntimeError(f"API error: {data.get('error-type', 'unknown')}")

    rates = data.get("conversion_rates")
    if not isinstance(rates, dict):
        raise RuntimeError("Malformed API response: missing conversion_rates")

    return rates


def get_rates(base: str = "USD", api_key: Optional[str] = None, force_refresh: bool = False) -> Dict[str, float]:
    """Return conversion rates for a given base currency. Caches responses for `CACHE_TTL` seconds.

    - `api_key`: optional API key string. If not provided, environment variable `EXCHANGE_API_KEY` is used, then `DEFAULT_API_KEY`.
    - Raises RuntimeError on failure.
    """
    base = base.upper()
    now = time.time()
    if not force_refresh and base in _RATES_CACHE:
        ts, rates = _RATES_CACHE[base]
        if now - ts < CACHE_TTL:
            return rates

    # Prefer explicit api_key argument, then CURRENCY_CONVERTER_API env var, then EXCHANGE_API_KEY, then .env, then default
    env_key = os.getenv("CURRENCY_CONVERTER_API") or os.getenv("EXCHANGE_API_KEY")
    if not env_key:
        # Try loading .env from workspace root
        env_path = Path(__file__).resolve().parent / ".env"
        if env_path.exists():
            try:
                with env_path.open("r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" not in line:
                            continue
                        k, v = line.split("=", 1)
                        k = k.strip()
                        v = v.strip().strip('"').strip("'")
                        if k == "CURRENCY_CONVERTER_API":
                            env_key = v
                            os.environ["CURRENCY_CONVERTER_API"] = v
                            break
                        if k == "EXCHANGE_API_KEY" and not env_key:
                            env_key = v
                            os.environ["EXCHANGE_API_KEY"] = v
            except Exception:
                pass

    key = api_key or env_key
    rates = _fetch_rates_from_api(base, key)
    _RATES_CACHE[base] = (now, rates)
    return rates


def convert(amount: float, from_currency: str, to_currency: str, api_key: Optional[str] = None) -> float:
    """Convert `amount` from `from_currency` to `to_currency` using live rates and return numeric result."""
    if amount is None:
        raise ValueError("Amount is required")
    from_curr = from_currency.upper()
    to_curr = to_currency.upper()

    # Obtain rates with base = from_curr so we can directly multiply
    rates = get_rates(base=from_curr, api_key=api_key)
    if to_curr not in rates:
        raise ValueError(f"Unsupported currency '{to_curr}'. Available: {', '.join(sorted(rates.keys()))}")

    rate = rates[to_curr]
    return amount * rate


@mcp.tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Tool wrapper for MCP: converts and returns a formatted string."""
    try:
        result = convert(amount, from_currency, to_currency)
        return f"{amount} {from_currency.upper()} = {result:.2f} {to_currency.upper()}"
    except Exception as e:
        return f"Error: {e}"


def _cli_main():
    import argparse

    parser = argparse.ArgumentParser(description="Convert currencies using ExchangeRate-API")
    parser.add_argument("amount", type=float, nargs="?", help="Amount to convert")
    parser.add_argument("from_currency", type=str, nargs="?", help="Source currency code (e.g. USD)")
    parser.add_argument("to_currency", type=str, nargs="?", help="Target currency code (e.g. EUR)")
    parser.add_argument("--api-key", type=str, default=None, help="ExchangeRate-API key (or set EXCHANGE_API_KEY env var)")
    parser.add_argument("--serve", action="store_true", help="Run the FastMCP server instead of CLI")
    parser.add_argument("--refresh", action="store_true", help="Force refresh cached rates")
    args = parser.parse_args()

    if args.serve:
        print("Starting MCP server (Currency Converter)...")
        mcp.run()
        return

    if args.amount is None or args.from_currency is None or args.to_currency is None:
        parser.print_help()
        return

    try:
        if args.refresh:
            # bump cache by forcing refresh
            get_rates(base=args.from_currency.upper(), api_key=args.api_key, force_refresh=True)

        res = convert(args.amount, args.from_currency, args.to_currency, api_key=args.api_key)
        print(f"{args.amount} {args.from_currency.upper()} = {res:.2f} {args.to_currency.upper()}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    _cli_main()
