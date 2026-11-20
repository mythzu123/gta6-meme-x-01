import json
import re
from pathlib import Path

from camoufox.sync_api import Camoufox

ROOT = Path(__file__).resolve().parent
CAPTION = "Waited 13 years for GTA 6, so I put my pre-order in my will 📜 My agent and I earn real money from @makefunai's skill-based bounties on make.fun. The queue spot is still mine. makefun-cub-market-glade"
PROFILE = r'C:\Users\Hype GLK\camoufox-test\profil'
POST_PATTERN = re.compile(r'^/zinlee_bnb/status/\d+$')


def find_post(page):
    for article in page.get_by_role('article').all():
        text = article.locator('div[lang]').first
        if text.count() and text.first.inner_text() == CAPTION:
            for link in article.locator('a[href]').all():
                href = link.get_attribute('href') or ''
                if POST_PATTERN.fullmatch(href):
                    return 'https://x.com' + href
    return None


def save_url(url):
    (ROOT / 'post_url.txt').write_text(url + '\n', encoding='utf-8')
    (ROOT / 'POST.json').write_text(json.dumps({'url': url}, separators=(',', ':')), encoding='utf-8')
    print(url, flush=True)


with Camoufox(persistent_context=True, user_data_dir=PROFILE, headless=False) as context:
    page = context.pages[0] if context.pages else context.new_page()
    page.goto('https://x.com/home', timeout=60000)
    try:
        page.get_by_role('link', name='Profile', exact=True).wait_for(timeout=30000)
    except Exception:
        print('URL pemeriksaan:', page.url, flush=True)
        print(page.locator('body').inner_text()[:4000], flush=True)
        page.screenshot(path=str(ROOT / 'x_diagnostic.png'))
        if '/login' in page.url or page.locator('input[autocomplete="username"], input[type="password"]').count():
            raise SystemExit('LOGIN KADALUARSA')
        raise RuntimeError('Status login tidak dapat dipastikan; tidak posting.')

    profile_link = page.get_by_role('link', name='Profile', exact=True)
    if (profile_link.get_attribute('href') or '').lower().rstrip('/') != '/zinlee_bnb':
        raise RuntimeError('Akun aktif bukan @zinlee_bnb; tidak posting.')

    # Check for an existing identical post before composing, including on reruns.
    page.goto('https://x.com/zinlee_bnb', timeout=60000)
    page.get_by_role('article').first.wait_for(timeout=30000)
    existing = find_post(page)
    if existing:
        save_url(existing)
    else:
        page.goto('https://x.com/compose/post', timeout=60000)
        editor = page.get_by_role('dialog').get_by_role('textbox').last
        editor.wait_for(timeout=30000)
        page.locator('input[type="file"]').last.set_input_files(str(ROOT / 'meme.png'))
        page.locator('img[alt="Preview of meme.png"]').wait_for(state='visible', timeout=30000)
        editor.fill(CAPTION)
        if editor.input_value() != CAPTION:
            raise RuntimeError('Caption berbeda; tidak posting.')
        if not page.locator('img[alt="Preview of meme.png"]').is_visible():
            raise RuntimeError('Pratinjau gambar tidak terlihat; tidak posting.')
        button = page.get_by_role('dialog').get_by_role('button', name='Post', exact=True)
        page.wait_for_function("() => [...document.querySelectorAll('[role=dialog] button')].some(b => b.textContent.trim() === 'Post' && !b.disabled)", timeout=30000)
        if not button.is_enabled():
            raise RuntimeError('Tombol Post belum siap; tidak posting.')
        # Exactly one click. No retry, even if confirmation times out.
        try:
            button.click(timeout=15000)
            editor.wait_for(state='hidden', timeout=30000)
        except Exception as error:
            print(f'Hasil klik perlu diperiksa di profil: {error}', flush=True)
        page.goto('https://x.com/zinlee_bnb', timeout=60000)
        page.get_by_role('article').first.wait_for(timeout=30000)
        posted = find_post(page)
        if not posted:
            raise RuntimeError('URL belum terkonfirmasi di profil. Tidak mencoba posting lagi.')
        save_url(posted)
