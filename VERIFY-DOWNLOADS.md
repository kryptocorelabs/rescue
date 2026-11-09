# Check a download before opening it

The published Windows archives provide SHA-256 checksums and detached manifest/signature pairs.

For preview.4, verify the ZIP with GitHub CLI using
`gh attestation verify KryptoCore-Rescue-0.1.0-preview.4-windows-x64.zip --repo kryptocorelabs/apps-source`.
The [release manifest](RELEASE_MANIFEST.json) records the source commit and
build run. Both build records accompany the download. Verify the extracted
EXE with the same command and its executable path.

Follow the [shared download verification guide](https://github.com/kryptocorelabs/kryptocore/blob/main/VERIFY-DOWNLOADS.md) and check the exact file against its release metadata.
Confirm the [published KryptoCoreLabs verification key](https://github.com/kryptocorelabs/kryptocore/blob/main/PUBLIC_RELEASE_KEY.txt) through a trusted route before using Verify.
