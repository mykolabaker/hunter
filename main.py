import os
import sys
from dotenv import load_dotenv
import requests
import json


def call_hunter_api(endpoint: str, api_parameters: dict) -> dict:
    """
    Calls the Hunter.io API with the given endpoint and parameters.

    Args:
        endpoint (str): The API endpoint to call.
        api_parameters (dict): The parameters to pass to the API.

    Returns:
        dict: The JSON response from the API.
    """
    load_dotenv()
    api_key = os.getenv('HUNTER_API_KEY')
    response = requests.get(
        f'https://api.hunter.io/v2/{endpoint}',
        params={**api_parameters, 'api_key': api_key}
    )
    response.raise_for_status()
    response_data = response.json()
    return response_data.get('data', response_data)


if __name__ == "__main__":
    endpoints = {
        'domain-search': ('domain-search', 'domain'),
        'email-verifier': ('email-verifier', 'email'),
        'company-enrichment': ('companies/find', 'domain')
    }

    if len(sys.argv) != 3 or sys.argv[1] not in endpoints:
        sys.stderr.write(
            "Hunter.io CLI client\n"
            "\n"
            "Usage:\n"
            "  python hunter.py domain-search <domain>\n"
            "  python hunter.py email-verifier <email>\n"
            "  python hunter.py company-enrichment <domain>\n"
        )
        sys.exit(1)

    load_dotenv()
    endpoint, parameter_name = endpoints[sys.argv[1]]
    api_result = call_hunter_api(endpoint, {parameter_name: sys.argv[2]})
    output = json.dumps(api_result, indent=2)
    sys.stdout.write(f'{output}\n')
