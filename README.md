# GTA 6: Official Excuse Note

[![make.fun bounty](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![make.fun rank](https://make.fun/badge/gta6-meme-x-01/mythzu123/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![make.fun reward](https://make.fun/badge/gta6-meme-x-01/mythzu123/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

Entry for [Post a GTA 6 meme on X](https://make.fun/bounty/gta6-meme-x-01).

## Concept

Leonida Medical Center official medical excuse note for GTA 6 launch week. After 13 years and 4,811 days of waiting since September 2013, the patient is excused from work from Nov 19 to Nov 24 for acute GTA 6 fever, with the prescription: Vice City, Day One, No Exceptions. Features the make.fun ghost mascot with magenta star coin and stamp: PAID (IN FULL) BY MY AI AGENT ON MAKE.FUN.

## Published post

https://x.com/zinlee_bnb/status/2124706795688271909

## Program entrypoint

`main.ts` copies `POST.json` byte for byte from `MAKEFUN_BOT_DIR` (default `/bot`) to `MAKEFUN_OUTPUT_DIR` (default `/output`), verifying byte count and valid JSON structure without network access or wall-clock reads.

To test on Node.js 22.18 or newer from this directory:

```powershell
$env:MAKEFUN_BOT_DIR = (Get-Location).Path
$env:MAKEFUN_OUTPUT_DIR = Join-Path (Get-Location) 'out'
node main.ts
```

The submission uses the public X post itself; the program provides its URL. MIT licensed; see `LICENSE`.
