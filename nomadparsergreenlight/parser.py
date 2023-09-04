import os
import numpy as np
from nomad.metainfo import MSection, Quantity
from nomad.parsing.parser import MatchingParser
from nomad.datamodel import EntryArchive
# from nomad.datamodel.metainfo.annotations import ELNAnnotation, ELNComponentEnum

# import custom library
from echem_data import electrochem_data as ed

# m_package = Package(name='greenlight')

class Greenlight(MSection):
    test_name = Quantity(type=str)
            #                         a_eln=ELNAnnotation(component=ELNComponentEnum.StringEditQuantity))

    cell_voltage = Quantity(type=np.float64, shape=['*'])

    current_density = Quantity(type=np.float64, shape=['*'])


class GreenlightParser(MatchingParser):
    def __init__(self):
        print('initalize GreenlightParser')
        super().__init__(
            name='parsers/greenlight',
            mainfile_mime_re=r'application/csv',
            code_name='greenlight', code_homepage='https://github.com/zbt-tools/ElectrochemDataProcessing',
            mainfile_contents_re=(r'https://github.com/zbt-tools/ElectrochemDataProcessing/TestData/Greenlight')
        )

    def parse(self, mainfile, archive: EntryArchive, logger):
        print('parse Greenlight data file')
        data_file_object = ed.EChemDataFile(mainfile, 'Greenlight')

        archive.metadata.entry_name = os.path.basename(mainfile)
        # archive.metadata.external_id = data[0][1:]
        archive.data = Greenlight()
        print(data_file_object.data.columns)
        archive.data.test_name = data_file_object.header['Test Name']
        archive.data.cell_voltage = data_file_object.data['cell_voltage_total']
        archive.data.current_density = data_file_object.data['current_density']

