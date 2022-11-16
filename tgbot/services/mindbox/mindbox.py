import aiohttp

from .schemas import CustomerData, SubscribeData, APIError


class MindBox:
    def __init__(self, secret_key: str):
        self.headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Accept': 'application/json',
            'Authorization': f'Mindbox secretKey="{secret_key}"'
        }

    async def register_customer_with_telegram_bot(self, customer_data: CustomerData) -> bool:
        """
        Customer registration via Chatbot

        :param customer_data:
        :return: True — if the request successful, False — otherwise.
        """
        api_url = 'https://api.mindbox.ru/v3/operations/async?endpointId=naos.ru&operation=ChatBot.Registration'
        customer_data.subscriptions[:0] = SubscribeData(brand='naos', pointOfContact='Email')

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=self.headers, json=customer_data.dict()) as response:
                try:
                    response_json = await response.json()
                except BaseException as e:
                    raise APIError(e)

                if response_json['status'] == 'Success':
                    return True

                if response_json.get('errorMessage'):
                    raise APIError(response_json['status'] + ' - ' + response_json['errorMessage'])

                return False
