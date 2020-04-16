from pyrosm.data_manager import get_osm_data
from pyrosm.frames import prepare_geodataframe
import geopandas as gpd
import warnings


def get_landuse_data(nodes, node_coordinates, way_records, relations, tags_as_columns, custom_filter):
    # If custom_filter has not been defined, initialize with default
    if custom_filter is None:
        custom_filter = {"landuse": True}
    else:
        # Check that the custom filter is in correct format
        if not isinstance(custom_filter, dict):
            raise ValueError(f"'custom_filter' should be a Python dictionary. "
                             f"Got {custom_filter} with type {type(custom_filter)}.")

        # Ensure that the "landuse" tag exists
        if "landuse" not in custom_filter.keys():
            custom_filter["landuse"] = True

    # Call signature for fetching buildings
    nodes, ways, relation_ways, relations = get_osm_data(node_arrays=nodes,
                                                         way_records=way_records,
                                                         relations=relations,
                                                         tags_as_columns=tags_as_columns,
                                                         data_filter=custom_filter,
                                                         filter_type="keep",
                                                         osm_keys=None
                                                         )

    # If there weren't any data, return empty GeoDataFrame
    if nodes is None and ways is None and relations is None:
        warnings.warn("Could not find any landuse elements for given area.",
                      UserWarning,
                      stacklevel=2)
        return gpd.GeoDataFrame()

    # Prepare GeoDataFrame
    gdf = prepare_geodataframe(nodes, node_coordinates, ways,
                               relations, relation_ways, tags_as_columns)
    return gdf