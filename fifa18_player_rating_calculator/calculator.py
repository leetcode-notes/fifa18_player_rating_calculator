import json
import os

def get_position_blueprint_dict():
    filepath = os.path.join(__file__, 'position_blueprint_dict.json')
    with open(filepath, 'r') as fp:
        return json.load(fp)

def add_reputation(value, international_reputation, subtraction):    
    value = round(value)
    increase = max(international_reputation - subtraction, 1)
    return round(value + increase)

def check_potential(value, potential):
    """Value cannot be higher than potential"""
    return min(value, potential)

def process_raw_rating(rating, international_reputation, rep_subtraction, potential):
    contrib_plus_reputation = add_reputation(rating, international_reputation, rep_subtraction)
    capped_contrib = check_potential(contrib_plus_reputation, potential)
    return capped_contrib

def calculate_ratings(stats_dict):
    root_positions = position_blueprint_dict.keys()
    international_rep = stats_dict['international_reputation']
    potential = stats_dict['potential']
    position_ratings = {}
    for position in root_positions:
        sub_dict = position_blueprint_dict[position]
        coefficient_dict = sub_dict['coefficients']
        rep_subtraction = sub_dict['reputation_subtraction']
        raw_position_rating = sum(coefficient * stats_dict[stat] 
                                  for stat, coefficient in coefficient_dict.items())
        position_ratings[position] = process_raw_rating(raw_position_rating, international_rep, 
                                                        rep_subtraction, potential)
    return position_ratings