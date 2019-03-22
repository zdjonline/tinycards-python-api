import csv
from dataclasses import dataclass, field
from typing import List

from .card import Card


# @dataclass
# class Deck:
#     """Data class for a Tinycards deck entity."""
#     id: str
#     user_id: str
#     creation_timestamp: int
#     title: str
#     description: str
#     visibility: str = 'everyone'
#     front_language: str = None
#     back_language: str = None
#     cards: List[Card] = field(default_factory=list)


class Deck(object):
    """Data class for an Tinycards deck entity."""

    def __init__(self,
                 title,
                 description=None,
                 cover=None,
                 deck_id=None,
                 front_language=None,
                 back_language=None,
                 cards=None,
                 private=False,
                 shareable=False,
                 slug='',
                 compact_id=''):
        '''
        Initialize a new instance of the Deck class.
        Args:
            cover (string, optional):
                The cover image of this deck. If set to a file path, the corresponding file will be uploaded to Tinycards.
                After creating or updating a deck, this field will be set to the URL of the cover image.
            private (bool, optional):
                If set to False (the default), the deck will be publicly available.
                If set to True, it will not. If you need a "shareable link", please also set shareable to True.
                See also below "Visibility of the deck" section.
            shareable (bool, optional):
                If set to False (the default), the deck will not have any "shareable link" associated to it.
                If set to True, it will. Once the deck has been created, the link generated by Tinycards is accessible via the shareable_link attribute.
                See also below "Visibility of the deck" section.
            slug (string, optional): short name for the Deck. Only returned by Tinycards upon Deck creation.
            compact_id (string, optional): short unique ID for the deck. Only returned by Tinycards upon Deck creation.

        Visibility of the deck:
            Tinycards' UI let's you specifiy that a deck is visible to:
            - Everyone
            - People with a private link
            - Only me
            To achieve the equivalent using Tinycards' API, one needs to correctly set the private and shareable flags:
            - Everyone:                     private=False,  shareable=False
            - People with a private link:   private=True,   shareable=True
            - Only me:                      private=True,   shareable=False

        '''
        # IDs:
        self.id = deck_id
        self.slug = slug
        self.compact_id = compact_id

        self.creation_timestamp = None
        self.title = title
        self.description = description
        self.cover = cover
        self.cards = cards if cards else []
        # Visibility:
        self.private = private
        self.shareable = shareable
        self.shareable_link = 'https://tiny.cards/decks/%s/%s' % (compact_id, slug) if private and shareable and compact_id and slug else ''

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def add_card(self, card):
        """Add a new card to the deck."""
        if isinstance(card, tuple) and len(card) == 2:
            new_card = Card(front=card[0], back=card[1])
        else:
            raise ValueError("Invalid card used as argument")
        self.cards.append(new_card)

    def add_cards_from_csv(self, csv_file,
                           front_column='front',
                           back_column='back'):
        """Add word pairs from a CSV file as cards to the deck.

        Args:
            csv_file: The file buffer that contains the CSV data.
            front_column (str): Optional name for the 'front' column.
            back_column (str): Optional name for the 'back' column.

        Example:
            >>> with open(csv_path, 'r') as csv_file:
            >>>     deck.add_cards_from_csv(csv_file)

        """
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            current_word_pair = (row[front_column], row[back_column])
            self.add_card(current_word_pair)

    def save_cards_to_csv(self, csv_file,
                          front_column='front',
                          back_column='back'):
        """Save the word pairs from the deck's cards to a CSV file.

        Args:
            csv_file: The file buffer to store the CSV data in.
            front_column (str): Optional name for the 'front' column.
            back_column (str): Optional name for the 'back' column.

        Example:
            >>> with open(csv_path, 'w') as csv_file:
            >>>     deck.save_cards_to_csv(csv_file)

        """
        csv_writer = csv.DictWriter(csv_file,
                                    fieldnames=[front_column, back_column])
        # Add header row first.
        csv_writer.writeheader()
        # Then add all cards as rows.
        for card in self.cards:
            front_word = card.front.concepts[0].fact.text
            back_word = card.back.concepts[0].fact.text
            csv_writer.writerow({front_column: front_word,
                                 back_column: back_word})
