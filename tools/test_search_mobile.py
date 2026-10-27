"""スマホでの検索（検索ボタン・Enter・変換確定後の Enter・候補の選択）のテスト"""
import asyncio, os
from playwright.async_api import async_playwright
TOOLS = os.path.dirname(os.path.abspath(__file__))
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); errs = []
        async def page(w, h, mobile):
            ctx = await b.new_context(viewport={'width': w, 'height': h}, is_mobile=mobile, has_touch=mobile)
            pg = await ctx.new_page(); pg.on('pageerror', lambda e: errs.append(str(e)))
            async def lib(route): await route.fulfill(path=os.path.join(TOOLS, 'node_modules/vis-network/standalone/umd/vis-network.min.js'), content_type='application/javascript')
            await pg.route('**/vis-network.min.js', lib); await pg.route('**fonts.g**', lambda r: r.abort())
            await pg.goto('http://localhost:8782/index.html'); await pg.wait_for_selector('#loading.done', timeout=60000)
            return pg
        cur = "current && current.mode === 'focus' ? current.id : (current && current.mode)"
        pg = await page(390, 844, True)
        print('touch', await pg.evaluate("TOUCH"), 'button visible', await pg.is_visible('#goBtn'))
        await pg.tap('#q'); await pg.fill('#q', 'inspect'); await pg.tap('#goBtn'); await pg.wait_for_timeout(300)
        print('1 button  ->', await pg.evaluate(cur))
        await pg.fill('#q', 'gate'); await pg.press('#q', 'Enter'); await pg.wait_for_timeout(300)
        print('2 enter   ->', await pg.evaluate(cur))
        # 変換中の Enter（keyCode 229）→ compositionend で検索
        await pg.fill('#q', 'pause')
        await pg.evaluate("""() => { const q = document.getElementById('q');
          q.dispatchEvent(new KeyboardEvent('keydown', { key: 'Process', code: 'Enter', keyCode: 229, isComposing: true, bubbles: true }));
          q.dispatchEvent(new CompositionEvent('compositionend', { data: 'pause', bubbles: true })); }""")
        await pg.wait_for_timeout(300); print('3 ime     ->', await pg.evaluate(cur))
        # 候補の選択（insertReplacementText）
        await pg.evaluate("""() => { const q = document.getElementById('q'); q.value = 'restaurant';
          q.dispatchEvent(new InputEvent('input', { inputType: 'insertReplacementText', bubbles: true })); }""")
        await pg.wait_for_timeout(300); print('4 datalist->', await pg.evaluate(cur))
        # 普通に打っているだけでは検索しない
        await pg.evaluate("go({mode:'home'})"); await pg.fill('#q', ''); await pg.type('#q', 'tea'); await pg.wait_for_timeout(300)
        print('5 typing  ->', await pg.evaluate(cur), '(home のままが正しい)')
        pc = await page(1440, 900, False)
        print('pc touch', await pc.evaluate("TOUCH"), 'button visible', await pc.is_visible('#goBtn'))
        await pc.fill('#q', 'inspect'); await pc.press('#q', 'Enter'); await pc.wait_for_timeout(300)
        print('pc enter  ->', await pc.evaluate(cur))
        print('errors', errs); await b.close()
asyncio.run(main())
