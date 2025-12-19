from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from infrastructure.search_manager import SearchManager
from services.csv_converter import CSVConverter

app = FastAPI(
    title="My FastAPI Project",
    description="API documentation",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return "Second python homework!!"

@app.get("/search")
async def search_repos(limit: int, offset: int, lang: str, stars_min: int = 0, stars_max: int = 10**9, fork_min: int = 0, fork_max: int = 10**9):
    manager = SearchManager()
    parsed_json = await manager.search(limit, offset, lang, stars_min, stars_max, fork_min, fork_max)

    name = f'repositories_{lang}_{limit}_{offset}.csv'
    csv_converter = CSVConverter(parsed_json)
    csv_converter.save_csv(name=name)

    return Response(content=f'Saved with name: {name}', media_type="application/json", status_code=200)
