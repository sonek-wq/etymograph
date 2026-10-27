"""スマホ幅のスクリーンショット（tools/mob_*.png）と簡単な操作テスト。PC 幅も1枚撮る"""
import asyncio, os
from playwright.async_api import async_playwright
TOOLS = os.path.dirname(os.path.abspath(__file__))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); errs = []
        async def page(w, h, mobile):
            ctx = await b.new_context(viewport={'width': w, 'height': h}, is_mobile=mobile, has_touch=mobile, device_scale_factor=2 if mobile else 1)
            pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
            async def lib(route): await route.fulfill(path=os.path.join(TOOLS, 'node_modules/vis-network/standalone/umd/vis-network.min.js'), content_type='application/javascript')
            await pg.route('**/vis-network.min.js', lib); await pg.route('**fonts.g**', lambda r: r.abort())
            await pg.goto('http://localhost:8782/index.html'); await pg.wait_for_selector('#loading.done', timeout=60000)
            await pg.evaluate("localStorage.clear()")
            return pg
        shot = lambda pg, n: pg.screenshot(path=os.path.join(TOOLS, f'mob_{n}.png'))
        pg = await page(390, 844, True)
        await pg.wait_for_timeout(1200); await shot(pg, '1home')
        await pg.evaluate("go({mode:'focus', id:'word:inspect'})"); await pg.wait_for_timeout(1500); await shot(pg, '2word')
        await pg.evaluate("go({mode:'focus', id:'pie:*spek-'})"); await pg.wait_for_timeout(1500); await shot(pg, '3pie')
        await pg.evaluate("switchTab('path'); go({mode:'route', from:'word:respect', to:'word:structure'})"); await pg.wait_for_timeout(1500); await shot(pg, '4route')
        await pg.evaluate("go({mode:'home'})"); await pg.wait_for_timeout(600)
        await pg.evaluate("openIndex(true)"); await pg.wait_for_timeout(400); await shot(pg, '5index')
        await pg.evaluate("openIndex(false); openFav(true)"); await pg.wait_for_timeout(400); await shot(pg, '6fav')
        await pg.evaluate("openFav(false)")
        pg2 = await page(360, 640, True)
        await pg2.evaluate("go({mode:'focus', id:'word:restaurant'})"); await pg2.wait_for_timeout(1500); await shot(pg2, '7small')
        pc = await page(1440, 900, False)
        await pc.evaluate("go({mode:'focus', id:'word:inspect'})"); await pc.wait_for_timeout(1500); await shot(pc, '8pc')
        print('errors', errs); await b.close()
asyncio.run(main())
