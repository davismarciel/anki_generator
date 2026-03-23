import csv
import genanki

# modelo do cartão
model = genanki.Model(
    1607392319,
    'Generic Simple Model',
    fields=[
        {'name': 'Termo'},
        {'name': 'Tradução'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Termo}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Tradução}}',
        },
    ])

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