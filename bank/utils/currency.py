from STINBank.utils.config import get_bank_config

CURRENCIES = {
    'CZK': 'koruna (CZK)',
    'AUD': 'dolar (AUD)',
    'BRL': 'real (BRL)',
    'BGN': 'lev (BGN)',
    'CNY': 'žen-min-pi (CNY)',
    'DKK': 'koruna (DKK)',
    'EUR': 'euro (EUR)',
    'PHP': 'peso (PHP)',
    'HKD': 'dolar (HKD)',
    'INR': 'rupie (INR)',
    'IDR': 'rupie (IDR)',
    'ISK': 'koruna (ISK)',
    'ILS': 'nový šekel (ILS)',
    'JPY': 'jen (JPY)',
    'ZAR': 'rand (ZAR)',
    'CAD': 'dolar (CAD)',
    'KRW': 'won (KRW)',
    'HUF': 'forint (HUF)',
    'MYR': 'ringgit (MYR)',
    'MXN': 'peso (MXN)',
    'XDR': 'ZPČ (XDR)',
    'NOK': 'koruna (NOK)',
    'NZD': 'dolar (NZD)',
    'PLN': 'zlotý (PLN)',
    'RON': 'leu (RON)',
    'SGD': 'dolar (SGD)',
    'SEK': 'koruna (SEK)',
    'CHF': 'frank (CHF)',
    'THB': 'baht (THB)',
    'TRY': 'lira (TRY)',
    'USD': 'dolar (USD)',
    'GBP': 'libra (GBP)'
}

# Used for choices in models
CURRENCIES__MODELS = tuple((key, value) for key, value in CURRENCIES.items())


def get_default_currency() -> tuple[str, str]:
    """
    Returns the default currency specified in the config as a tuple (code, currency_display)
    """
    code = get_bank_config().default_currency
    return code, CURRENCIES[code]


def get_currency_display(code: str) -> str:
    return CURRENCIES[code]
