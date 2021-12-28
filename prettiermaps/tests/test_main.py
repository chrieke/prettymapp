# import geopandas as gpd
# import osmnx as ox
# import matplotlib.pyplot as plt
# from descartes import PolygonPatch
#
# from prettiermaps import main


custom_filters = {
    "streets": '["highway"~"motorway|trunk|primary|secondary|tertiary|'
    'residential|service|unclassified|pedestrian|footway"]'
}


# def test_query_osm_data():
#     address = "Praça Ferreira do Amaral, Macau"
#     radius = 1100
#
#     df = query_osm_data(address=address, radius=radius, custom_filters=custom_filters)
#
#     # PLOT
#     fig, ax = plt.subplots(1, 1, figsize=(12, 12))
#     # ax.axis("off")
#     # ax.axis("equal")
#     drawing_kwargs = {"fc": "#2F3737", "ec": "#475657"}
#     geom = df.dissolve().plot(
#         ax=ax, **drawing_kwargs
#     )  # multilinestring #TODO probably multiple mls from gdf
#     plt.show()
#
#     ax.add_patch(PolygonPatch(geom, **drawing_kwargs))
#
#     plt.show()
#
#     assert isinstance(df, gpd.GeoDataFrame)
