import json
import traceback
from src import message


def send_event(event: dict, context: dict) -> dict:
    """API Gatewayリクエストのevent情報をDiscordに送信する

    Args:
        event(dict): eventパラメータ(https://docs.aws.amazon.com/ja_jp/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format)
        context(dict): contextオブジェクト(https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-context.html)

    Returns:
        dict: レスポンス(https://docs.aws.amazon.com/ja_jp/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format)

    """
    body = {"message": "ok"}
    response = {"statusCode": 200, "body": json.dumps(body)}
    print(event)
    try:
        message.send_discord(json.loads(event["body"]))
    except Exception as e:
        traceback.print_exc()
    return response
