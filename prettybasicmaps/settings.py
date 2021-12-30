LC_SETTINGS = {
    "urban": {"building": True, "landuse": ["construction"]},
    "water": {"natural": ["water", "bay"]},
    "woodland": {"landuse": ["forest"]},
    "grassland": {
        "landuse": ["grass"],
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

DRAW_SETTINGS = {
    "urban": {
        "cmap": ["#FFC857", "#E9724C", "#C5283D"],
        "ec": "#2F3737",
        "lw": 0.5,
        "zorder": 4,
    },
    "water": {
        "fc": "#a1e3ff",
        "ec": "#2F3737",
        "hatch": "ooo...",
        "lw": 1,
        "zorder": 2,
    },
    "grassland": {"fc": "#D0F1BF", "ec": "#2F3737", "lw": 1, "zorder": 1},
    "woodland": {"fc": "#64B96A", "ec": "#2F3737", "lw": 1, "zorder": 1},
    "streets": {"fc": "#2F3737", "ec": "#475657", "alpha": 1, "lw": 0, "zorder": 3},
    "parking": {"fc": "#F2F4CB", "ec": "#2F3737", "lw": 1, "zorder": 3},
}
