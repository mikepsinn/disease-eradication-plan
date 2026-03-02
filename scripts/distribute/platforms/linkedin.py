#!/usr/bin/env python3
"""
LinkedIn Platform
=================

Posts to LinkedIn personal profile via the Share API.

Required env vars:
    LINKEDIN_ACCESS_TOKEN   (OAuth2 token)
    LINKEDIN_PERSON_URN     (e.g., "urn:li:person:ABC123")

Setup is painful (OAuth2 dance required):
    1. Create app at https://www.linkedin.com/developers/apps
    2. Request "Share on LinkedIn" (w_member_social) permission
    3. Complete OAuth2 flow to get access token
    4. Get your person URN from https://api.linkedin.com/v2/userinfo

Consider using a helper like https://github.com/tomquirk/linkedin-api
or just posting manually until LinkedIn simplifies their API.
"""

import json
import os
import urllib.request
from typing import Dict


def is_configured() -> bool:
    return all(os.environ.get(k) for k in ["LINKEDIN_ACCESS_TOKEN", "LINKEDIN_PERSON_URN"])


def post(content: Dict) -> bool:
    """Post to LinkedIn. Returns True on success."""
    token = os.environ["LINKEDIN_ACCESS_TOKEN"]
    person_urn = os.environ["LINKEDIN_PERSON_URN"]

    payload = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": content["long_post"],
                },
                "shareMediaCategory": "ARTICLE",
                "media": [{
                    "status": "READY",
                    "originalUrl": content["url"],
                    "title": {"text": content["title"]},
                    "description": {"text": content["description"][:200] if content["description"] else ""},
                }],
            },
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC",
        },
    }

    url = "https://api.linkedin.com/v2/ugcPosts"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0",
        },
        method="POST",
    )

    response = urllib.request.urlopen(req)
    return response.status == 201
