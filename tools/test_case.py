"""大文字・小文字だけが違う語（Miss / miss、May / may など）の検索と、id を変えた語（mister → Mister）の旧リンク・登録の引き継ぎを確認する"""
import os as _os
TOOLS=_os.path.dirname(_os.path.abspath(__file__)); ROOT=_os.path.dirname(TOOLS)
import asyncio, json
from playwright.async_api import async_playwright
S = TOOLS
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        async def lib(route): await route.fulfill(path=S + '/node_modules/vis-network/standalone/umd/vis-network.min.js', content_type='application/javascript')
        await pg.route('**/vis-network.min.js', lib); await pg.route('**fonts.g**', lambda r: r.abort())
        await pg.add_init_script("if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.setItem('etymo-favs-v1', JSON.stringify([{id:'word:mister', t:1}, {id:'word:miss', t:2}])); }")
        await pg.goto('http://localhost:8782/index.html#f=word:mister'); await pg.wait_for_selector('#loading.done', timeout=60000)
        await pg.wait_for_timeout(500)
        want = {'Miss': 'word:Miss', 'miss': 'word:miss', 'May': 'word:May', 'may': 'word:may', 'March': 'word:March', 'march': 'word:march', 'Mister': 'word:Mister', 'mister': 'word:Mister'}
        got = await pg.evaluate("ws => Object.fromEntries(ws.map(s => [s, (findNode(s) || {}).id]))", list(want))
        for k, v in want.items():
            if got[k] != v: errs.append(f'search {k}: {got[k]} != {v}')
        print('search', json.dumps(got))
        h = await pg.evaluate("location.hash"); print('hash', h)
        if 'Mister' not in h: errs.append('old link word:mister did not open Mister')
        fav = await pg.evaluate("[...favs.keys()]"); print('favs', fav)
        if 'word:Mister' not in fav: errs.append('favorite word:mister was not carried over')
        print('errors', errs)
        await b.close()
asyncio.run(main())
