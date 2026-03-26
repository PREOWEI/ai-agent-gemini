from tools.base import BaseTool
import requests


class CurrencyTool(BaseTool):

    def __init__(self) -> None:
        super().__init__("currency", "Convert money between currencies")

    # main logic
    def execute(self, args: dict) -> str:
        try:
            amount = float(args.get("amount", 0))
            from_currency = args.get("from_currency", "").upper()
            to_currency = args.get("to_currency", "")
            to_currencies = args.get("to_currencies", [])

            if to_currency:
                targets = [to_currency.upper()]
            else:
                targets = [currency.upper() for currency in to_currencies]

            # get exchange rates
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            response = requests.get(url).json()

            if "rates" not in response:
                return "invalid currency"

            results = []

            for currency in targets:
                if currency not in response["rates"]:
                    continue

                rate = response["rates"][currency]
                result = amount * rate
                results.append(f"{amount} {from_currency} = {round(result, 2)} {currency}")

            if not results:
                return "invalid currency"

            return "\n".join(results)

        except Exception as e:
            return f"error: {e}"

    # schema for Gemini
    def get_declaration(self) -> dict:
        return {
            "name": "currency",
            "description": "Convert money between currencies",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "amount to convert"
                    },
                    "from_currency": {
                        "type": "string",
                        "description": "currency to convert from (e.g. USD)"
                    },
                    "to_currency": {
                        "type": "string",
                        "description": "currency to convert to (e.g. EUR)"
                    },
                    "to_currencies": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "list of currencies to convert to, for example ['NGN', 'CAD', 'GBP']"
                    }
                },
                "required": ["amount", "from_currency"]
            }
        }
