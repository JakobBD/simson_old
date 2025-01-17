from os.path import join
from typing import Any
import yaml
import numpy as np
# from src.read_data.load_data import load_region_mapping, load_pop



class Config:
    """
    Class of SIMSON configurations. Contains both general configurations like SSP scenarios
    and product categories to use as well as adaptable parameters like steel price change.
    A common instance of this class ('cfg') is used by most other files, its attributes can be
    adapted with the 'customize' method.
    """

    def __init__(self):
        """
        Creates instance of config class with default parameters. These can :func:`print`
        modified through :py:func:`src.tools.config.Config#customize` method.
        """

        # general config
        self.simulation_name = 'SIMSON_Test_1'
        self.try_reload = {
            'setup': True,
            'dsms': True,
            'historic_stocks': True,
            'gdp': True
        }
        self.include_gdp_and_pop_scenarios_in_prediction = True

        self.do_show_figs = True
        self.do_save_figs = True

        # data sources
        self.data_path = 'data'
        self.data_sources = {
            'pop': 'remind',  # Options: UN, KC-Lutz (only for scenarios)
            'gdp': 'remind',  # Options: IMF, Koch-Leimbach (only for scenarios)
            'production': 'geyer',  # Options: geyer
            'lifetime': 'geyer',  # Options: geyer
            'regions': 'World',  # Options: REMIND, World, REMIND_EU
            'good_and_material_shares': 'geyer',  # Options: geyer
            'mechanical_recycling_rate': 'excel',
            'chemical_recycling_rate': 'excel',
            'solvent_recycling_rate': 'excel',
            'incineration_rate': 'excel',
            'uncontrolled_losses_rate': 'excel',
            'bio_production_rate': 'excel',
            'daccu_production_rate': 'excel',
            'mechanical_recycling_yield': 'excel',
            'reclmech_loss_uncontrolled_rate': 'excel',
            'material_shares_in_goods': 'excel',
            'emission_capture_rate': 'excel',
            'carbon_content_materials': 'excel'
        }

        # model customization
        self.curve_strategy = 'Duerrwaechter'  # Options: Duerrwaechter

        self.do_visualize = {
            'stock_prediction': False,
            'future_production': False,
            'sankey': True
        }

        # indices / scope
        self.aspects = ['Time', 'Element', 'Region', 'Material', 'Good']
        self.index_letters = {'Time': 't',
                              'Element': 'e',
                              'Region': 'r',
                              'Material': 'm',
                              'Good': 'g'}
        self.start_year = 1950
        self.end_year = 2100
        self.last_historic_year = 2015

        self.elements = sorted(['C', 'Other Elements'])
        self.materials = sorted(['PE', 'PP', 'PS', 'PVC', 'PET', 'PUR', 'Other'])
        self.in_use_categories = sorted(['Transportation', 'Packaging', 'Building and Construction', 'Other Uses'])
        self.scenario = 'SSP2'

        self.n_elements = len(self.elements)
        self.n_materials = len(self.materials)
        self.n_use_categories = len(self.in_use_categories)

        # Init attributes
        self.data = SetupDataContainer()

        # TODO: check interaction with self.data and clean up
        self.odym_dimensions = {'Time': 'Time',
                           'Element': 'Element',
                           'Material': 'Material',
                           'Region': 'Region',
                           'Good': 'Material'}

        self.items = None

    def init_items_dict(self):
        """"
        only call after setup
        """
        self.items = {'Time': self.years,
                      'Element': self.elements,
                      'Material': self.materials,
                      'Region': self.data.region_list,
                      'Good': self.in_use_categories}


    def customize(self, config_dict: dict):
        """
        Function to change attributes of config instance. Allows functionality to change
        the config instance all other files are referring to during runtime.

        :param config_dict: A dictionary containing the attribute names as keys and adabted values as values.
        :return:
        """
        name = config_dict['simulation_name']
        for prm_name, prm_value in config_dict.items():
            if prm_name not in self.__dict__:
                raise Exception(f'The custom parameter {prm_name} given in the configuration {name} '
                                'is not registered in the default config definition. '
                                'Maybe you misspelled it or did not add it to the defaults?')
            setattr(self, prm_name, prm_value)
        return self


    def generate_yml(self, filename: str = 'yaml_test.yml'):
        """
        Generates and saves yaml file with current config file settings in
        simulation/interface/yaml folder. Filename is given as parameter,
        if it doesn't have '.yml'/'.yaml' ending, '.yml' is appended.

        :param filename: Name of yaml file, with or without '.yml'/'.yaml' ending.
        :return:
        """
        filename = f'{filename}.yml' if filename[-4:] not in ['.yml', 'yaml'] else filename
        filepath = join('simulation', 'interface', 'yaml', filename)
        with open(filepath, 'w') as f:
            yaml.dump(self.__dict__, f, sort_keys=False)

    @property
    def n_years(self):
        return self.end_year - self.start_year + 1

    @property
    def years(self):
        return np.arange(self.start_year, self.end_year + 1)

    @property
    def historic_years(self):
        return np.arange(self.start_year, self.last_historic_year + 1)

    @property
    def future_years(self):
        return np.arange(self.last_historic_year + 1, self.end_year + 1)

    @property
    def n_historic_years(self):
        return self.last_historic_year - self.start_year + 1

    @property
    def i_historic(self):
        return np.arange(self.n_historic_years)

    @property
    def i_future(self):
        return np.arange(self.n_historic_years, self.n_years)

    @property
    def n_regions(self):
        return self.data.region_list.shape[0]

    def y_id(self, year):
        return int(year) - self.start_year


class SetupDataContainer():

    def __init__(self) -> None:
        self.df_region_mapping = None
        self.region_list = None

        self.df_pop = None
        self.df_pop_countries = None

        self.np_pop = None
        self.np_gdp = None

    def __getattribute__(self, __name: str) -> Any:
        # if not loaded, call setup
        attr = super().__getattribute__(__name)
        if attr is None:
            raise Exception("Setup no yet called, call setup() at start of program")
        else:
            return attr


cfg = Config()


if __name__ == '__main__':
    cfg.generate_yml()
