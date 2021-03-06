#!/usr/bin/env python
# SPDX-FileCopyrightText: (c) 2020 Western Digital Corporation or its affiliates,
#                             Arseniy Aharonov <arseniy@aharonov.icu>
#
# SPDX-License-Identifier: MIT

import os
import re

import stat_attributes as attributes
from services import toPosixPath, readTextFileAtOnce, listMakefiles, Configuration, SingletonMeta, meta_class
from stat_makefile import StatMakefile


def calculateConfigurationVersion():
    value = str(os.stat(attributes.CONFIG_FILENAME).st_mtime) if os.path.isfile(attributes.CONFIG_FILENAME) else None
    return value


class StatConfiguration(meta_class(SingletonMeta, Configuration)):
    def __init__(self):
        super(StatConfiguration, self).__init__()
        self.update(TOOL_VERSION=attributes.VERSION,
                    OUTPUT_DIR=attributes.OUTPUT_DIRECTORY,
                    STAT_ROOT=toPosixPath(os.path.relpath(attributes.TOOL_PATH)),
                    DUMMIES_DIR=attributes.DUMMIES_DIRECTORY)
        self.__products = [item[:-4] for item in listMakefiles(attributes.PRODUCT_DIRECTORY)]
        self.__autoGenerated = {}
        self.__readUserConfiguration()
        self.__readAutoGenerated()

    def __readUserConfiguration(self):
        if os.path.isfile(attributes.CONFIG_FILENAME):
            self.update(StatMakefile(attributes.CONFIG_FILENAME))

    def __readAutoGenerated(self):
        if os.path.isfile(attributes.AUTO_GENERATED_MAKEFILE):
            text = readTextFileAtOnce(attributes.AUTO_GENERATED_MAKEFILE)
            self.__autoGenerated.update(re.findall(r'\s*(\w+)\s*=\s*(.+)\s*', text))

    @property
    def products(self):
        return self.__products

    @property
    def defaultProduct(self):
        product = self.__autoGenerated.get('PRODUCT_FLAVOR', None)
        return product if product in self.products else None

    def isStale(self):
        return self.defaultProduct is None \
               or self.__autoGenerated.get('TOOL_VERSION', None) != attributes.VERSION \
               or self.__autoGenerated.get('CONFIG_VERSION', None) != calculateConfigurationVersion()


class StatConfigurationException(Exception):
    """
    Custom exception for STAT services
    """
    RESOURCE_NOT_FOUND = "No resource by filename '{0}' was found."


if __name__ == '__main__':
    pass
