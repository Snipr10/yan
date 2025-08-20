import asyncio
from playwright.async_api import async_playwright

async def main():
    # Запускаем браузер
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # Создаем список для хранения ответов
        responses = []

        # Обработчик событий для перехвата ответов
        async def handle_response(response):
            url = response.url
            if "https://yandex.ru/maps/api/search?add_snippet" in url:
                try:
                    json_body = await response.json()
                    responses.append(json_body)
                    print(f"Перехвачен ответ: {url}")
                except Exception as e:
                    print(f"Ошибка при получении JSON: {e}")

        # Создаем страницу и навешиваем обработчик
        page = await context.new_page()
        page.on("response", handle_response)

        # Открываем страницу
        url = "https://yandex.ru/maps/?display-text=%D0%9E%D0%B1%D1%89%D0%B5%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B5%20%D1%82%D1%83%D0%B0%D0%BB%D0%B5%D1%82%D1%8B%20%D0%93%D0%A3%D0%9F%20%D0%92%D0%BE%D0%B4%D0%BE%D0%BA%D0%B0%D0%BD%D0%B0%D0%BB&filter=chain_id%3A182139012541&ll=30.102219%2C60.819454&mode=search&sctx=ZAAAAAgBEAAaKAoSCQzp8BDGez5AEfda0HtjBk5AEhIJOEw0SMFTyD8Rkj1CzZAqtj8iBgABAgMEBSgAOABAx4IGSAFiRnJlYXJyPXNjaGVtZV9Mb2NhbC9HZW91cHBlci9BZHZlcnRzL1JlYXJyYW5nZUJ5QXVjdGlvbi9DYWNoZS9FbmFibGVkPTFqAnJ1ggEVY2hhaW5faWQ6MTgyMTM5MDEyNTQxnQHNzMw9oAEAqAEAvQFENxUyggIVY2hhaW5faWQ6MTgyMTM5MDEyNTQxigIWOTA2NTkwOTI2NiQ2ODA0OTUwODgyN5ICATKaAgxkZXNrdG9wLW1hcHOqAgwxODIxMzkwMTI1NDE%3D&sll=30.102219%2C60.819454&sspn=1.337585%2C1.153543&text=chain_id%3A%28182139012541%29&z=9"
        await page.goto(url)

        # Ждем некоторое время, чтобы все запросы прошли (можно заменить на более точное ожидание)
        await asyncio.sleep(400)

        # Закрываем браузер
        await browser.close()

        tualet = {}
        for r  in  responses:

            for item in r.get("data").get("items"):
                try:
                    tualet[item["id"]] = {
                        "address": item['fullAddress'],
                        "titile": item['title'],
                        "coordinates": item['coordinates'],
                        "images": [i['urlTemplate'].replace("%s", "XXXL") for i in item['photos']['items']]
                    }
                except Exception as e:
                    try:
                        tualet[item["id"]] = {
                            "address": item['fullAddress'],
                            "titile": item['title'],
                            "coordinates": item['coordinates'],
                            "images": []
                        }
                    except Exception as e:
                        print(e)
        # Выводим собранные ответы
        for idx, resp in enumerate(responses):
            print(f"\nОтвет {idx + 1}:\n{resp}")

# Запуск асинхронной функции
asyncio.run(main())