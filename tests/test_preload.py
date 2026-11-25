import importlib

from fastapi.testclient import TestClient

from api import server


def test_serves_the_manifests_listed_in_preload_manifests(monkeypatch):
    monkeypatch.setenv("PRELOAD_MANIFESTS", "examples/civique-droit-vote/manifest.json")
    preloaded = importlib.reload(server)
    assert TestClient(preloaded.app).get("/public/catalog/civique-droit-vote").status_code == 200
