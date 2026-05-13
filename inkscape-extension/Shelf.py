import inkex
from inkex import Rectangle, Group, TextElement, PathElement


SPECIAL_OBJECT_COLORS = {
    'WALL': '#0000ff',
    'START': '#00ff00',
    'END': '#ff0000',
}


class ShelfNameHolder:

    def __init__(self, base, number, side):
        self.base = base
        self.number = number
        self.side = side

    def get_full_name(self):
        return "{}-{}-{}".format(self.base, self.number, self.side)

    def get_base_and_number(self):
        return "{}-{}".format(self.base, self.number)


def draw_rect(x, y, w, h, width, fill, name, parent):
    """Draw an SVG Rectangle"""
    rect = parent.add(Rectangle(x=str(x), y=str(y), width=str(w), height=str(h)))
    rect.style = {'stroke': '#000000', 'stroke-width': str(width), 'fill': fill}
    rect.label = name


def draw_horizontal_text(w, h, target_text, parent):
    font_size = 0.8 * h

    txt_args = {
        "x": str(w / 2),
        "y": str(font_size),
        'text-anchor': 'middle',
        'text-align': 'center',
        "font-size": str(font_size),
        "id": "text-" + target_text
    }

    text_element = TextElement(**txt_args)
    text_element.text = target_text
    parent.add(text_element)


def draw_vertical_text(w, h, target_text, parent):
    font_size = 0.8 * w

    txt_args = {
        "x": str(-h / 2),
        "y": str(font_size),
        'text-anchor': 'middle',
        'text-align': 'center',
        "font-size": str(font_size),
        "id": "text-" + target_text,
        "transform": "rotate(-90)"
    }

    text_element = TextElement(**txt_args)
    text_element.text = target_text
    parent.add(text_element)


def draw_smaller_text(w, h, target_text, parent):
    font_size = 0.3 * w

    txt_args = {
        "x": str(w / 2),
        "y": str((h + font_size) / 2),
        'text-anchor': 'middle',
        'text-align': 'center',
        "font-size": str(font_size),
        "id": "text-" + target_text,
    }

    text_element = TextElement(**txt_args)
    text_element.text = target_text
    parent.add(text_element)


def draw_text(w, h, target_text, parent):
    if w > 3 * h:
        draw_horizontal_text(w, h, target_text, parent)
    elif h > 3 * w:
        draw_vertical_text(w, h, target_text, parent)
    else:
        draw_smaller_text(w, h, target_text, parent)


def get_side_line_coordinates(w, h, direction):
    diff_ratio = .93

    if direction == 'U':
        x1 = w * (1 - diff_ratio)
        x2 = w * diff_ratio
        y1 = h * (1 - diff_ratio)
        y2 = h * (1 - diff_ratio)
        return x1, x2, y1, y2

    if direction == 'D':
        x1 = w * (1 - diff_ratio)
        x2 = w * diff_ratio
        y1 = h * diff_ratio
        y2 = h * diff_ratio
        return x1, x2, y1, y2

    if direction == 'R':
        x1 = w * diff_ratio
        x2 = w * diff_ratio
        y1 = h * (1 - diff_ratio)
        y2 = h * diff_ratio
        return x1, x2, y1, y2

    if direction == 'L':
        x1 = w * (1 - diff_ratio)
        x2 = w * (1 - diff_ratio)
        y1 = h * (1 - diff_ratio)
        y2 = h * diff_ratio
        return x1, x2, y1, y2


def draw_side_line(w, h, direction, parent):
    line = parent.add(PathElement())
    line.style = {'stroke': '#00ff00', 'stroke-width': str(min(w, h) / 5), 'fill': 'none', "stroke-opacity": "0.5"}

    x1, x2, y1, y2 = get_side_line_coordinates(w, h, direction)

    line.path = 'M {},{} L {},{}'.format(x1, y1, x2, y2)


def draw_rectangle_with_text_name(x, y, w, h, width, fill, name, direction, parent):
    group_attributes = {
        'transform': 'translate({},{})'.format(x, y),
        'id': "shelf-{}".format(name.get_full_name()),
    }

    one_shelf_group = parent.add(Group(**group_attributes))

    draw_rect(0, 0, w, h, width, fill, name.get_full_name(), one_shelf_group)
    draw_text(w, h, name.get_base_and_number(), one_shelf_group)
    draw_side_line(w, h, direction, one_shelf_group)


def print_shelf(width, height, name, current_column_idx, start, diff, direction, rotation, parent):
    act = start + diff * current_column_idx
    x = 0
    y = 0
    if rotation == "R":
        x = current_column_idx * width
    if rotation == "L":
        x = -current_column_idx * width
    if rotation == "D":
        y = current_column_idx * height
    if rotation == "U":
        y = -current_column_idx * height

    name_holder = ShelfNameHolder(name, act, direction)

    draw_rectangle_with_text_name(x, y, width, height, 0.1, 'none', name_holder, direction, parent)


def generate_shelf(options, svg):
    cols_count = options.cols
    facing_width = options.facing_width / 10
    shelf_depth = options.shelf_depth / 10
    name = options.name
    rotation, direction = options.layout_and_side.split('-')

    if rotation in ('U', 'D'):
        width = shelf_depth
        height = facing_width
    else:
        width = facing_width
        height = shelf_depth
    start = options.start
    diff = options.diff

    cx, cy = get_viewport_center(svg)
    total_w = width * cols_count if rotation in ('L', 'R') else width
    total_h = height * cols_count if rotation in ('U', 'D') else height

    if rotation == 'R':
        origin_x = cx - total_w / 2
    elif rotation == 'L':
        origin_x = cx + total_w / 2 - width
    else:
        origin_x = cx - width / 2

    if rotation == 'D':
        origin_y = cy - total_h / 2
    elif rotation == 'U':
        origin_y = cy + total_h / 2 - height
    else:
        origin_y = cy - height / 2

    parent_group = svg.add(Group.new("Shelf:{}-{}+{}x{}".format(name, start, diff, cols_count)))
    parent_group.transform = "translate({},{})".format(origin_x, origin_y)

    for i in range(0, cols_count):
        print_shelf(width, height, name, i, start, diff, direction, rotation, parent_group)

    return parent_group


def get_viewport_center(svg):
    nv = svg.namedview
    try:
        cx = float(nv.get('inkscape:cx') or 0) / svg.scale
        cy = float(nv.get('inkscape:cy') or 0) / svg.scale
        return cx, cy
    except (TypeError, ValueError):
        return 0, 0


def generate_special_object(options, svg):
    object_type = options.object_type
    width = options.obj_width
    height = options.obj_height

    fill = SPECIAL_OBJECT_COLORS.get(object_type, '#888888')

    cx, cy = get_viewport_center(svg)
    rect = Rectangle(
        x=str(cx - width / 2),
        y=str(cy - height / 2),
        width=str(width),
        height=str(height),
    )
    rect.style = {
        'fill': fill,
        'stroke': 'none',
    }
    rect.label = object_type

    return rect


class WarehouseShelfDesigner(inkex.GenerateExtension):

    def add_arguments(self, pars):
        pars.add_argument("--tab", type=str, default="tab_shelf")
        pars.add_argument("--cols", type=int, default=5)
        pars.add_argument("--facing_width", type=int, default=50)
        pars.add_argument("--shelf_depth", type=int, default=80)
        pars.add_argument("--name", type=str, default="1A")
        pars.add_argument("--layout_and_side", type=str, default="D-L")
        pars.add_argument("--start", type=int, default=1)
        pars.add_argument("--diff", type=int, default=1)
        pars.add_argument("--object_type", type=str, default="WALL")
        pars.add_argument("--obj_width", type=float, default=10)
        pars.add_argument("--obj_height", type=float, default=10)

    def generate(self):
        if self.options.tab == "tab_special":
            return generate_special_object(self.options, self.svg)
        return generate_shelf(self.options, self.svg)


if __name__ == '__main__':
    WarehouseShelfDesigner().run()
