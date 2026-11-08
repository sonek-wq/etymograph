"""大文字・小文字だけが違う語（Miss / miss、May / may など）の検索、id を変えた語（mister → Mister）と異表記に統合した語（okay → OK、grey → gray）、番号を付け直した同綴り語（bear → bear(1)、found(2) → found(1) など）の旧リンク・登録の引き継ぎを確認する"""
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
        await pg.add_init_script("if (!sessionStorage.getItem('seeded')) { sessionStorage.setItem('seeded', '1'); localStorage.setItem('etymo-favs-v1', JSON.stringify([{id:'word:mister', t:1}, {id:'word:miss', t:2}, {id:'word:okay', t:3}, {id:'word:grey', t:4}, {id:'word:bear', t:5}, {id:'word:found', t:6}, {id:'word:found(2)', t:7}, {id:'word:scale', t:8}])); }")
        await pg.goto('http://localhost:8782/index.html#f=word:mister'); await pg.wait_for_selector('#loading.done', timeout=60000)
        await pg.wait_for_timeout(500)
        want = {'Miss': 'word:Miss', 'miss': 'word:miss(1)', 'bear': 'word:bear(1)', 'bear2': 'word:bear(2)', 'found': 'word:found(1)', 'scale': 'word:scale(1)', 'scale3': 'word:scale(3)', 'Light': 'word:light(1)', 'May': 'word:May', 'may': 'word:may', 'March': 'word:March', 'march': 'word:march', 'Mister': 'word:Mister', 'mister': 'word:Mister', 'okay': 'word:OK', 'Okay': 'word:OK', 'OK': 'word:OK', 'ok': 'word:OK', 'grey': 'word:gray', 'gray': 'word:gray'}
        got = await pg.evaluate("ws => Object.fromEntries(ws.map(s => [s, (findNode(s) || {}).id]))", list(want))
        for k, v in want.items():
            if got[k] != v: errs.append(f'search {k}: {got[k]} != {v}')
        print('search', json.dumps(got))
        h = await pg.evaluate("location.hash"); print('hash', h)
        if 'Mister' not in h: errs.append('old link word:mister did not open Mister')
        fav = await pg.evaluate("[...favs.keys()]"); print('favs', fav)
        if 'word:Mister' not in fav: errs.append('favorite word:mister was not carried over')
        for o, n in (('word:okay', 'word:OK'), ('word:grey', 'word:gray'), ('word:bear', 'word:bear(1)'), ('word:scale', 'word:scale(3)')):
            if n not in fav or o in fav: errs.append(f'favorite {o} was not carried over to {n}')
        if 'word:found(2)' not in fav or 'word:found(1)' not in fav: errs.append('favorites found / found(2) were not renumbered to found(2) / found(1)')
        if await pg.evaluate("localStorage.getItem('etymo-fav-mig')") != '1': errs.append('migration marker not set')
        await pg.reload(); await pg.wait_for_selector('#loading.done', timeout=60000); await pg.wait_for_timeout(300)
        fav2 = await pg.evaluate("[...favs.keys()]")
        if sorted(fav2) != sorted(fav): errs.append(f'favorites changed on reload: {fav2}')
        opt = await pg.evaluate("[...document.querySelectorAll('#suggest option')].filter(o => ['okay','grey'].includes(o.value)).map(o => o.value + ':' + o.textContent)")
        print('datalist', opt)
        if len(opt) != 2: errs.append('variant options missing in datalist')
        dup = await pg.evaluate("nodeList.filter(n => n.type === 'word' && ['okay','grey'].includes(n.key)).length")
        if dup: errs.append('okay / grey still exist as separate words')
        await pg.goto('http://localhost:8782/index.html#f=word:okay'); await pg.reload(); await pg.wait_for_selector('#loading.done', timeout=60000); await pg.wait_for_timeout(500)
        h2 = await pg.evaluate("location.hash"); print('hash2', h2)
        if 'OK' not in h2: errs.append('old link word:okay did not open OK')
        var = await pg.evaluate("(document.querySelector('.info-var') || {}).textContent || ''"); print('info', var)
        if 'okay' not in var: errs.append('info panel does not show the variant okay')
        await pg.fill('#q', 'okay'); await pg.press('#q', 'Enter'); await pg.wait_for_timeout(400)
        h3 = await pg.evaluate("location.hash"); print('hash3', h3)
        if 'OK' not in h3: errs.append('searching okay did not open OK')
        await pg.goto('http://localhost:8782/index.html#f=word:bear'); await pg.reload(); await pg.wait_for_selector('#loading.done', timeout=60000); await pg.wait_for_timeout(500)
        h4 = await pg.evaluate("location.hash"); print('hash4', h4)
        if 'bear(1)' not in h4 and 'bear%281%29' not in h4: errs.append('old link word:bear did not open bear(1)')
        unnum = await pg.evaluate("(() => { const ks = new Set(nodeList.filter(n => n.type === 'word').map(n => n.key)); return [...ks].filter(k => /\\(\\d+\\)$/.test(k) && ks.has(k.replace(/\\(\\d+\\)$/, ''))); })()")
        if unnum: errs.append(f'homographs without (1): {unnum}')
        print('errors', errs)
        await b.close()
asyncio.run(main())
