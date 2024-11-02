from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import time
import asyncpg
import os

async def get_database():
    DATABASE_URL = os.environ.get("PGURL", "postgres://postgres:postgres@db:5432/jogos")
    return await asyncpg.connect(DATABASE_URL)

app = FastAPI()

class Jogo(BaseModel):
    id: Optional[int] = None
    titulo: str
    desenvolvedor: str
    quantidade: int
    preco: float

class JogoBase(BaseModel):
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

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Path: {request.url.path}, Method: {request.method}, Process Time: {process_time:.4f}s")
    return response

async def jogo_existe(titulo: str, desenvolvedor: str, conn: asyncpg.Connection):
    try:
        query = "SELECT * FROM jogos WHERE LOWER(titulo) = LOWER($1) AND LOWER(desenvolvedor) = LOWER($2)"
        result = await conn.fetchval(query, titulo, desenvolvedor)
        return result is not None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao verificar se o jogo existe: {str(e)}")

@app.post("/api/v1/jogos/", status_code=201)
async def adicionar_jogo(jogo: JogoBase):
    conn = await get_database()
    if await jogo_existe(jogo.titulo, jogo.desenvolvedor, conn):
        raise HTTPException(status_code=400, detail="Jogo já existe.")
    try:
        query = "INSERT INTO jogos (titulo, desenvolvedor, quantidade, preco) VALUES ($1, $2, $3, $4)"
        async with conn.transaction():
            result = await conn.execute(query, jogo.titulo, jogo.desenvolvedor, jogo.quantidade, jogo.preco)
            return {"message": "Jogo adicionado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Falha ao adicionar o jogo: {str(e)}")
    finally:
        await conn.close()

@app.get("/api/v1/jogos/", response_model=List[Jogo])
async def listar_jogos():
    conn = await get_database()
    try:
        query = "SELECT * FROM jogos"
        rows = await conn.fetch(query)
        jogos = [dict(row) for row in rows]
        return jogos
    finally:
        await conn.close()

@app.get("/api/v1/jogos/{jogo_id}")
async def listar_jogo_por_id(jogo_id: int):
    conn = await get_database()
    try:
        query = "SELECT * FROM jogos WHERE id = $1"
        jogo = await conn.fetchrow(query, jogo_id)
        if jogo is None:
            raise HTTPException(status_code=404, detail="Jogo não encontrado.")
        return dict(jogo)
    finally:
        await conn.close()

@app.put("/api/v1/jogos/{jogo_id}/vender/")
async def vender_jogo(jogo_id: int, venda: VendaJogo):
    conn = await get_database()
    try:
        query = "SELECT * FROM jogos WHERE id = $1"
        jogo = await conn.fetchrow(query, jogo_id)
        if jogo is None:
            raise HTTPException(status_code=404, detail="Jogo não encontrado.")

        if jogo['quantidade'] < venda.quantidade:
            raise HTTPException(status_code=400, detail="Quantidade insuficiente no estoque.")

        nova_quantidade = jogo['quantidade'] - venda.quantidade
        update_query = "UPDATE jogos SET quantidade = $1 WHERE id = $2"
        await conn.execute(update_query, nova_quantidade, jogo_id)

        valor_venda = jogo['preco'] * venda.quantidade

        insert_venda_query = """
            INSERT INTO vendas (jogo_id, quantidade_vendida, valor_venda) 
            VALUES ($1, $2, $3)
        """
        await conn.execute(insert_venda_query, jogo_id, venda.quantidade, valor_venda)

        jogo_atualizado = dict(jogo)
        jogo_atualizado['quantidade'] = nova_quantidade

        return {"message": "Venda realizada com sucesso!", "jogo": jogo_atualizado}
    finally:
        await conn.close()

@app.patch("/api/v1/jogos/{jogo_id}")
async def atualizar_jogo(jogo_id: int, jogo_atualizacao: AtualizarJogo):
    conn = await get_database()
    try:
        query = "SELECT * FROM jogos WHERE id = $1"
        jogo = await conn.fetchrow(query, jogo_id)
        if jogo is None:
            raise HTTPException(status_code=404, detail="Jogo não encontrado.")

        update_query = """
            UPDATE jogos
            SET titulo = COALESCE($1, titulo),
                desenvolvedor = COALESCE($2, desenvolvedor),
                quantidade = COALESCE($3, quantidade),
                preco = COALESCE($4, preco)
            WHERE id = $5
        """
        await conn.execute(
            update_query,
            jogo_atualizacao.titulo,
            jogo_atualizacao.desenvolvedor,
            jogo_atualizacao.quantidade,
            jogo_atualizacao.preco,
            jogo_id
        )
        return {"message": "Jogo atualizado com sucesso!"}
    finally:
        await conn.close()

@app.delete("/api/v1/jogos/{jogo_id}")
async def remover_jogo(jogo_id: int):
    conn = await get_database()
    try:
        query = "SELECT * FROM jogos WHERE id = $1"
        jogo = await conn.fetchrow(query, jogo_id)
        if jogo is None:
            raise HTTPException(status_code=404, detail="Jogo não encontrado.")

        delete_query = "DELETE FROM jogos WHERE id = $1"
        await conn.execute(delete_query, jogo_id)
        return {"message": "Jogo removido com sucesso!"}
    finally:
        await conn.close()

@app.delete("/api/v1/jogos/")
async def resetar_jogos():
    init_sql = os.getenv("INIT_SQL", "db/init.sql")
    conn = await get_database()
    try:
        with open(init_sql, 'r') as file:
            sql_commands = file.read()
        await conn.execute(sql_commands)
        return {"message": "Banco de dados limpo com sucesso!"}
    finally:
        await conn.close()


@app.get("/api/v1/vendas/")
async def listar_vendas():
    conn = await get_database()
    try:
        query = "SELECT * FROM vendas"
        rows = await conn.fetch(query)
        vendas = [dict(row) for row in rows]
        return vendas
    finally:
        await conn.close()
