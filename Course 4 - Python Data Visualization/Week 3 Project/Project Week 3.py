"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal


# Function from Project from Week 2
def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    row_dict = dict()
    with open(filename, mode='r', newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            row_dict[row[keyfield]] = row
    return row_dict


def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
                       
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    output_dict = dict()
    cc_np = set()
    pc_set = set(item_tuple[1] for item_tuple in plot_countries.items())
    gdpc_set = set(c_name_k for c_name_k in gdp_countries.keys())
    c_intersection = pc_set & gdpc_set
    pc_rev = {item_tuple[1]:item_tuple[0] for item_tuple in plot_countries.items()}
    for c_name in c_intersection:
        output_dict[pc_rev[c_name]] = c_name
    for c_name in pc_set:
        if c_name not in c_intersection:
            cc_np.add(pc_rev[c_name])
    return (output_dict,cc_np)


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    op_dict = dict()
    set1 = set()
    set2 = set()
    nested_dict = read_csv_as_nested_dict(gdpinfo['gdpfile'],
                                          gdpinfo['country_name'],
                                          gdpinfo['separator'],
                                          gdpinfo['quote'])
    format_dict, format_set = reconcile_countries_by_name(plot_countries, nested_dict)
    for country_code in format_dict:
        if nested_dict[format_dict[country_code]][year] == '':
            set2.add(country_code)
        else:
            op_dict[country_code] = math.log10(float(nested_dict[format_dict[country_code]][year]))
    set1 = format_set
    return (op_dict,set1,set2)


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    world_map = pygal.maps.world.World()
    plot_dict, plot_set1, plot_set2 = build_map_dict_by_name(gdpinfo, plot_countries, year)
    world_map.title = 'GDP by country for '+str(year)+' (log scale), unified by common country NAME'
    world_map.add('GDP for '+str(year),plot_dict)
    world_map.add('Missing from World Bank Data',plot_set1)
    world_map.add('No GDP data',plot_set2)
    world_map.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

# test_render_world_map()
