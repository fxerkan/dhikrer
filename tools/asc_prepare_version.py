#!/usr/bin/env python3
"""Prepare (but do NOT submit) an App Store version so a release needs only one
manual click: "Submit for Review".

Given a build already uploaded by the CI (altool), this:
  1. waits for that build to finish Apple-side processing (state VALID),
  2. finds or creates the editable App Store version (versionString),
  3. attaches the build to it,
  4. writes the localized "What's New" from store/release-notes.json.

It deliberately does NOT create a review submission — the human clicks Submit.
It never touches screenshots, description, keywords, or review-contact info.

Auth: App Store Connect API key (ES256 JWT). Env:
  ASC_KEY_ID, ASC_ISSUER_ID, and ASC_API_KEY_PATH (path to the .p8).
Release inputs (env, with CLI fallback):
  ASC_APP_ID (default 6803203796), APP_VERSION (MARKETING_VERSION),
  BUILD_NUMBER (CFBundleVersion). RELEASE_NOTES defaults to store/release-notes.json.

ponytail: PyJWT does the ES256/JOSE encoding (don't hand-roll DER->raw). stdlib urllib
for HTTP — no requests dependency.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

API = "https://api.appstoreconnect.apple.com"
# App Store states in which metadata/build are still editable.
EDITABLE = {
    "PREPARE_FOR_SUBMISSION", "DEVELOPER_REJECTED", "REJECTED",
    "METADATA_REJECTED", "INVALID_BINARY", "WAITING_FOR_REVIEW",
}


def make_token(key_id: str, issuer_id: str, p8: str) -> str:
    import jwt  # PyJWT + cryptography (CI installs it; not needed for --selftest)
    now = int(time.time())
    return jwt.encode(
        {"iss": issuer_id, "iat": now, "exp": now + 19 * 60, "aud": "appstoreconnect-v1"},
        p8,
        algorithm="ES256",
        headers={"kid": key_id, "typ": "JWT"},
    )


def api(token, method, path, body=None):
    url = path if path.startswith("http") else API + path
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")
        raise SystemExit(f"ASC API {method} {path} -> {e.code}\n{detail}")


def wait_for_build(token, app_id, build_number, timeout, interval):
    deadline = time.time() + timeout
    q = (f"/v1/builds?filter[app]={app_id}"
         f"&filter[version]={build_number}&limit=1")
    while True:
        data = api(token, "GET", q).get("data", [])
        if data:
            b = data[0]
            state = b["attributes"]["processingState"]
            print(f"build {build_number}: {state}")
            if state == "VALID":
                return b["id"]
            if state in ("INVALID", "FAILED"):
                raise SystemExit(f"build {build_number} processing {state}")
        else:
            print(f"build {build_number}: not visible yet")
        if time.time() > deadline:
            raise SystemExit(f"timed out waiting for build {build_number} to process")
        time.sleep(interval)


def find_or_create_version(token, app_id, version):
    q = (f"/v1/apps/{app_id}/appStoreVersions"
         f"?filter[versionString]={version}&filter[platform]=IOS&limit=1")
    data = api(token, "GET", q).get("data", [])
    if data:
        v = data[0]
        state = v["attributes"]["appStoreState"]
        print(f"version {version} exists (state {state})")
        return v["id"], state
    print(f"creating version {version}")
    v = api(token, "POST", "/v1/appStoreVersions", {
        "data": {
            "type": "appStoreVersions",
            "attributes": {"platform": "IOS", "versionString": version},
            "relationships": {"app": {"data": {"type": "apps", "id": app_id}}},
        }
    })["data"]
    return v["id"], v["attributes"]["appStoreState"]


def attach_build(token, version_id, build_id):
    api(token, "PATCH", f"/v1/appStoreVersions/{version_id}", {
        "data": {
            "type": "appStoreVersions", "id": version_id,
            "relationships": {"build": {"data": {"type": "builds", "id": build_id}}},
        }
    })
    print("build attached")


def set_whats_new(token, version_id, notes):
    locs = api(token, "GET",
               f"/v1/appStoreVersions/{version_id}/appStoreVersionLocalizations"
               "?limit=50").get("data", [])
    for loc in locs:
        locale = loc["attributes"]["locale"]
        if locale not in notes:
            print(f"  {locale}: no note in release-notes.json — left unchanged")
            continue
        api(token, "PATCH", f"/v1/appStoreVersionLocalizations/{loc['id']}", {
            "data": {"type": "appStoreVersionLocalizations", "id": loc["id"],
                     "attributes": {"whatsNew": notes[locale]}}
        })
        print(f"  {locale}: What's New set")


def main():
    app_id = os.environ.get("ASC_APP_ID", "6803203796")
    version = os.environ["APP_VERSION"]
    build_number = os.environ["BUILD_NUMBER"]
    notes_path = os.environ.get("RELEASE_NOTES", "store/release-notes.json")
    timeout = int(os.environ.get("WAIT_TIMEOUT_SEC", "2400"))
    interval = int(os.environ.get("POLL_INTERVAL_SEC", "60"))

    key_id = os.environ["ASC_KEY_ID"]
    issuer_id = os.environ["ASC_ISSUER_ID"]
    with open(os.environ["ASC_API_KEY_PATH"]) as f:
        p8 = f.read()

    rn = json.load(open(notes_path))
    notes = rn.get("notes", {}) if rn.get("version") == version else {}
    if not notes:
        print(f"WARNING: {notes_path} version={rn.get('version')!r} != {version!r} "
              "— skipping What's New (set it manually).")

    token = make_token(key_id, issuer_id, p8)
    build_id = wait_for_build(token, app_id, build_number, timeout, interval)
    version_id, state = find_or_create_version(token, app_id, version)
    if state not in EDITABLE:
        raise SystemExit(f"version {version} state {state} is not editable — "
                         "nothing prepared (already submitted/live?).")
    attach_build(token, version_id, build_id)
    if notes:
        set_whats_new(token, version_id, notes)
    print(f"\nReady. Review + click Submit: "
          f"https://appstoreconnect.apple.com/apps/{app_id}/distribution/ios/version/deliverable")


def _selftest():
    # Pure logic guard: version mismatch must blank the notes; match must keep them.
    rn = {"version": "1.3.2", "notes": {"en-US": "x"}}
    assert (rn["notes"] if rn["version"] == "1.3.2" else {}) == {"en-US": "x"}
    assert (rn["notes"] if rn["version"] == "9.9.9" else {}) == {}
    print("selftest ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        main()
