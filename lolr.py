from __future__ import annotations

from utils import Trie


class Champion:
    def __init__(self, name: str, gender: str, position: list[str], species: list[str], resource: str, range_type: list[str], region: list[str], release_year: int) -> None:
        self.name = name
        self.gender = gender
        self.position = position
        self.species = species
        self.resource = resource
        self.range_type = range_type
        self.region = region
        self.release_year = release_year

    @staticmethod
    def from_dict(data) -> Champion:
        return Champion(data["name"], data["gender"], data["position"], data["species"], data["resource"], data["range_type"], data["region"], data["release_year"])

    @staticmethod
    def from_list(data) -> list[Champion]:
        return [Champion.from_dict(entry) for entry in data]


class Lolr:
    def __init__(self, data) -> None:
        self.trie = Trie()
        self.champions = Champion.from_list(data)
        self.index_champions()

    def index_champions(self):
        for idx, champion in enumerate(self.champions):
            self.trie.insert(champion.name.lower())
            self.trie.get_trie(champion.name.lower()).value = idx

    def search(self, term) -> list[str]:
        return self.trie.autocomplete(term)

    def get_champion_index(self, name):
        return self.trie.get_trie(name.lower()).value

    def get_champion(self, name: str):
        return self.champions[self.get_champion_index(name)]
