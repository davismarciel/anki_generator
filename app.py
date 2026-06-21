import io
import random
import tempfile
from pathlib import Path

import genanki
from flask import Flask, render_template_string, request, send_file

app = Flask(__name__)

HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Anki Deck Generator</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #0f0f0f;
            color: #e0e0e0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            padding: 40px 20px;
        }

        .container {
            width: 100%;
            max-width: 700px;
        }

        h1 {
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 8px;
            color: #fff;
        }

        .subtitle {
            color: #888;
            margin-bottom: 32px;
            font-size: 0.95rem;
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            font-weight: 500;
            margin-bottom: 8px;
            font-size: 0.9rem;
            color: #aaa;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px 14px;
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            color: #fff;
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.2s;
        }

        input[type="text"]:focus {
            border-color: #5b7ff5;
        }

        textarea {
            width: 100%;
            min-height: 280px;
            padding: 14px;
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            color: #fff;
            font-family: 'Cascadia Code', 'Fira Code', monospace;
            font-size: 0.9rem;
            line-height: 1.6;
            resize: vertical;
            outline: none;
            transition: border-color 0.2s;
        }

        textarea:focus {
            border-color: #5b7ff5;
        }

        textarea::placeholder {
            color: #555;
        }

        .help-text {
            font-size: 0.8rem;
            color: #666;
            margin-top: 6px;
        }

        .btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 12px 28px;
            background: #5b7ff5;
            color: #fff;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 500;
            cursor: pointer;
            transition: background 0.2s;
            margin-top: 8px;
        }

        .btn:hover {
            background: #4a6de0;
        }

        .btn:active {
            background: #3d5cc5;
        }

        .error {
            background: #2a1515;
            border: 1px solid #5c2020;
            color: #f08080;
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 0.9rem;
        }

        .stats {
            display: inline-block;
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 6px;
            padding: 4px 12px;
            font-size: 0.8rem;
            color: #888;
            margin-left: 12px;
            vertical-align: middle;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Anki Deck Generator</h1>
        <p class="subtitle">Gere decks .apkg para estudar qualquer idioma</p>

        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}

        <form method="POST" action="/generate">
            <div class="form-group">
                <label for="deck_name">Nome do Deck</label>
                <input type="text" id="deck_name" name="deck_name"
                      value="{{ deck_name or 'Idioma - Estudos' }}"
                      placeholder="Idioma - Estudos">
            </div>

            <div class="form-group">
                <label for="cards">
                    Cards
                    <span class="stats" id="count">0 cards</span>
                </label>
                <textarea id="cards" name="cards" placeholder="termo,tradução&#10;segunda-feira,monday&#10;terça-feira,tuesday&#10;quarta-feira,wednesday&#10;quinta-feira,thursday&#10;sexta-feira,friday">{{ cards or '' }}</textarea>
                <p class="help-text">Um card por linha no formato: <strong>termo,tradução</strong></p>
            </div>

            <button type="submit" class="btn">Gerar Deck .apkg</button>
        </form>
    </div>

    <script>
        const textarea = document.getElementById('cards');
        const count = document.getElementById('count');

        function updateCount() {
            const lines = textarea.value.split('\n').filter(l => l.trim() && l.includes(','));
            count.textContent = lines.length + ' card' + (lines.length !== 1 ? 's' : '');
        }

        textarea.addEventListener('input', updateCount);
        updateCount();
    </script>
</body>
</html>
"""


def parse_cards(raw: str) -> list[tuple[str, str]]:
    cards = []
    for line in raw.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(",", 1)
        if len(parts) != 2:
            continue
        front, back = parts[0].strip(), parts[1].strip()
        if front and back:
            cards.append((front, back))
    return cards


def build_apkg(deck_name: str, cards: list[tuple[str, str]]) -> io.BytesIO:
    model = genanki.Model(
        1607392319,
        "Generic Simple Model",
        fields=[
            {"name": "Coreano"},
            {"name": "Traducao"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "{{Coreano}}",
                "afmt": '{{FrontSide}}<hr style="text-align: center;"id="answer">{{Traducao}}',
            },
        ],
        css=""".card {
  font-family: \"Malgun Gothic\", \"Apple SD Gothic Neo\", sans-serif;
  font-size: 45px;
  text-align: center;
  color: #2c3e50;
  background-color: #fdfdfd;
}

.hangul {
  font-size: 48px;
  font-weight: bold;
  color: #e74c3c;
}

.exemplo {
  font-style: italic;
  font-size: 18px;
  color: #7f8c8d;
  margin-top: 10px;
}""",
    )

    deck_id = random.randrange(1 << 30, 1 << 31)
    deck = genanki.Deck(deck_id, deck_name)

    for front, back in cards:
        note = genanki.Note(model=model, fields=[front, back])
        deck.add_note(note)

    buf = io.BytesIO()
    with tempfile.NamedTemporaryFile(suffix=".apkg", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    genanki.Package(deck).write_to_file(str(tmp_path))
    buf.write(tmp_path.read_bytes())
    tmp_path.unlink(missing_ok=True)
    buf.seek(0)
    return buf


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/generate", methods=["POST"])
def generate():
    deck_name = request.form.get("deck_name", "").strip() or "Idioma - Estudos"
    raw_cards = request.form.get("cards", "")

    cards = parse_cards(raw_cards)
    if not cards:
        return render_template_string(
            HTML_TEMPLATE,
            error="Nenhum card válido encontrado. Use o formato: lingua,tradução",
            deck_name=deck_name,
            cards=raw_cards,
        )

    filename = deck_name.replace(" ", "_") + ".apkg"
    buf = build_apkg(deck_name, cards)

    return send_file(
        buf,
        as_attachment=True,
        download_name=filename,
        mimetype="application/octet-stream",
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
