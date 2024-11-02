DROP TABLE IF EXISTS "vendas";
DROP TABLE IF EXISTS "jogos";

CREATE TABLE "jogos" (
    "id" SERIAL PRIMARY KEY,
    "titulo" VARCHAR(255) NOT NULL,
    "desenvolvedor" VARCHAR(255) NOT NULL,
    "quantidade" INTEGER NOT NULL,
    "preco" FLOAT NOT NULL
);

CREATE TABLE "vendas" (
    "id" SERIAL PRIMARY KEY,
    "jogo_id" INTEGER REFERENCES jogos(id) ON DELETE CASCADE,
    "quantidade_vendida" INTEGER NOT NULL,
    "valor_venda" FLOAT NOT NULL,
    "data_venda" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO "jogos" ("titulo", "desenvolvedor", "quantidade", "preco") VALUES ('The Legend of Zelda™: Echoes of Wisdom', 'Nintendo', 20, 299.00);
INSERT INTO "jogos" ("titulo", "desenvolvedor", "quantidade", "preco") VALUES ('ASTRO BOT', 'Team Asobi', 15, 299.90);
INSERT INTO "jogos" ("titulo", "desenvolvedor", "quantidade", "preco") VALUES ('SILENT HILL 2', 'Konami', 10, 349.90)
