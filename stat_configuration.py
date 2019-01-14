import os
import re

import stat_attributes as attributes
from services import Singleton, toPosixPath, readTextFileAtOnce, listMakefiles
from stat_makefile import StatMakefile
from vs_tools import MsvsTools


def calculateConfigurationVersion():
    value = str(os.stat(attributes.CONFIG_FILENAME).st_mtime) if os.path.isfile(attributes.CONFIG_FILENAME) else None
    return value

class StatConfiguration(Singleton):
    def __init__(self):
        self.__toolPath = os.path.dirname(os.path.relpath(__file__))
        self.__configuration = {
            'TOOL_VERSION': attributes.VERSION,
            'OUTPUT_DIR': attributes.OUTPUT_DIRECTORY,
            'TOOL_DIR': toPosixPath(attributes.TOOL_PATH),
            'DUMMIES_DIR': attributes.DUMMIES_DIRECTORY,
        }
        self.__products = [item[:-4] for item in listMakefiles(attributes.PRODUCT_DIRECTORY)]
        self.__autoGenerated = {}
        self.__readUserConfiguration()
        self.__readAutoGenerated()
        self.__msvsTools = MsvsTools.find(self.getInt('MSVS_VERSION', None))

    def __readUserConfiguration(self):
        if os.path.isfile(attributes.CONFIG_FILENAME):
            userConfig = StatMakefile(attributes.CONFIG_FILENAME)
            self.__configuration.update({key: userConfig[key] for key in userConfig})

    def __readAutoGenerated(self):
        if os.path.isfile(attributes.AUTO_GENERATED_MAKEFILE):
            text = readTextFileAtOnce(attributes.AUTO_GENERATED_MAKEFILE)
            self.__autoGenerated.update(re.findall(r'\s*(\w+)\s*=\s*(.+)\s*', text))

    def __getitem__(self, key):
        return self.__configuration.get(key, None)

    def __iter__(self):
        for key in self.__configuration:
            yield key

    @property
    def statPath(self):
        return self.__toolPath

    @property
    def products(self):
        return self.__products

    @property
    def defaultProduct(self):
        product = self.__autoGenerated.get('OUTPUT_NAME', None)
        return product if product in self.products else None

    def getToolchain(self):
        """
        :rtype: StatToolchain
        """
        return self.__msvsTools

    def getMsvsTools(self):
        return self.__msvsTools

    def getInt(self, key, default):
        try:
            return int(self.__configuration.get(key, ''))
        except ValueError:
            return default

    def isStale(self):
        return self.defaultProduct is None \
               or self.__autoGenerated.get('TOOL_VERSION', None) != attributes.VERSION \
               or self.__autoGenerated.get('CONFIG_VERSION', None) != calculateConfigurationVersion()



class StatConfigurationException(Exception):
    """
    Custom exception for STAT services
    """
    RESOURCE_NOT_FOUND = "No resource by filename '{0}' was found."