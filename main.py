#!/usr/bin/env python3

import os
import curses

import json
from lolr import Champion, Lolr
import random


color_map = {"✓": 1,
             " ": 0,
             "*": 2,
             "<": 0,
             ">": 0}


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    with open("lol.json", "r") as f:
        data = json.load(f)

    lolr = Lolr(data)

    rows, cols = stdscr.getmaxyx()

    tried: list[str] = []
    tried_champs: list[Champion] = []

    winner_champ = random.choice(lolr.champions)

    stdscr.clear()
    stdscr.refresh()

    current_input = ""

    tried_champ_offset = 0
    tried_champ_max_show = rows - 16
    max_suggestions = 12
    suggestion_offset = 0

    confirm_quit = False
    while True:
        suggestions = list(filter(lambda x: x not in tried,
                           lolr.search(current_input)))

        stdscr.erase()
        stdscr.addstr(f"> {current_input}\n\n")

        for suggestion in suggestions[suggestion_offset:max_suggestions+suggestion_offset]:
            stdscr.addstr(f"{suggestion}\n")

        stdscr.move(4+max_suggestions, 0)
        for champion in tried_champs[::-1][tried_champ_offset:tried_champ_offset+tried_champ_max_show]:
            name_comp = "✓" if champion.name == winner_champ.name else " "
            gender_comp = "✓" if champion.gender == winner_champ.gender else " "
            if champion.position == winner_champ.position:
                position_comp = "✓"
            elif any([val in winner_champ.position for val in champion.position]):
                position_comp = "*"
            else:
                position_comp = " "

            if champion.species == winner_champ.species:
                species_comp = "✓"
            elif any([val in winner_champ.species for val in champion.species]):
                species_comp = "*"
            else:
                species_comp = " "

            resource_comp = "✓" if champion.resource == winner_champ.resource else " "

            if champion.range_type == winner_champ.range_type:
                range_type_comp = "✓"
            elif any([val in winner_champ.range_type for val in champion.range_type]):
                range_type_comp = "*"
            else:
                range_type_comp = " "

            if champion.region == winner_champ.region:
                region_comp = "✓"
            elif any([val in winner_champ.region for val in champion.species]):
                region_comp = "*"
            else:
                region_comp = " "

            if champion.release_year > winner_champ.release_year:
                release_year_comp = "<"
            elif champion.release_year < winner_champ.release_year:
                release_year_comp = ">"
            else:
                release_year_comp = "✓"

            stdscr.addstr(f"{champion.name}{name_comp}  ",
                          curses.color_pair(color_map[name_comp]))
            stdscr.addstr(f"{champion.gender}{gender_comp}  ",
                          curses.color_pair(color_map[gender_comp]))
            stdscr.addstr(f"{','.join(champion.position)}{position_comp}  ",
                          curses.color_pair(color_map[position_comp]))
            stdscr.addstr(
                f"{','.join(champion.species)}{species_comp}  ", curses.color_pair(color_map[species_comp]))
            stdscr.addstr(f"{champion.resource}{resource_comp}  ",
                          curses.color_pair(color_map[resource_comp]))
            stdscr.addstr(
                f"{','.join(champion.range_type)}{range_type_comp}  ", curses.color_pair(color_map[range_type_comp]))
            stdscr.addstr(
                f"{','.join(champion.region)}{region_comp}  ", curses.color_pair(color_map[region_comp]))
            stdscr.addstr(f"{champion.release_year} {release_year_comp}\n",
                          curses.color_pair(color_map[release_year_comp]))

        stdscr.move(0, len(current_input)+2)

        key = stdscr.getch()
        is_escape = key == 27
        is_tab = key == 9
        isenter = key == curses.KEY_ENTER or key == 13 or key == 10

        if is_escape and confirm_quit:
            break
        elif is_escape:
            confirm_quit = True
            continue
        confirm_quit = False
        if key == curses.KEY_BACKSPACE:
            current_input = current_input[:-1]
            continue
        elif is_tab:
            if len(suggestions):
                current_input = suggestions[0]
            continue

        elif key == curses.KEY_DOWN:
            if len(tried) > tried_champ_max_show:
                tried_champ_offset += 1
                if tried_champ_offset > len(tried) - tried_champ_max_show:
                    tried_champ_offset = len(tried) - tried_champ_max_show
            continue

        elif key == curses.KEY_UP:
            tried_champ_offset -= 1
            if tried_champ_offset < 0:
                tried_champ_offset = 0
            continue

        elif key == curses.KEY_RIGHT:
            suggestion_offset += 1

            suggestion_offset = min(
                len(suggestions) - max_suggestions, suggestion_offset)

            continue

        elif key == curses.KEY_LEFT:
            suggestion_offset -= 1
            suggestion_offset = max(0, suggestion_offset)
            continue

        elif isenter:
            if current_input in suggestions:
                tried.append(current_input)
                tried_champs.append(lolr.get_champion(current_input))
                current_input = ""
            continue

        current_input += chr(key)
        suggestion_offset = 0


if __name__ == "__main__":
    os.environ.setdefault('ESCDELAY', '25')
    curses.wrapper(main)
