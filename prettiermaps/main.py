from prettiermaps import geo
from prettiermaps import plotting


def main():
    address = "Praça Ferreira do Amaral, Macau"
    radius = 1100

    aoi = geo.get_aoi_from_user_input(address=address, radius=radius)
    df_streets = geo.query_osm_streets(aoi=aoi)
    df_streets = geo.adjust_street_width(df_streets=df_streets)

    plotting.plot(df_streets)
    return df_streets
