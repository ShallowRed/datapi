import json
from pathlib import Path

from adapters.openfisca_adapter import OpenfiscaAdapter

MANIFEST = json.loads(Path("examples/openfisca-pass-culture/manifest.json").read_text())


def test_the_manifest_of_the_pass_culture_is_valid():
    assert OpenfiscaAdapter().validate_manifest(MANIFEST)["ok"]


def test_the_pass_culture_is_computed_for_a_person_born_in_2007():
    out = OpenfiscaAdapter().execute_sync(MANIFEST, "run1", MANIFEST["sample_inputs"], exec_opts={"timeout_seconds": 10})

    assert out["status"] == "success", out
    assert out["output"] == {"pass_culture": 150.0}


def test_an_input_outside_the_schema_fails():
    out = OpenfiscaAdapter().execute_sync(MANIFEST, "run2", {"period": "2025", "date_naissance": "2007-02-01"}, exec_opts={})

    assert out["status"] == "failed"
