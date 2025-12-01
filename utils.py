def get_stars(star_str):
    stars = 0
    if star_str.lower() == "one":
        stars = 1
    elif star_str.lower() == "two":
        stars = 2
    elif star_str.lower() == "three":
        stars = 3
    elif star_str.lower() == "four":
        stars = 4
    elif star_str.lower() == "five":
        stars = 5
    return stars