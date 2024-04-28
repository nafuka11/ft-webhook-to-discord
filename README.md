# ft-webhook-to-discord

42のWebhookから得た情報をDiscordのチャンネルに通知する API Gateway + Lambdaです。

## 必要物

- Serverless Framework >= v2.23.0
- AWS CLI

## セットアップ

1. ssm作成

    dev
    ```bash
    aws ssm put-parameter \
        --name "/ft-webhook-to-discord/dev/DISCORD_CHANNEL_ID" \
        --value "<your_channel_id>" \
        --type "SecureString"
    
    aws ssm put-parameter \
        --name "/ft-webhook-to-discord/dev/DISCORD_BOT_TOKEN" \
        --value "<your_bot_token>" \
        --type "SecureString"
    ```

    prod
    ```bash
    aws ssm put-parameter \
        --name "/ft-webhook-to-discord/prod/DISCORD_CHANNEL_ID" \
        --value "<your_channel_id>" \
        --type "SecureString"
    
    aws ssm put-parameter \
        --name "/ft-webhook-to-discord/prod/DISCORD_BOT_TOKEN" \
        --value "<your_bot_token>" \
        --type "SecureString"
    ```

1. 必要なパッケージをインストール

    ```bash
    npm install
    ```

## デプロイ

```bash
sls deploy --stage dev
sls deploy --stage prod
```

## 動作確認

ローカル
```bash
pipenv shell
sls invoke local -f event -p events/data.json
```
dev環境
```bash
sls invoke -f event -s dev -p events/data.json
```
