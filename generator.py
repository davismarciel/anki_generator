import csv
import genanki

# modelo do cartão
model = genanki.Model(
    1607392319,
    'Generic Simple Model',
    fields=[
        {'name': 'Coreano'},
        {'name': 'Traducao'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Coreano}}',
            'afmt': '{{FrontSide}}<hr style="text-align: center;"id="answer">{{Traducao}}',
        },
    ],
    css='''.card {
  font-family: "Malgun Gothic", "Apple SD Gothic Neo", sans-serif;
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
}''')

deck = genanki.Deck(
    2059400110,
    'Idioma - Estudos IA'
)

# lê o CSV
with open('cards.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        note = genanki.Note(
            model=model,
            fields=[row['termo'], row['traducao']]
        )
        deck.add_note(note)

# exporta .apkg
genanki.Package(deck).write_to_file('deck.apkg')

print("Deck criado: deck.apkg")