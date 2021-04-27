import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://discord.com/channels/542224582317441034/592829820371599451')
    #await page.screenshot({'example.png'})
    

    dimensions = await page.evaluate('''() => {
        return {
            width: document.documentElement.clientWidth,
            height: document.documentElement.clientHeight,
            deviceScaleFactor: window.devicePixelRatio,
        }
    }''')

    print(dimensions)

    content = await page.evaluate('document.body.textContent', force_expr=True)

    element = await page.querySelector('h3')

    title = await page.evaluate('(element) => element.textContent', element)

    await browser.close()

asyncio.get_event_loop().run_until_complete(main())