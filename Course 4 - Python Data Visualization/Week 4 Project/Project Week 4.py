"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.

https://py3.codeskulptor.org/#user304_IMhVMhWtDY_2.py
"""

import csv
import math
import pygal


def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    cc_dict, pc_dict, wbc_dict = dict(), dict(), dict()
    filename = codeinfo['codefile']
    keyfield_pc = codeinfo['plot_codes']
    keyfield_wbc = codeinfo['data_codes']
    separator = codeinfo['separator']
    quote = codeinfo['quote']
    with open(filename, mode='r', newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile,delimiter=separator,quotechar=quote)
        for row in csv_reader:
            pc_dict[row[keyfield_pc]] = row
            wbc_dict[row[keyfield_wbc]] = row
    for pc_dkey, wbc_dkey in zip(pc_dict.keys(), wbc_dict.keys()):
        cc_dict[pc_dkey] = wbc_dkey
    return cc_dict


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    output_dict = dict()
    output_set = set()
    
    converter_dict = build_country_code_converter(codeinfo)
    # The key and value country codes in converter dict are not in specific case
    # Therefore, make a new dict with lowercased key and values
    lower_converter = dict()
    for key in converter_dict:
        lower_converter[key.lower()] = converter_dict[key].lower()

    # The keys in gdp_countries dictionary are in uppercase
    # But we want all the required country codes in lowercase for comparison
    lower_gdp = dict()
    for key in gdp_countries:
        lower_gdp[key.lower()] = key

    for plot_key in plot_countries:
        for gdp_key in gdp_countries:
            if plot_key.lower() in lower_converter:
                if lower_converter[plot_key.lower()] in lower_gdp:
                    if lower_converter[plot_key.lower()] == gdp_key.lower():
                        output_dict[plot_key] = gdp_key
                elif lower_converter[plot_key.lower()] not in lower_gdp:
                    output_set.add(plot_key)
            else:
                output_set.add(plot_key)
    return (output_dict, output_set)


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    row_dict = dict()
    output_dict = dict()
    set2 = set()
    with open(gdpinfo['gdpfile'],mode='r',newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile,
                                    delimiter = gdpinfo['separator'],
                                    quotechar = gdpinfo['quote'])
        for row in csv_reader:
            row_dict[row[gdpinfo['country_code']]] = dict(row)

    ret_dict, ret_set1 = reconcile_countries_by_code(codeinfo, plot_countries, row_dict)
    for country_code in ret_dict:
        if row_dict[ret_dict[country_code]][year] == '':
            set2.add(country_code)
        else:
            gdp = row_dict[ret_dict[country_code]][year]
            output_dict[country_code] = math.log10(float(gdp))
    return (output_dict, ret_set1, set2)

def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    world_map = pygal.maps.world.World()
    plot_dict, plot_set1, plot_set2 = build_map_dict_by_code(gdpinfo,codeinfo,plot_countries,year)
    world_map.title = 'GDP by country for '+str(year)+' (log scale), unified by common country CODE'
    world_map.add('GDP for '+str(year),plot_dict)
    world_map.add('Missing from World Bank Data',plot_set1)
    world_map.add('No GDP data',plot_set2)
    world_map.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years
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

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()
