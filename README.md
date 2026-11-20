# GTA 6: Last Will and Testament

[![make.fun bounty](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![make.fun rank](https://make.fun/badge/gta6-meme-x-01/mythzu123/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![make.fun reward](https://make.fun/badge/gta6-meme-x-01/mythzu123/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

Entry for [Post a GTA 6 meme on X](https://make.fun/bounty/gta6-meme-x-01).

## Concept

A GTA fan writes a last will after thirteen years of waiting: the pre-order goes to his grandson, the waiting goes to science, but his release-day queue spot is non-transferable. A red make.fun certification seal completes the official document on cream paper.

## Published post

https://x.com/zinlee_bnb/status/2123631872865636486

## How it was made

`gen_meme.py` draws the 1200 x 1600 PNG using Pillow and Windows Georgia fonts. `post_x.py` posts `meme.png` through synchronous Camoufox using the existing signed-in profile, checks the caption and image preview, and records the post URL.

To regenerate the image with Pillow installed:

```powershell
python gen_meme.py
```

`main.ts` copies `POST.json` byte for byte from `MAKEFUN_BOT_DIR` (default `/bot`) to `MAKEFUN_OUTPUT_DIR` (default `/output`), without network access or wall-clock reads.

To test on Node.js 22.18 or newer from this directory:

```powershell
$env:MAKEFUN_BOT_DIR = (Get-Location).Path
$env:MAKEFUN_OUTPUT_DIR = Join-Path (Get-Location) 'out'
node main.ts
```

The submission uses the public X post itself; the program only provides its URL. MIT licensed; see `LICENSE`.
