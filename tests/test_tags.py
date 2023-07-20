import pytest
import requests_mock

from riitag import NotFoundException, RiiTag

riitag = RiiTag()


def test_vehicles_in_radius():
    with requests_mock.Mocker() as m:
        m.get(
            url="https://tag.rc24.xyz/api/user/1234",
            json={
                "user": {"name": "testuser", "id": "1234"},
                "tag_url": {
                    "normal": "https://tag.rc24.xyz/1234/tag.png",
                    "max": "https://tag.rc24.xyz/1234/tag.max.png",
                },
                "game_data": {
                    "last_played": {
                        "game_id": "ABCD",
                        "console": "wii",
                        "region": "EN",
                        "cover_url": "https://tag.rc24.xyz/api/cover/wii/ABCD",
                        "time": 12345678,
                    },
                    "games": ["wii-ABCD"],
                },
            },
        )

        tag = riitag.tags.get("1234")

        assert type(tag) == dict
        assert tag.get("user").get("name") == "testuser"
        assert tag.get("user").get("id") == "1234"


def test_non_existent_zone():
    with requests_mock.Mocker() as m:
        m.get(
            url="https://tag.rc24.xyz/api/user/0000",
            status_code=404,
            json={"error": "User not found"},
        )

        with pytest.raises(NotFoundException):
            assert riitag.tags.get("0000")
