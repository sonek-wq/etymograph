import os as _os
TOOLS=_os.path.dirname(_os.path.abspath(__file__)); ROOT=_os.path.dirname(TOOLS)
import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        async def lib(route): await route.fulfill(path=_os.path.join(TOOLS,'node_modules/vis-network/standalone/umd/vis-network.min.js'), content_type='application/javascript')
        await pg.route('**/vis-network.min.js', lib); await pg.route('**fonts.g**', lambda r: r.abort())
        await pg.goto('http://localhost:8782/index.html'); await pg.wait_for_selector('#loading.done', timeout=60000)
        r = await pg.evaluate("""() => nodeList.filter(n => n.type === 'word').map(n => n.key + '\t' + formsIn(n, n.partRefs.map(r => byId.get(ID.part(r))).filter(Boolean)).join(' + '))""")
        open(_os.path.join(TOOLS,'js_dec.txt'),'w').write('\n'.join(r))
        print('errors', errs)
        await b.close()
asyncio.run(main())
