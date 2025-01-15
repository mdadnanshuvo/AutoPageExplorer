def compare_tile_and_map_data(self, tile_data, map_data):
    """
    Compare data extracted from tile and map sections.

    Args:
        tile_data (dict): Data extracted from the tile.
        map_data (dict): Data extracted from the map.

    Returns:
        dict: A dictionary showing discrepancies or consistency between the data.
    """
    comparison = {}
    for key in tile_data:
        if key in map_data:
            comparison[key] = {
                'tile_value': tile_data[key],
                'map_value': map_data[key],
                'consistent': tile_data[key] == map_data[key]
            }
        else:
            comparison[key] = {
                'tile_value': tile_data[key],
                'map_value': 'Not Found',
                'consistent': False
            }
    return comparison
