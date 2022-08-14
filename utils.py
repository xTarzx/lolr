from __future__ import annotations
import csv
import json


def csv_to_json(csv_file_path, json_file_path):
    data = []
    with open(csv_file_path, "r") as csvf:
        csv_reader = csv.DictReader(csvf)

        for entry in csv_reader:
            name = entry["Name"]
            if not name:
                continue
            gender = entry["Gender"]
            position = entry["Position"].split(";")
            species = entry["Species"].split(";")
            resource = entry["Resource"]
            range_type = entry["Range"].split(";")
            region = entry["Region"].split(";")
            release_year = int(entry["Release"])

            data.append({
                "name": name,
                "gender": gender,
                "position": position,
                "species": species,
                "resource": resource,
                "range_type": range_type,
                "region": region,
                "release_year": release_year
            })

        with open(json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)


class Trie:
    def __init__(self, is_end=False):
        self.tree: dict[str, Trie] = {}
        self.is_end = is_end
        self.value = None

    def insert(self, string: str):
        f, rest = string[:1], string[1:]

        if f not in self.tree:
            self.tree[f] = Trie()

        if not rest:
            self.tree[f].is_end = True
        else:
            self.tree[f].insert(rest)

    def search(self, term: str):
        f, rest = term[:1], term[1:]

        if f not in self.tree:
            return False

        if not rest and self.tree[f].is_end:
            return True

        return self.tree[f].search(rest)

    def contains(self, term: str):
        f, rest = term[:1], term[1:]

        if f not in self.tree:
            return False

        if not rest:
            return True

        return self.tree[f].contains(rest)

    def get_trie(self, term: str) -> Trie:
        f, rest = term[:1], term[1:]

        if f not in self.tree:
            return None

        if not rest:
            return self.tree[f]

        return self.tree[f].get_trie(rest)

    def walk(self):
        res = []
        for k, trie in self.tree.items():
            word = k

            if trie.is_end:
                res.append(word)

            if trie.tree:
                for entry in trie.walk():
                    res.append(word+entry)

        return res

    def autocomplete(self, term: str):
        res = []
        if self.contains(term):
            base_trie = self.get_trie(term)

            if self.search(term):
                res.append(term)

            for entry in base_trie.walk():
                res.append(term+entry)

        return res
