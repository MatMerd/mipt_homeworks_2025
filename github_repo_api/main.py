from fastapi import FastAPI, Response
from infrastructure.search_manager import SearchManager
from services.csv_converter import CSVConverter
from web.application import get_app

app = get_app()


@app.get("/")
async def root() -> str:
    """
    Приветственная страница.

    :return:
    """
    return "Second python homework!!"


@app.get("/search")
async def search_repos(
    limit: int,
    offset: int,
    lang: str,
    stars_min: int = 0,
    stars_max: int = 10**9,
    fork_min: int = 0,
    fork_max: int = 10**9,
) -> Response:
    """
    Эндпоинт для поиска репозиториев по параметрам.

    :param limit: Кол-во реп
    :param offset: Сдвиг реп
    :param lang: Язык репозитория
    :param stars_min: Мин число звезд
    :param stars_max: Макс число звезд
    :param fork_min: Мин число форков
    :param fork_max: Макс число форков

    :return: Response: статус и имя файла
    """
    manager = SearchManager()
    parsed_json = await manager.search(
        limit, offset, lang, stars_min, stars_max, fork_min, fork_max
    )

    name = f"repositories_{lang}_{limit}_{offset}.csv"
    csv_converter = CSVConverter(parsed_json)
    csv_converter.save_csv(name=name)

    return Response(
        content=f"Saved with name: {name}",
        media_type="text/plain",
        status_code=200,
    )


def get_instance() -> FastAPI:
    """
    Get FastAPI instance.

    :return:
    """
    return app
