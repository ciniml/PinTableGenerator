from typing import Tuple, Dict, Union
import svgwrite

def __conv_to_svg_color(color: Union[int,str]) -> str:
    return f'#{color:06X}' if type(color) == 'int' else color

def generate_pin_map_svg(pin_map: Tuple[Tuple[str]], pin_definitions: Dict[str, Dict[str, str]], pin_type_colors: Dict[str, int], usage_type_colors: Dict[str, int], column_width:int = 120, usage_column_width:int = 80, row_height = 20) -> svgwrite.Drawing:
    drawing = svgwrite.Drawing()

    for row_index, row in enumerate(pin_map):
        y = row_height * row_index
        for column_index, pin in enumerate(row):
            x = column_width * column_index
            if pin == "": continue  # Skip blank pin
             
            pin_definition = pin_definitions.get(pin, {'type': 'normal'})
            pin_type = pin_definition['type']
            pin_usage = pin_definition.get('usage')
            pin_usage_type = pin_definition.get('usage_type')
            pin_color = pin_type_colors.get(pin_type, ('black', 'white'))
            fill = __conv_to_svg_color(pin_color[0])
            text_color = __conv_to_svg_color(pin_color[1])

            if pin_usage is None:
                rect = drawing.rect(insert=(x, y), size=(column_width, row_height), fill=fill)
                drawing.add(rect)
                text = drawing.text(pin, insert=(x+column_width/2, y+row_height/2), style='text-anchor:middle; dominant-baseline:central', fill=text_color)
                drawing.add(text)
            else:
                pin_start_x = x if column_index == 0 else x + usage_column_width
                pin_column_width = column_width - usage_column_width
                usage_start_x = x + column_width - usage_column_width if column_index == 0 else x

                rect = drawing.rect(insert=(pin_start_x, y), size=(pin_column_width, row_height), fill=fill)
                drawing.add(rect)
                text = drawing.text(pin, insert=(pin_start_x+pin_column_width/2, y+row_height/2), style='text-anchor:middle; dominant-baseline:central', fill=text_color)
                drawing.add(text)

                usage_color = usage_type_colors[pin_usage_type]
                usage_fill = __conv_to_svg_color(usage_color[0])
                usage_text_color = __conv_to_svg_color(usage_color[1])
                rect = drawing.rect(insert=(usage_start_x, y), size=(usage_column_width, row_height), fill=usage_fill)
                drawing.add(rect)
                text = drawing.text(pin_usage, insert=(usage_start_x+usage_column_width/2, y+row_height/2), style='text-anchor:middle; dominant-baseline:central', fill=usage_text_color)
                drawing.add(text)

    return drawing

def generate_pin_map_svg_from_json(def_json_path: str, color_json_path: str, **kwargs) -> svgwrite.Drawing:
    import json5
    with open(def_json_path, 'r') as f:
        definitions = json5.load(f)
    with open(color_json_path, 'r') as f:
        colors = json5.load(f)
    
    return generate_pin_map_svg(definitions['pin_map'], definitions['pin_definitions'], colors['pin_type_colors'], colors['usage_type_colors'], **kwargs) 

if __name__ == '__main__':
    import sys
    import os
    from optparse import OptionParser
    parser = OptionParser()
    parser.set_usage("pin_table_gen.py DEF_JSON COLOR_JSON [options]")
    parser.add_option('-o', "--output", dest="output_file", help="output file name", metavar="OUTPUT")
    parser.add_option("--column_width", type="int", dest="column_width", help="column width of the table", metavar="COLUMN_WIDTH", default=120)
    parser.add_option("--usage_column_width", type="int", dest="usage_column_width", help="column width of the table for the usage cell", metavar="USAGE_COLUMN_WIDTH", default=80)
    parser.add_option('--row_height', type="int", dest="row_height", help="row height of the table", metavar="ROW_HEIGHT", default=20)
    (option, args) = parser.parse_args()
    if len(args) < 2:
        parser.print_help()
        sys.exit(1)
    def_json_path = args[0]
    color_json_path = args[1]
    output_path = os.path.splitext(args[0])[0] + '.svg' if option.output_file is None else option.output_file
    
    if option.column_width <= option.usage_column_width:
        print("Error: COLUMN_WIDTH must be wider than USAGE_COLUMN_WIDTH", file=sys.stderr)
        sys.exit(1)

    optional_args = {}
    optional_args['column_width'] = option.column_width
    optional_args['usage_column_width'] = option.usage_column_width
    optional_args['row_height'] = option.row_height
    
    drawing = generate_pin_map_svg_from_json(def_json_path, color_json_path, **optional_args)
    drawing.saveas(output_path)