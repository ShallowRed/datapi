import httpx


class APIPartClientError(Exception):
    """API Particulier HTTP call failed."""


async def fetch_quotient_familial(config: dict, fc_access_token: str) -> dict:
    """Fetch the user's quotient familial (CAF/MSA) via API Particulier.

    France Connect modality: the FC access token identifies the user, no
    identity parameters are needed. The FC token must carry the endpoint's
    métier scopes (cnaf_quotient_familial, cnaf_allocataires, cnaf_enfants,
    cnaf_adresse) and is very short-lived (~60 s), so this must be called
    right after the FC token exchange.
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{config['base_url']}/v3/dss/quotient_familial/france_connect",
            params={"recipient": config["recipient"]},
            headers={"Authorization": f"Bearer {fc_access_token}"},
        )
    if resp.status_code != 200:
        raise APIPartClientError(
            f"quotient familial fetch failed: {resp.status_code} {resp.text}"
        )
    return resp.json()
