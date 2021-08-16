# VMF to Maphack converter

Creates a [MapHack file](https://developer.valvesoftware.com/wiki/Maphack_Fundamentals) out of a [Valve Map Format file](https://developer.valvesoftware.com/wiki/Valve_Map_Format) which contains all of its entities.

## Requirements
  - `pyparsing`

## Usage
  - `python vmf2mh.py map_file.vmf`
    - Outputs `<map_file>_maphack.txt` to the work folder. It might take a while..
