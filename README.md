# Anki Generator

Aplicação simples para gerar decks do Anki no formato .apkg a partir de pares termo,tradução.

## O que este projeto faz

- Gera decks .apkg para importar direto no Anki.
- Possui interface web com Flask para criar cards rapidamente.
- Inclui script Python para gerar deck a partir de CSV.

## Requisitos

- Python 3.14+
- Dependências do projeto instaladas

## Como inicializar

### Opção recomendada (uv)

1. Instale dependências:

```bash
uv sync
```

2. Rode a aplicação web:

```bash
uv run app.py
```

3. Acesse no navegador:

http://127.0.0.1:5000

### Opção alternativa (venv + pip)

1. Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instale as dependências:

```bash
pip install flask genanki
```

3. Rode a aplicação:

```bash
python app.py
```

## Como usar

1. Defina o nome do deck.
2. Adicione os cards, um por linha, no formato:

```text
termo,tradução
segunda-feira,monday
```

3. Clique em Gerar Deck .apkg.
4. Importe o arquivo no Anki.

## Geração via CSV (script)

O script generator.py lê um arquivo cards.csv com cabeçalhos termo e traducao e gera deck.apkg.

Exemplo de execução:

```bash
python generator.py
```

## Estrutura

- app.py: interface web e geração do arquivo .apkg
- generator.py: geração de deck via CSV
- pyproject.toml: metadados e dependências do projeto