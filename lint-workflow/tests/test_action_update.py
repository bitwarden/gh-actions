import urllib3 as urllib

from lint import get_action_update, memoized_action_update_urls

http = urllib.PoolManager()


def test_action_update():
    action_id = "actions/checkout@86f86b36ef15e6570752e7175f451a512eac206b"
    sub_string = "github.com"
    update_url = get_action_update(action_id)
    assert str(sub_string) in str(update_url)

    r = http.request("GET", update_url)

    assert r.status == 200

    assert "actions/checkout" in memoized_action_update_urls
