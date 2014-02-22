#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Parses all the tsv files in riverdata and pushes them to mongodb
"""

import os
import sys
import csv
import glob
import fileinput
import ConfigParser
from pymongo import MongoClient


class RiverLevels(object):

    def __init__(self):
        self.creds = self.read_credentials()
        self.db = self.get_db_handle()

    def parse_tsv(self, datafile, delim='\t'):
        """
        Parse River level tsv data file
        """
        print "Pushing file %s" % datafile
        reader = csv.DictReader(open(datafile), delimiter=delim)

        for doc in reader:
            data = dict()
            for key, val in doc.iteritems():
                if key:
                    data[key] = val
            self.push_data(data)
        print "Done!"

    def push_data(self, data, collection="riverlevels"):
        """
        Push data to mongodb collection
        """
        self.db[collection].insert(data)

    def read_credentials(self, config="mongo.ini", section='mongo'):
        """
        Read credentials from the config file
        """
        # Can we find the config file
        if not os.path.exists(config):
            sys.stderr.write("Could not find %s file!\n" % config)
            sys.exit(1)

        # Get the credentials from the config file
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config)
        try:
            return dict(config_parser.items(section))
        except ConfigParser.NoSectionError:
            sys.stderr.write("Could not find section %s in file %s!\n" % (section, config))
            sys.exit(1)

    def get_db_handle(self):
        """
        Get a handle on the mongo database stored in the mongo.ini
        """
        client = MongoClient(self.creds["host"], int(self.creds["port"]))
        client[self.creds["db"]].authenticate(self.creds["user"],
                                               self.creds["password"])
        return client[self.creds["db"]]

if __name__ == "__main__":

    river_level = RiverLevels()
    datasource = "riverdata"

    if os.path.exists(datasource):
        for datafile in glob.glob(datasource + "/*tsv"):
            river_level.parse_tsv(datafile)
