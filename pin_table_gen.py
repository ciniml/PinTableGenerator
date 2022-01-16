import svgwrite
from typing import Tuple, Dict

def generate_pin_map_svg(pin_map: Tuple[Tuple[str]], pin_definitions: Dict[str, Dict[str, str]], pin_type_colors: Dict[str, int], usage_type_colors: Dict[str, int], column_width:int = 120, column_usage_width:int = 80, row_height = 20) -> svgwrite.Drawing:
    drawing = svgwrite.Drawing()

    column_width = 120
    column_usage_width = 80
    row_height = 20

    y = 0
    for row_index, row in enumerate(pin_map):
        y = row_height * row_index
        for column_index, pin in enumerate(row):
            x = column_width * column_index
            pin_definition = pin_definitions.get(pin, {'type': 'normal'})
            pin_type = pin_definition['type']
            pin_usage = pin_definition.get('usage')
            pin_usage_type = pin_definition.get('usage_type')
            pin_color = pin_type_colors.get(pin_type, (0x000000, 0xffffff))
            fill = f'#{pin_color[0]:06X}'
            text_color = f'#{pin_color[1]:06X}'

            if pin_usage is None:
                rect = drawing.rect(insert=(x, y), size=(column_width, row_height), fill=fill)
                drawing.add(rect)
                text = drawing.text(pin, insert=(x+column_width/2, y+row_height/2), style='text-anchor:middle; dominant-baseline:central', fill=text_color)
                drawing.add(text)
            else:
                pin_start_x = x if column_index == 0 else x + column_usage_width
                pin_column_width = column_width - column_usage_width
                usage_start_x = x + column_width - column_usage_width if column_index == 0 else x

                rect = drawing.rect(insert=(pin_start_x, y), size=(pin_column_width, row_height), fill=fill)
                drawing.add(rect)
                text = drawing.text(pin, insert=(pin_start_x+pin_column_width/2, y+row_height/2), style='text-anchor:middle; dominant-baseline:central', fill=text_color)
                drawing.add(text)

                usage_color = usage_type_colors[pin_usage_type]
                usage_fill = f'#{usage_color[0]:06X}'
                usage_text_color = f'#{usage_color[1]:06X}'
                rect = drawing.rect(insert=(usage_start_x, y), size=(column_usage_width, row_height), fill=usage_fill)
                drawing.add(rect)
                text = drawing.text(pin_usage, insert=(usage_start_x+column_usage_width/2, y+row_height/2), style='text-anchor:middle; dominant-baseline:central', fill=usage_text_color)
                drawing.add(text)

    return drawing
