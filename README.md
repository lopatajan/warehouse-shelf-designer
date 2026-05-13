# Warehouse Shelf Designer — Inkscape Extension

An [Inkscape](https://inkscape.org/) extension for drawing warehouse floor plans with labeled shelf positions. The generated SVG files can be consumed by downstream tools to extract shelf topology and compute picking sequences.

## Requirements

- Inkscape 1.x
- Python 3 (bundled with Inkscape)

## Installation

Copy `Shelf.py` and `Shelf.inx` into your Inkscape extensions directory:

| Platform | Path |
|----------|------|
| Linux    | `~/.config/inkscape/extensions/` |
| macOS    | `~/Library/Application Support/org.inkscape.Inkscape/config/inkscape/extensions/` |
| Windows  | `%APPDATA%\inkscape\extensions\` |

Restart Inkscape. The extension appears under **Extensions → Warehouse Designer → Warehouse Shelf Designer**.

## Usage

### Tab: Shelf

Generates a row or column of shelf positions, each rendered as a labeled rectangle.

| Parameter | Description                                                                          |
|-----------|--------------------------------------------------------------------------------------|
| **Shelf count** | Number of shelf positions to generate                                                |
| **Facing width** | Width of the shelf face (the side visible from the aisle), in cm                     |
| **Shelf depth** | Depth of the shelf (perpendicular to the aisle), in cm                               |
| **Name** | Base name for the shelf series, e.g. `1A`                                          |
| **Layout and facing side** | Combined setting: which direction shelves are placed, and which side faces the aisle |
| **Start number** | Number assigned to the first shelf position                                          |
| **Step** | Increment between consecutive shelf numbers                                          |

#### Example

With default settings (Name `1A`, count 5, start 1, step 1, top to bottom, facing Left) the extension generates a vertical column of 5 rectangles with these `inkscape:label` values:

```
1A-1-L
1A-2-L
1A-3-L
1A-4-L
1A-5-L
```

A small line on the left edge of each rectangle marks the facing side. The group containing all five is labeled `Shelf:1A-1+1x5`.

To generate the opposite side of the same rack (right aisle), run again with facing Right and a different name, e.g. `1B` → produces `1B-1-R` … `1B-5-R`.

#### Layout and facing side

The facing side determines from which direction a picker approaches each shelf. It must be perpendicular to the layout direction:

- Horizontal layout (left↔right) → facing side is Up or Down
- Vertical layout (top↔bottom) → facing side is Left or Right

A small indicator line on each shelf rectangle marks the facing side.

#### Shelf label format

Each generated shelf position is labeled as `{Name}-{Number}-{Side}`, e.g. `1A-23-L`. The label is stored as the `inkscape:label` attribute on the SVG group element and is used by the parser to identify shelf positions.

### Tab: Special Object

Inserts a single labeled rectangle used to mark structural elements of the warehouse floor plan.

| Type | Color | Meaning |
|------|-------|---------|
| `WALL` | Blue | Physical wall or obstacle — impassable |
| `START` | Green | Entry point for the picker |
| `END` | Red | Exit point or handoff location |

Special objects are placed at the center of the current viewport. Resize and reposition them freely after insertion; the parser identifies them by their `inkscape:label`, not by size or position.

## SVG label conventions

The parser reads `inkscape:label` attributes on `<rect>` elements to understand the floor plan:

| Label pattern | Meaning |
|---------------|---------|
| `{Name}-{Number}-{Side}` | Shelf position (e.g. `1A-23-L`) |
| `WALL` | Impassable obstacle |
| `START` | Picker entry point |
| `END` | Picker exit / handoff point |

Any rectangle without a recognized label is ignored by the parser, so decorative elements (labels, notes, door markings, etc.) can be added freely.

## Contributing

Bug reports and pull requests are welcome. When modifying the extension, note that:

- `Shelf.inx` defines the UI (parameters, labels, layout)
- `Shelf.py` contains all generation logic
- Both files must be kept in sync — every `<param name="x">` in the INX needs a corresponding `pars.add_argument("--x", ...)` in the Python
