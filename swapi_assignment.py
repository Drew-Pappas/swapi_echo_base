import json, requests

ENDPOINT = 'https://swapi.co/api'
PEOPLE_KEYS = (
    'url','name','height','mass','hair_color','skin_color',
    'eye_color','birth_year','gender','homeworld','species'
)
PLANET_KEYS = (
    'url', 'name', 'rotation_period', 'orbital_period','diameter', 
    'climate', 'gravity', 'terrain', 'surface_water', 'population'
)
STARSHIP_KEYS = (
    'url', 'starship_class', 'name', 'model', 'manufacturer', 'length',
    'width', 'max_atmosphering_speed', 'hyperdrive_rating', 'MGLT',
    'crew', 'passengers', 'cargo_capacity', 'consumables', 'armament'
    
)
SPECIES_KEYS = (
    'url','name', 'classification', 'designation',
    'average_height', 'skin_colors', 'hair_colors',
    'eye_colors', 'average_lifespan', 'language'
)
VEHICLE_KEYS = (
    'url', 'vehicle_class', 'name','model',
    'manufacturer', 'length', 'max_atmosphering_speed',
    'crew', 'passengers', 'cargo_capacity', 'consumables',
    'armament'
)
PLANET_HOTH_KEYS = (
    'url', 'name','system_position','natural_satellites','rotation_period',
    'orbital_period','diameter', 'climate', 'gravity', 
    'terrain', 'surface_water', 'population','indigenous_life_forms'
)

def assign_crew(entity, crew):
    '''
    This function assigns crew members from the supplied crew dict
    to the entity dict provided.

    Parameters:
        entity (dict) : The entity dict to which the crew members will be assigned
        crew (dict) : A dict of crewmembers with the structure 'role' : 'name'

    Returns:
        dict: An updated dictionary with the crewmembers given
    '''
    for role, person in crew.items():
        entity[role] = person
    return entity

def clean_data(entity):
    '''
    Converts dictionary string values into their appropriate non-string
    types. Strings can go to float, int, dict, and list, and None as needed

    Parameters:
        entity (dict): a dictionary of values that need to be cleaned

    Returns:
        dict: a new dictionary of converted data
    '''
    dict_props = ('homeworld','species')
    int_props = ('max_atmosphering_speed', 'MGLT', 'crew',
                'passengers', 'cargo_capacity', 'height','mass',
                'rotation_period','orbital_period','diameter',
                'surface_water','population','average_height',
                'average_lifespan')
    list_props = ('hair_color', 'skin_color','climate','terrain',
                    'skin_colors', 'hair_colors', 'eye_colors')
    float_props = ('gravity','length','width','hyperdrive_rating')
    cleaned = {}

    for key, value in entity.items():
        if is_unknown(str(value)):
            cleaned[key] = None

        elif key in int_props:
            cleaned[key] = convert_string_to_int(value)

        elif key in list_props:
            cleaned[key] = convert_string_to_list(value)

        elif key in float_props:
            if key == 'gravity':
                cleaned[key] = convert_string_to_float(value.replace(' standard',''))
            else:
                cleaned[key] = convert_string_to_float(value)

        elif key in dict_props:
            if key == 'species':
                new_dict = filter_data(get_swapi_resource(value[0]), SPECIES_KEYS) #TODO
                cleaned[key] = [clean_data(new_dict)]
            elif key == 'homeworld':
                new_dict = filter_data(get_swapi_resource(value), PLANET_KEYS) #TODO
                cleaned[key] = clean_data(new_dict)  

        else:
            cleaned[key] = value

    return cleaned

def combine_data(default_data, override_data):
    '''
    Takes two dictionaries and overrides the value of one dictionary onto
    any matching keys in the first dictionary

    Parameters:
        default_data (dict): a dict of data to be overridden
        override_data (dict): a dict whose keys will override the default_data
                              keys

    Returns:
        dict: an updated dictionary with merged override keys
    '''
    for key,value in override_data.items():
        default_data[key] = value
    return default_data

def convert_string_to_float(value):
    '''
    Converts a string value to a float value. Handles an exception if the
    value cannot be converted.

    Parameters:
        value (str): the value to be converted to a float

    Returns:
        float: the value converted to a float unless excepted
    '''
    try:
        return float(value)
    except ValueError:
        return value

def convert_string_to_int(value):
    '''
    Converts a string value to an int value. Handles an exception if the
    value cannot be converted.

    Parameters:
        value (str): the value to be converted to an int

    Returns:
        int: the value converted to an int unless excepted
    '''
    try:
        return int(value)
    except ValueError:
        return value

def convert_string_to_list(value, delimiter=','):
    '''
    Converts a string value to a list while stripping all whitespace
    from each individual string.

    Parameters:
        value (str): the value to be converted to a float
        delimiter (str): a value used to split the string


    Returns:
        list: the value converted to a list unless excepted
    '''    
    return [word.strip() for word in value.split(',')]

def filter_data(data, filter_keys):
    '''
    Applies a filter to a set of data and sorts the data
    in the order of the keys given to the function.

    Parameters:
        data (dict): The data to be filtered down
        filter_keys (tuple): A collection of keys to filter the data


    Returns:
        dict: A smaller dictionary ordered by the provided tuple
    '''
    filtered_data = dict()

    for key in filter_keys:
        if key in data.keys():
            filtered_data[key] = data[key]
    return filtered_data

def get_swapi_resource(url, params=None):
    '''
    Accesses an API resource and sends back a de-serialized JSON representation
    of the resource

    Parameters:
        url (str): a URL resource to be located
        params (dict): a dictionary of values that can be used for
                       searching the API

    Returns:
        dict: a JSON structured dictionary of the resource found
    '''
    return requests.get(url,params).json()

def is_unknown(value):
    '''
    TODO Docstring
    Applies a case and whitespace insensitive truth value test to check for
    unknown or n/a strings

    Parameters:
        value (str): the value to be checked

    Returns:
        bool: a True or False value dependent on the evaluation of the check

    '''
    if (value.lower().strip() == 'unknown' or value.lower().strip() == 'n/a'):
        return True

def read_json(filepath):
    '''
    Given a valid filepath reads a JSON document and returns a dictionary.

    Parameters:
        filepath (str): path to file.

    Returns:
        dict: dictionary representations of the decoded JSON document.
    
    '''

    with open(filepath,'r', encoding = "utf-8") as file_obj:
        return json.load(file_obj)

def write_json(filepath, data):
    '''
    Writes a dictionary to a JSON file.

    Parameters:
        filepath (str): the path to the file.
        data (dict): the data to be encoded as JSON and written to the file.

    Returns:
        None
    '''
    with open(filepath, 'w', encoding = "utf-8") as file_obj:
        json.dump(data, file_obj, indent = 2, ensure_ascii = False)

def main():
    '''
    Entry point. This program will interact with local file assets and the Star Wars
    API to create two data files required by Rebel Alliance Intelligence.

    - A JSON file comprising a list of likely uninhabited planets where a new rebel base could be
      situated if Imperial forces discover the location of Echo Base.

    - A JSON file of Echo Base information including an evacuation plan of base personnel
      along with passenger assignments for Princess Leia, the communications droid C-3PO aboard
      the transport Bright Hope escorted by two X-wing starfighters piloted by Luke Skywalker
      (with astromech droid R2-D2) and Wedge Antilles (with astromech droid R5-D4).

    Parameters:
        None

    Returns:
        None
    '''
    uninhabited_planets = []

    planet_json = read_json('swapi_planets-v1p0.json')
    
    for planet in planet_json:
        if is_unknown(planet['population']):
            uninhabited_planets.append(
                clean_data((filter_data(planet, PLANET_KEYS)))
                )
    write_json('swapi_planets_uninhabited-v1p1.json',uninhabited_planets)

    echo_base = read_json('swapi_echo_base-v1p0.json')
    swapi_hoth = get_swapi_resource(f"{ENDPOINT}/planets/4/")
    
    echo_base_hoth = echo_base['location']['planet']
    hoth = combine_data(echo_base_hoth, swapi_hoth)
    hoth = filter_data(hoth, PLANET_HOTH_KEYS)
    hoth = clean_data(hoth)
    echo_base['location']['planet'] = hoth

    echo_base_commander = echo_base['garrison']['commander']
    echo_base_commander = clean_data(echo_base_commander)
    echo_base['garrison']['commander'] = echo_base_commander
    
    echo_base_pilot = echo_base['visiting_starships']['freighters'][1]['pilot']
    echo_base_pilot = clean_data(echo_base_pilot)
    echo_base['visiting_starships']['freighters'][1]['pilot'] = echo_base_pilot

    swapi_vehicles_url = f"{ENDPOINT}/vehicles/"
    swapi_snowspeeder = get_swapi_resource(swapi_vehicles_url, {'search': 'snowspeeder'})['results'][0]

    echo_base_snowspeeder = echo_base['vehicle_assets']['snowspeeders'][0]['type']

    snowspeeder = combine_data(echo_base_snowspeeder, swapi_snowspeeder)
    snowspeeder = filter_data(snowspeeder, VEHICLE_KEYS)
    snowspeeder = clean_data(snowspeeder)
    echo_base['vehicle_assets']['snowspeeders'][0]['type'] = snowspeeder

    swapi_starships_url = f"{ENDPOINT}/starships/"
    swapi_t_65 = get_swapi_resource(swapi_starships_url, {'search': 'T-65 X-wing'})['results'][0]

    echo_base_t_65 = echo_base['starship_assets']['starfighters'][0]['type']

    t_65_x_wing = combine_data(echo_base_t_65, swapi_t_65)
    t_65_x_wing = filter_data(t_65_x_wing, STARSHIP_KEYS)
    t_65_x_wing = clean_data(t_65_x_wing)
    echo_base['starship_assets']['starfighters'][0]['type'] = t_65_x_wing

    swapi_millennium_falcon = get_swapi_resource(swapi_starships_url, {'search': 'Millennium Falcon'})['results'][0]

    echo_base_millennium_falcon = echo_base['visiting_starships']['freighters'][0]

    millennium_falcon = combine_data(echo_base_millennium_falcon, swapi_millennium_falcon)
    millennium_falcon = filter_data(millennium_falcon, STARSHIP_KEYS)
    millennium_falcon = clean_data(millennium_falcon)
    echo_base['visiting_starships']['freighters'][0] = millennium_falcon

    swapi_gr_75 = get_swapi_resource(swapi_starships_url, {'search': 'GR-75 medium transport'})['results'][0]


    echo_base_gr_75 = echo_base['starship_assets']['transports'][0]['type']

    gr_75 = combine_data(echo_base_gr_75, swapi_gr_75)
    gr_75 = filter_data(gr_75, STARSHIP_KEYS)
    gr_75 = clean_data(gr_75)
    echo_base['starship_assets']['transports'][0]['type'] = gr_75

    swapi_people_url = f"{ENDPOINT}/people/"
    han = get_swapi_resource(swapi_people_url, {'search': 'han solo'})['results'][0]
    han = filter_data(han, PEOPLE_KEYS)
    han = clean_data(han)

    swapi_people_url = f"{ENDPOINT}/people/"
    chewbacca = get_swapi_resource(swapi_people_url, {'search': 'chewbacca'})['results'][0]
    chewbacca = filter_data(chewbacca, PEOPLE_KEYS)
    chewbacca = clean_data(chewbacca)

    millennium_falcon = assign_crew(millennium_falcon, {'pilot': han, 'copilot': chewbacca})
    echo_base['visiting_starships']['freighters'][0] = millennium_falcon

    evac_plan = echo_base['evacuation_plan']
    
    num_personnel = 0
    for key, value in echo_base['garrison']['personnel'].items():
        num_personnel += value
    evac_plan['max_base_personnel'] = num_personnel

    evac_plan['max_available_transports'] = echo_base['starship_assets']['transports'][0]['num_available']

    evac_plan['max_passenger_overload_capacity'] = evac_plan['max_available_transports'] * echo_base['starship_assets']['transports'][0]['type']['passengers'] * evac_plan['passenger_overload_multiplier']
    
    evac_transport = echo_base['starship_assets']['transports'][0]['type'].copy()
    evac_transport['name'] = "Bright Hope"
    evac_transport['passenger_manifest'] = []

    princess_leia = get_swapi_resource(swapi_people_url, {'search': 'Leia'})['results'][0]
    princess_leia = filter_data(princess_leia, PEOPLE_KEYS)
    princess_leia = clean_data(princess_leia)
    evac_transport['passenger_manifest'].append(princess_leia)

    c3po = get_swapi_resource(swapi_people_url, {'search': 'C-3PO'})['results'][0]
    c3po = filter_data(c3po, PEOPLE_KEYS)
    c3po = clean_data(c3po)
    evac_transport['passenger_manifest'].append(c3po)

    evac_transport['escorts'] = []
    luke_x_wing = echo_base['starship_assets']['starfighters'][0]['type'].copy()
    wedge_x_wing = echo_base['starship_assets']['starfighters'][0]['type'].copy()

    luke_skywalker = get_swapi_resource(swapi_people_url, {'search': 'Luke Skywalker'})['results'][0]
    luke_skywalker = filter_data(luke_skywalker, PEOPLE_KEYS)
    luke_skywalker = clean_data(luke_skywalker)

    r2d2 = get_swapi_resource(swapi_people_url, {'search': 'R2-D2'})['results'][0]
    r2d2 = filter_data(r2d2, PEOPLE_KEYS)
    r2d2 = clean_data(r2d2)

    luke_x_wing = assign_crew(luke_x_wing, {'pilot': luke_skywalker, 'astromech_droid': r2d2})
    evac_transport['escorts'].append(luke_x_wing)

    wedge_antilles = get_swapi_resource(swapi_people_url, {'search': 'Wedge Antilles'})['results'][0]
    wedge_antilles = filter_data(wedge_antilles, PEOPLE_KEYS)
    wedge_antilles = clean_data(wedge_antilles)

    r5d4 = get_swapi_resource(swapi_people_url, {'search': 'R5-D4'})['results'][0]
    r5d4 = filter_data(r5d4, PEOPLE_KEYS)
    r5d4 = clean_data(r5d4)
    
    wedge_x_wing = assign_crew(wedge_x_wing, {'pilot': wedge_antilles, 'astromech_droid': r5d4})
    evac_transport['escorts'].append(wedge_x_wing)

    evac_plan['transport_assignments'] = [evac_transport]
    echo_base['evacuation_plan'] = evac_plan

    write_json('swapi_echo_base-v1p1.json',echo_base)


if __name__ == '__main__':
    main()
