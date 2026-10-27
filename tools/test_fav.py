import os as _os
TOOLS=_os.path.dirname(_os.path.abspath(__file__)); ROOT=_os.path.dirname(TOOLS)
import asyncio, sys
from playwright.async_api import async_playwright
S = TOOLS
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
        async def lib(route): await route.fulfill(path=S + '/node_modules/vis-network/standalone/umd/vis-network.min.js', content_type='application/javascript')
        await pg.route('**/vis-network.min.js', lib); await pg.route('**fonts.g**', lambda r: r.abort())
        await pg.goto('http://localhost:8782/index.html'); await pg.wait_for_selector('#loading.done', timeout=60000)
        await pg.evaluate("localStorage.clear()")
        # 1. star on word / pie / affix / root
        for nid in ['word:inspect', 'pie:*spek-', 'part:-ion', 'part:spect', 'word:gate']:
            await pg.evaluate(f"go({{mode:'focus', id:{nid!r}}})"); await pg.wait_for_timeout(300)
            has = await pg.evaluate("!!document.querySelector('#info .fav')")
            await pg.click('#info .fav'); await pg.wait_for_timeout(50)
            print(nid, 'star', has, 'on', await pg.evaluate("document.querySelector('#info .fav').classList.contains('on')"))
        # speak button order
        await pg.evaluate("go({mode:'focus', id:'word:inspect'})"); await pg.wait_for_timeout(300)
        print('order', await pg.evaluate("[...document.querySelector('#info .info-name').children].map(e=>e.className)"))
        await pg.screenshot(path=S + '/fav_info.png')
        print('count', await pg.inner_text('#favCount'), 'stored', await pg.evaluate("localStorage.getItem('etymo-favs-v1')"))
        await pg.click('#favOpen'); await pg.wait_for_timeout(200)
        print('tabs', await pg.inner_text('#fvTabs'))
        print('list', (await pg.inner_text('#fvList')).replace('\n', ' | '))
        await pg.screenshot(path=S + '/fav_panel.png')
        for srt in ['old', 'az', 'za', 'links']:
            await pg.click(f'#fvSort [data-sort="{srt}"]')
            print(srt, (await pg.inner_text('#fvList')).replace('\n', ' | ')[:200])
        await pg.click('#fvTabs [data-fv="word"]'); print('word tab', (await pg.inner_text('#fvList')).replace('\n', ' | '))
        await pg.click('#fvList [data-unfav="word:gate"]'); print('after unfav', await pg.inner_text('#fvUndo'), await pg.inner_text('#favCount'))
        await pg.click('#fvUndo [data-undo]'); print('after undo', await pg.inner_text('#favCount'), (await pg.inner_text('#fvList')).replace('\n', ' | '))
        await pg.fill('#fvFilter', '見る'); await pg.click('#fvTabs [data-fv="all"]'); print('filter', (await pg.inner_text('#fvList')).replace('\n', ' | '))
        await pg.click('#fvToIx'); print('exclusive', await pg.evaluate("[document.getElementById('favPanel').hidden, document.getElementById('indexPanel').hidden]"))
        await pg.click('#ixToFav'); print('back', await pg.evaluate("[document.getElementById('favPanel').hidden, document.getElementById('indexPanel').hidden]")); await pg.click('#fvClose')
        # reload persistence
        await pg.reload(); await pg.wait_for_selector('#loading.done', timeout=60000)
        print('persist', await pg.inner_text('#favCount'))
        # 3. routes
        res = await pg.evaluate("""() => {
          const words = nodeList.filter(n => n.type === 'word'); let need = null, none = null;
          for (let i = 0; i < 4000 && (!need || !none); i++) {
            const a = words[(i * 7919) % words.length], b = words[(i * 104729 + 13) % words.length]; if (a === b) continue;
            const s = shortestPaths(a.id, b.id, false, 1), l = shortestPaths(a.id, b.id, true, 1);
            if (!s.length && l.length && !need) need = [a.id, b.id, l[0]];
            if (!l.length && !none) none = [a.id, b.id];
          }
          return { need, none };
        }""")
        print('pairs', res)
        await pg.evaluate("switchTab('path')")
        await pg.uncheck('#viaAffix')
        a, bb, _ = res['need']
        await pg.evaluate(f"go({{mode:'route', from:{a!r}, to:{bb!r}}})"); await pg.wait_for_timeout(400)
        print('fallback hint:', await pg.inner_text('#pathHint'), '| note:', await pg.evaluate("document.querySelector('.route-note')?.textContent"))
        await pg.screenshot(path=S + '/route_fb.png')
        await pg.evaluate("go({mode:'route', from:'word:inspect', to:'word:structure'})"); await pg.wait_for_timeout(400)
        print('strict hint:', await pg.inner_text('#pathHint'), await pg.evaluate("route.all[0].map(id=>byId.get(id).type).join(',')"))
        await pg.check('#viaAffix'); await pg.wait_for_timeout(300)
        print('on hint:', await pg.inner_text('#pathHint'))
        if res['none']:
            a, bb = res['none']
            await pg.evaluate(f"go({{mode:'route', from:{a!r}, to:{bb!r}}})"); await pg.wait_for_timeout(300)
            print('none hint:', await pg.inner_text('#pathHint'), 'mode', await pg.evaluate("current && current.mode"))
        await pg.uncheck('#viaAffix')
        await pg.click('#randomBtn'); await pg.wait_for_timeout(400); print('random:', await pg.inner_text('#pathHint'))
        await pg.reload(); await pg.wait_for_selector('#loading.done', timeout=60000)
        print('viaAffix persisted off:', not await pg.is_checked('#viaAffix'))
        # mobile
        await pg.evaluate("go({mode:'home'})"); await pg.set_viewport_size({'width': 390, 'height': 800}); await pg.wait_for_timeout(600)
        await pg.click('#favOpen'); await pg.wait_for_timeout(200); await pg.screenshot(path=S + '/fav_mobile.png')
        print('errors', errs)
        await b.close()
asyncio.run(main())
