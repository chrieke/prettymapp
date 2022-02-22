LC_SETTINGS = {
    "urban": {"building": True, "landuse": ["construction", "commercial"]},
    "water": {"natural": ["water", "bay"]},
    "woodland": {"landuse": ["forest"]},
    "grassland": {
        "landuse": ["grass", "vineyard"],
        "natural": ["island", "wood"],
        "leisure": ["park"],
    },
    "streets": {
        "highway": [
            "motorway",
            "trunk",
            "primary",
            "secondary",
            "tertiary",
            "residential",
            "service",
            "unclassified",
            "pedestrian",
            "footway",
        ]
    },
    "parking": {"amenity": ["parking"], "man_made": ["pier"]},
}

# Macau
DRAW_SETTINGS_1 = {
    "urban": {
        "cmap": ["#FFC857", "#E9724C", "#C5283D"],
        "ec": "#2F3737",
        "lw": 0.5,
        "zorder": 4,
    },
    "water": {
        "fc": "#a1e3ff",
        "ec": "#85c9e6",
        "hatch": "ooo...",
        "lw": 1,
        "zorder": 2,
    },
    "grassland": {"fc": "#D0F1BF", "ec": "#2F3737", "lw": 1, "zorder": 1},
    "woodland": {"fc": "#64B96A", "ec": "#2F3737", "lw": 1, "zorder": 1},
    "streets": {"fc": "#2F3737", "ec": "#475657", "alpha": 1, "lw": 0, "zorder": 3},
    "parking": {"fc": "#F2F4CB", "ec": "#2F3737", "lw": 1, "zorder": 3},
}

# spain
DRAW_SETTINGS_2 = {
    "urban": {
        "cmap": ["#433633", "#FF5E5B"],
        "ec": "#dadbc1",
        "lw": 0.5,
        "zorder": -1,
    },
    "water": {
        "fc": "#a8e1e6",
        "ec": "#2F3737",
        "hatch": "ooo...",
        "lw": 1,
        "zorder": 3,
    },
    "grassland": {"fc": "#8BB174", "ec": "#2F3737", "lw": 1, "zorder": 1},
    "woodland": {"fc": "#8BB174", "ec": "#2F3737", "lw": 1, "zorder": 1},
    "streets": {"fc": "#2F3737", "ec": "#475657", "alpha": 1, "lw": 0, "zorder": 4},
    "parking": {"fc": "#F2F4CB", "ec": "#2F3737", "lw": 1, "zorder": 3},
}
