import json
import pytest
from pytest_mock import MockerFixture
from unittest.mock import MagicMock
from src import handler


@pytest.fixture()
def mock_send_discord(mocker: MockerFixture) -> MagicMock:
    """message.send_event()のMagicMockを返す"""
    send_discord = mocker.patch.object(handler.message, "send_discord")
    return send_discord


def generate_event(body: dict) -> dict:
    """bodyからeventパラメータを返す"""
    return {"body": json.dumps(body)}


def get_valid_body() -> dict:
    """正常ケースのbodyを返す"""
    body = {
        "id": 1,
        "begin_at": "2042-01-02 04:02:42 UTC",
        "end_at": "2042-01-02 06:04:24 UTC",
        "name": "test event",
        "description": "test",
        "location": "online",
        "kind": "event",
        "max_people": None,
        "created_at": "2042-01-01 02:02:42 UTC",
        "updated_at": "2042-01-01 04:04:24 UTC",
        "prohibition_of_cancellation": None,
        "campus_ids": [26],
        "cursus_ids": [21],
    }
    return body


class TestSendEvent:
    def test_valid_body(self, mock_send_discord: MagicMock):
        """正常なbodyが渡された時send_discord()が呼び出されること"""
        body = get_valid_body()

        ret = handler.send_event(generate_event(body), {})
        data = json.loads(ret["body"])

        assert mock_send_discord.call_count == 1

        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
        assert data["message"] == "ok"

    def test_invalid_campus_id(self, mock_send_discord: MagicMock):
        """campus_idsが不正な時send_discord()が呼び出されないこと"""
        body = get_valid_body()
        body["campus_ids"] = [1]

        ret = handler.send_event(generate_event(body), {})
        data = json.loads(ret["body"])

        assert mock_send_discord.call_count == 0

        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
        assert data["message"] == "ok"

    def test_campus_id_is_empty(self, mock_send_discord: MagicMock):
        """campus_idが空のlistの時send_discord()が呼び出されないこと"""
        body = get_valid_body()
        body["campus_ids"] = []

        ret = handler.send_event(generate_event(body), {})
        data = json.loads(ret["body"])

        assert mock_send_discord.call_count == 0

        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
        assert data["message"] == "ok"

    def test_valid_and_invalid_campus_id(self, mock_send_discord: MagicMock):
        """campus_idsに複数の値が含まれる時"""
        body = get_valid_body()
        body["campus_ids"] = [1, 26]

        ret = handler.send_event(generate_event(body), {})
        data = json.loads(ret["body"])

        assert mock_send_discord.call_count == 1

        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
        assert data["message"] == "ok"

    def test_invalid_cursus_id(self, mock_send_discord: MagicMock):
        """cursus_idsが不正な時send_discord()が呼び出されないこと"""
        body = get_valid_body()
        body["cursus_ids"] = [9]

        ret = handler.send_event(generate_event(body), {})
        data = json.loads(ret["body"])

        assert mock_send_discord.call_count == 0

        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
        assert data["message"] == "ok"

    def test_cursus_id_is_empty(self, mock_send_discord: MagicMock):
        """cursus_idが空のlistの時send_discord()が呼び出されないこと"""
        body = get_valid_body()
        body["cursus_ids"] = []

        ret = handler.send_event(generate_event(body), {})
        data = json.loads(ret["body"])

        assert mock_send_discord.call_count == 0

        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
        assert data["message"] == "ok"

    def test_valid_and_invalid_cursus_id(self, mock_send_discord: MagicMock):
        """cursus_idsに複数の値が含まれる時"""
        body = get_valid_body()
        body["cursus_ids"] = [9, 21]

        ret = handler.send_event(generate_event(body), {})
        data = json.loads(ret["body"])

        assert mock_send_discord.call_count == 1

        assert ret["statusCode"] == 200
        assert "message" in ret["body"]
        assert data["message"] == "ok"
