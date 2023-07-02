from env_config import TG_API_TOKEN, HOSTNAME


# secure root of our api
API_ROOT = f'{HOSTNAME}/{TG_API_TOKEN}'

TGBOTAPIURL = f'https://api.telegram.org/bot{TG_API_TOKEN}'
TGURL_SETWEBHOOK = f'{TGBOTAPIURL}/setWebhook'
TGURL_ANSWERINLINEQUERY = f'{TGBOTAPIURL}/answerInlineQuery'
