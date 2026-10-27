import os as _os
TOOLS=_os.path.dirname(_os.path.abspath(__file__)); ROOT=_os.path.dirname(TOOLS)
import asyncio, sys
from playwright.async_api import async_playwright
S=TOOLS
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1440,'height':900})
        errs=[]; pg.on('pageerror', lambda e: errs.append(str(e)))
        async def lib(route): await route.fulfill(path=S+'/node_modules/vis-network/standalone/umd/vis-network.min.js', content_type='application/javascript')
        await pg.route('**/vis-network.min.js', lib); await pg.route('**fonts.g**', lambda r: r.abort())
        await pg.goto('http://localhost:8782/index.html'); await pg.wait_for_selector('#loading.done', timeout=60000)
        await pg.evaluate("localStorage.clear()")
        for nid in ['word:inspect','word:aspect','pie:*spek-','part:spect','part:in-']:
            await pg.evaluate(f"toggleFav({nid!r})")
        await pg.evaluate("go({mode:'focus', id:'part:spect'})"); await pg.wait_for_timeout(1800)
        await pg.screenshot(path=S+'/m_both.png')
        await pg.click('#labelSeg [data-l="en"]'); await pg.wait_for_timeout(500); await pg.screenshot(path=S+'/m_en.png')
        await pg.click('#labelSeg [data-l="ja"]'); await pg.wait_for_timeout(500); await pg.screenshot(path=S+'/m_ja.png')
        await pg.evaluate("go({mode:'focus', id:'word:aspect'})"); await pg.wait_for_timeout(1500)
        await pg.screenshot(path=S+'/m_ja2.png')
        await pg.reload(); await pg.wait_for_selector('#loading.done', timeout=60000)
        print('persist', await pg.evaluate("labelMode"), await pg.inner_text('#labelSeg .on'))
        await pg.click('#labelSeg [data-l="both"]')
        await pg.evaluate("go({mode:'home'})"); await pg.wait_for_timeout(1500); await pg.screenshot(path=S+'/m_home.png')
        print('errors', errs); await b.close()
asyncio.run(main())
