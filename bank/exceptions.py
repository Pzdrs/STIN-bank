class CurrencyExchangeRateNotAvailable(Exception):

    def __init__(self, currency_code: str) -> None:
        super().__init__(f'The exchange rate for "{currency_code}" is not available')
