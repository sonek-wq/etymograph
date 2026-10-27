import os as _os
TOOLS=_os.path.dirname(_os.path.abspath(__file__)); ROOT=_os.path.dirname(TOOLS)
import asyncio, sys
from playwright.async_api import async_playwright
S=TOOLS
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width':1440,'height':900})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        async def lib(route): await route.fulfill(path=S+'/node_modules/vis-network/standalone/umd/vis-network.min.js', content_type='application/javascript')
        await pg.route('**/vis-network.min.js', lib); await pg.route('**fonts.g**', lambda r: r.abort())
        await pg.goto('http://localhost:8782/index.html'); await pg.wait_for_selector('#loading.done', timeout=60000)
        print('stats:', (await pg.inner_text('#stats')).replace('\n',' / '), '| warn:', repr(await pg.inner_text('#warn')), await pg.get_attribute('#warn','title'))
        await pg.wait_for_timeout(1500); await pg.screenshot(path=S+'/b6home.png')
        for a,c in [('robot','car'),('karma','car'),('sugar','candy'),('mantra','mind'),('loot','rob')]:
            r = await pg.evaluate(f"shortestPaths('word:{a}','word:{c}',true).slice(0,1).map(p=>p.join(' > '))")
            print(a,'->',c,':',r)
        await pg.evaluate("go({mode:'focus', id:'word:robot'})"); await pg.wait_for_timeout(400)
        print('trig =', (await pg.inner_text('.decomp')).split('\n')[0])
        await pg.evaluate("go({mode:'category', id:'animal'})"); await pg.wait_for_timeout(2500); await pg.screenshot(path=S+'/b6animal.png')
        print('errors:', errs); await b.close()
asyncio.run(main())
