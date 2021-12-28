from prettiermaps import geo


def main():
    address = "Praça Ferreira do Amaral, Macau"
    radius = 1100

    aoi = geo.get_aoi_from_user_input(address=address, radius=radius)
    df = geo.query_osm_streets(aoi=aoi)

    return df
