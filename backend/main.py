from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time

jogos = [
    {"id": 1, "titulo": "The Legend of Zelda™: Echoes of Wisdom", "desenvolvedor": "Nintendo", "quantidade": 20, "preco": 299.0},
    {"id": 2, "titulo": "ASTRO BOT", "desenvolvedor": "Team Asobi", "quantidade": 15, "preco": 299.9},
    {"id": 3, "titulo": "SILENT HILL 2", "desenvolvedor": "Konami", "quantidade": 10, "preco": 349.9},
]

app = FastAPI()

class Jogo(BaseModel):
    id: Optional[int] = None
    titulo: str
    desenvolvedor: str
    quantidade: int
    preco: float


class VendaJogo(BaseModel):
    quantidade: int


class AtualizarJogo(BaseModel):
    titulo: Optional[str] = None
    desenvolvedor: Optional[str] = None
    quantidade: Optional[int] = None
    preco: Optional[float] = None


def gerar_proximo_id():
    if jogos:
        return max(jogo['id'] for jogo in jogos) + 1
    else:
        return 1


def buscar_jogo_por_id(jogo_id: int):
    for jogo in jogos:
        if jogo["id"] == jogo_id:
            return jogo
    return None

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s")
    return response

@app.post("/api/v1/jogos/", status_code=201)
def adicionar_jogo(jogo: Jogo):
    for j in jogos:
        if j["desenvolvedor"].lower() == jogo.desenvolvedor.lower() and j["titulo"].lower() == jogo.titulo.lower():
            raise HTTPException(status_code=400, detail="O jogo já se encontra cadastrado no sistema.")

    novo_jogo = jogo.dict()
    novo_jogo['id'] = gerar_proximo_id()

    jogos.append(novo_jogo)
    return {"message": "Jogo cadastrado com sucesso!", "jogo": novo_jogo}

@app.get("/api/v1/jogos/", response_model=List[Jogo])
def listar_jogos():
    return jogos

@app.get("/api/v1/jogos/{jogo_id}")
def listar_jogo_por_id(jogo_id: int):
    jogo = buscar_jogo_por_id(jogo_id)
    if jogo is None:
        raise HTTPException(status_code=404, detail="Jogo não encontrado.")
    return jogo

@app.put("/api/v1/jogos/{jogo_id}/vender/")
def vender_jogo(jogo_id: int, venda: VendaJogo):
    jogo = buscar_jogo_por_id(jogo_id)

    if jogo is None:
        raise HTTPException(status_code=404, detail="Jogo não encontrado.")

    if jogo["quantidade"] < venda.quantidade:
        raise HTTPException(status_code=400, detail="Quantidade insuficiente no estoque.")

    jogo["quantidade"] -= venda.quantidade
    return {"message": "Venda realizada com sucesso!", "jogo": jogo}

@app.patch("/api/v1/jogos/{jogo_id}")
def atualizar_jogo(jogo_id: int, jogo_atualizacao: AtualizarJogo):
    jogo = buscar_jogo_por_id(jogo_id)
    if jogo is None:
        raise HTTPException(status_code=404, detail="Jogo não encontrado.")

    if jogo_atualizacao.titulo is not None:
        jogo["titulo"] = jogo_atualizacao.titulo
    if jogo_atualizacao.desenvolvedor is not None:
        jogo["desenvolvedor"] = jogo_atualizacao.desenvolvedor
    if jogo_atualizacao.quantidade is not None:
        jogo["quantidade"] = jogo_atualizacao.quantidade
    if jogo_atualizacao.preco is not None:
        jogo["preco"] = jogo_atualizacao.preco

    return {"message": "Jogo atualizado com sucesso!", "jogo": jogo}

@app.delete("/api/v1/jogos/{jogo_id}")
def remover_jogo(jogo_id: int):
    for i, jogo in enumerate(jogos):
        if jogo["id"] == jogo_id:
            del jogos[i]
            return {"message": "Jogo removido com sucesso!"}

@app.delete("/api/v1/jogos/")
def resetar_jogos():
    global jogos
    jogos = [
        {"id": 1, "titulo": "The Legend of Zelda™: Echoes of Wisdom", "desenvolvedor": "Nintendo", "quantidade": 20,
         "preco": 299.0},
        {"id": 2, "titulo": "ASTRO BOT", "desenvolvedor": "Team Asobi", "quantidade": 15, "preco": 299.9},
        {"id": 3, "titulo": "SILENT HILL 2", "desenvolvedor": "Konami", "quantidade": 10, "preco": 349.9},
    ]
    return {"message": "Repositorio limpo com sucesso!", "jogos": jogos}