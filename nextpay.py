import json
from typing import Literal, Union

from aiohttp import ClientSession, FormData

BASE_URL = "https://example.com"  # address to your domain


class NextPay:
    # setting headers
    headers = {
        'User-Agent': 'PostmanRuntime/7.26.8',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # get token and money amount from user
    def __init__(self, token: str, amount: Union[str, int]):
        self.token, self.amount = token, amount

    # creating the purchase page
    async def purchase(
            self, order_id: str, currency: Literal['IRT', 'IRR'] = None, phone: str = None,
            custom_json_fields: dict = None, payer_name: str = None, payer_desc: str = None,
            auto_verify: Literal[True] = None, allowed_card: str = None):

        url = "https://nextpay.org/nx/gateway/token"

        # creating data for url
        data = FormData()
        data.add_field('api_key', self.token)
        data.add_field('amount', self.amount)
        data.add_field('order_id', order_id)
        data.add_field('callback_uri', f'{BASE_URL}/UploaderCreator/verify')
        # giving external data if user provided it
        if currency in ['IRT', 'IRR']:
            data.add_field('currency', currency)
        if phone:
            data.add_field('phone', phone)
        if custom_json_fields:
            data.add_field('custom_json_fields', json.dumps(custom_json_fields))
        if payer_name:
            data.add_field('payer_name', payer_name)
        if payer_desc:
            data.add_field('payer_desc', payer_desc)
        if auto_verify is True:
            data.add_field('auto_verify', 'yes')
        if allowed_card:
            data.add_field('allowed_card', allowed_card)

        async with ClientSession(headers=self.headers) as aiohttp:
            async with aiohttp.post(url=url, data=data) as respond:
                result = await respond.json()
                # if page created successfully
                if result['code'] == -1:
                    # purchase_page = f"https://nextpay.org/nx/gateway/payment/{result['trans_id']}"
                    return result['trans_id']
                # if an
                else:
                    return False

    # verifying the purchase
    async def verify(self, trans_id: str, currency: Literal['IRT', 'IRR'] = None):
        url = "https://nextpay.org/nx/gateway/verify"

        # creating data for url
        data = FormData()
        data.add_field('api_key', self.token)
        data.add_field('amount', self.amount)
        data.add_field('trans_id', trans_id)
        # giving external data if user provided it
        if currency in ['IRT', 'IRR']:
            data.add_field("currency", currency)

        async with ClientSession(headers=self.headers) as aiohttp:
            async with aiohttp.post(url=url, data=data) as respond:
                result = await respond.json()
                return result

    async def refund(self, trans_id):
        url = "https://nextpay.org/nx/gateway/verify"

        # creating data for url
        data = FormData()
        data.add_field('api_key', self.token)
        data.add_field('amount', self.amount)
        data.add_field('trans_id', trans_id)
        data.add_field('refund_request', 'yes_money_back')

        async with ClientSession(headers=self.headers) as aiohttp:
            async with aiohttp.post(url=url, data=data) as respond:
                result = await respond.json()
                return result
