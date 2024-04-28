import discord
import os
from datetime import datetime, timezone, timedelta
import traceback


CAMPUS_ID = 26
CURSUS_ID = 21


def can_send_discord(body: dict) -> bool:
    """Event情報からDiscordに送信できるかどうかを返す

    Args:
        body (dict): event情報

    Returns:
        bool: Discordに送信できるかどうか

    """
    if CAMPUS_ID not in body["campus_ids"]:
        return False
    if CURSUS_ID not in body["cursus_ids"]:
        return False
    return True


def send_discord(body: dict) -> None:
    """Discordにevent情報を送信する

    Args:
        body (dict): event情報

    """
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        try:
            embed = create_event_embed(body)
            channel = client.get_channel(int(os.getenv("DISCORD_CHANNEL_ID")))
            await channel.send(embed=embed)
        except Exception as e:
            traceback.print_exc()
        await client.close()

    client.run(os.getenv("DISCORD_BOT_TOKEN"))


def create_event_embed(event: dict) -> discord.Embed:
    """event情報のEmbedを返す

    Args:
        event (dict): event情報

    Returns:
        discord.Embed: Embed

    """
    title = f"{event['name']} が作成されました"
    begin_at = _get_local_timestr(event["begin_at"])
    end_at = _get_local_timestr(event["end_at"])

    max_people = event["max_people"] or "∞"

    location = event["location"] or "指定なし"
    kind = event["kind"] or "なし"

    link = f"https://profile.intra.42.fr/events/{event['id']}"
    register_message = f"[Register]({link})"

    embed = discord.Embed(title=title, description=event["description"])
    embed.add_field(name="開始", value=begin_at, inline=True)
    embed.add_field(name="終了", value=end_at, inline=True)
    embed.add_field(name="定員", value=max_people, inline=True)
    embed.add_field(name="場所", value=location)
    embed.add_field(name="種類", value=kind)
    embed.add_field(name="Link", value=register_message)
    return embed


def _get_local_timestr(timestr: str) -> str:
    """IS0 8601形式の日付文字列からメッセージ表示用の文字列を返す

    Args:
        timestr (str): IS0 8601形式の日付文字列

    Returns:
        str: メッセージ表示用の文字列(MM/DD HH:mm)

    """

    jst = timezone(timedelta(hours=9), "JST")
    date = _from_iso8601_str(timestr).astimezone(jst)
    result = date.strftime("%m/%d %H:%M")
    return result


def _from_iso8601_str(time_str: str) -> datetime:
    """ISO 8601形式の日付文字列からdatetimeを返す
    Webhookでは YYYY-MM-DD hh:mm:ss UTC 形式

    Args:
        time_str (str): ISO 8601形式の日付文字列

    Returns:
        datetime: datetime

    """
    time_str = time_str.replace("Z", "+00:00")
    time_str = time_str.replace("UTC", "+00:00")
    d = datetime.fromisoformat(time_str)
    return d
