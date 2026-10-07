import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


def test_page_renders_all_three_agents():
    r = TestClient(app).get("/")
    assert r.status_code == 200
    for name in ("Reach agent", "Click agent", "Subscriber agent"):
        assert name in r.text


def test_health():
    assert TestClient(app).get("/health").json() == {"ok": True}
