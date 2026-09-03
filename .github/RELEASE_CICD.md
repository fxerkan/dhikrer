# Release CI/CD

`.github/workflows/release.yml` builds **and deploys both platforms**.

- **Push a semver tag** → builds + **publishes** iOS (App Store Connect) and Android (Play).
  ```bash
  git tag -a v1.4.0 -m "Dhikrer 1.4.0" && git push origin v1.4.0
  ```
- **Actions tab → Run workflow** (manual) → **dry run by default**: builds + signs + uploads
  the `.aab`/`.ipa` as workflow artifacts but does **not** touch the stores. Tick the
  **publish** box to actually upload.

## Where the secrets live

Master copies are in **concealer**, scope `*/zikirci/prod/zikirci`
(`mcp__concealer__list_secrets --project zikirci`). GitHub Actions can't call concealer, so
the same values must also exist as **GitHub repo secrets** (Settings → Secrets and variables
→ Actions). Ask Claude to push them from concealer, or set them by hand from the table below.

| GitHub secret | Source (concealer secret → field) | Status |
|---|---|---|
| `ANDROID_KEYSTORE_BASE64` | `ANDROID_UPLOAD_KEYSTORE` → `keystore_base64` | ✅ in concealer |
| `ANDROID_STORE_PASSWORD` | `ANDROID_UPLOAD_KEYSTORE` → `store_password` | ✅ |
| `ANDROID_KEY_ALIAS` | `ANDROID_UPLOAD_KEYSTORE` → `key_alias` | ✅ |
| `ANDROID_KEY_PASSWORD` | `ANDROID_UPLOAD_KEYSTORE` → `key_password` | ✅ |
| `PLAY_SERVICE_ACCOUNT_JSON` | *(to be created — see below)* | ❌ **missing** |
| `IOS_DIST_CERT_P12_BASE64` | derived from `APPLE_DIST_CERT` (`cert_pem`+`private_key_pem` → p12) | ⚙️ regenerate |
| `IOS_DIST_CERT_PASSWORD` | password you set when building the p12 | ⚙️ |
| `IOS_PROVISION_PROFILE_BASE64` | `_credentials/apple/make_profile.py` output, base64 | ⚙️ regenerate |
| `IOS_PROFILE_NAME` | `APPLE_DIST_CERT` → `profile_name` (`Dhikrer App Store (local)`) | ✅ |
| `IOS_TEAM_ID` | `APPLE_DIST_CERT` → `team_id` (`96RZX28T7X`) | ✅ |
| `ASC_KEY_ID` | `APPLE_ASC_API_KEY` → `key_id` (`T2SMCH6U9X`) | ✅ |
| `ASC_ISSUER_ID` | `APPLE_ASC_API_KEY` → `issuer_id` | ✅ |
| `ASC_API_KEY_BASE64` | base64 of `APPLE_ASC_API_KEY` → `p8_private_key` | ✅ |

Android uses **Play App Signing**: this keystore is the *upload* key; Google re-signs with the
managed app-signing key. Default track is `internal` (edit `track:` in the workflow).

## Creating the Play service account JSON (one-time)

See the step-by-step in the release chat / `docs`. Summary: GCP Console → create service
account → create JSON key → Play Console → Users & permissions → invite that account with
*Release apps to testing tracks* (and production) → paste JSON into `PLAY_SERVICE_ACCOUNT_JSON`.

## iOS signing note

Manual signing with our **own** distribution cert + profile (not Xcode cloud signing — it
breaks the signature; see `docs/ios.md`). Upload lands in TestFlight; promoting to the App
Store is a click in App Store Connect (or set auto-release on the version).
