# configuration variables

# SO + EA mappings from fileID
keys = ["eaname", "soname", "sotel"]
ENERCHECK = ["Enercheck Solutions", "866-990-2499"]
MAPENERGY = ["Map Energy", "855-397-9116"]
DOMTOR = ["DOMTOR Energy Services", "902-317-6984"]
SOEA = {"1E33": dict(zip(keys, ["Martha Barrett"] + ENERCHECK)),
        "1E43": dict(zip(keys, ["Kamaakshi Baabu"] + ENERCHECK)),
        "1E44": dict(zip(keys, ["Ian Hearns"] + ENERCHECK)),
        "1E46": dict(zip(keys, ["Bahram Farrokhzad"] + ENERCHECK)),
        "7P36": dict(zip(keys, ["Ralph Doncaster"] + MAPENERGY)),
        "9Z09": dict(zip(keys, ["Ralph Doncaster"] + DOMTOR)),
       }

DFLT_SOEA = dict(zip(keys, ["Ralph Doncaster", "Solar Si", "902-555-1212"]))

