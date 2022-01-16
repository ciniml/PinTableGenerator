#!/usr/bin/env python3

from pin_table_gen import generate_pin_map_svg_from_json
import os.path

targets = {
    'atom_matrix': { 'colors': 'pin_table_colors', 'options': {'span_pin_name_without_usage': False}},
    'core': { 'colors': 'pin_table_colors', 'options': {'span_pin_name_without_usage': True}},
}

for target_name, target_defs in targets.items():
    pin_def_path = os.path.join('defs', f'pin_def_{target_name}.jsonc')
    color_def_path  = os.path.join('defs', f'{target_defs["colors"]}.jsonc')
    drawing = generate_pin_map_svg_from_json(pin_def_path, color_def_path, **target_defs['options'])
    output_path = os.path.join('outputs', f'pin_def_{target_name}.svg')
    drawing.saveas(output_path)
