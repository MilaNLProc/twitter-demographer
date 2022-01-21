import datetime
import os.path
import zipfile
from dataclasses import dataclass
from os.path import expanduser
from typing import List, Union

import requests
from tqdm import tqdm


@dataclass
class GeoNamesEntity:
    geoId: int
    name: str
    ascii_name: str
    alter_name: Union[str, List[str]]
    lat: float
    lon: float
    f_class: str
    f_code: str
    country: str
    cc: Union[str, List[str]]
    admin1: str
    admin2: str
    admin3: str
    admin4: str
    population: int
    elevation: int
    g_topo: int
    timezone: str
    mod_date: str

    def __post_init__(self):
        self.alter_name = [s.strip() for s in self.alter_name.split(",")] if self.alter_name else []
        self.cc = [s.strip() for s in self.cc.split(",")] if self.cc else []

        self.lat = float(self.lat) if self.lat else .0
        self.lon = float(self.lon) if self.lon else .0
        self.population = int(self.population) if self.population else 0
        self.elevation = int(self.elevation) if self.elevation else 0

        self.mod_date = datetime.datetime.fromisoformat(self.mod_date) if self.mod_date else ''


class GeoNamesProvider:

    def _download_dump(self):
        """
        https://github.com/sirbowen78/lab/blob/master/file_handling/dl_file1.py
        """
        resource_url = 'https://download.geonames.org/export/dump/allCountries.zip'  # todo env var
        print(f'{self._geonames_dump_zip} not found. Downloading it from {resource_url} ...')

        filesize = int(requests.head(resource_url).headers["Content-Length"])
        chunk_size = 1024

        with requests.get(resource_url, stream=True) as r, open(self._geonames_dump_zip, "wb") as f, tqdm(
                unit="B",  # unit string to be displayed.
                unit_scale=True,  # let tqdm to determine the scale in kilo, mega..etc.
                unit_divisor=chunk_size,  # is used when unit_scale is true
                total=filesize,  # the total iteration.
                # file=sys.stdout,  # default goes to stderr, this is the display on console.
                desc=self._geonames_dump_zip  # prefix to be displayed on progress bar.
        ) as progress:
            for chunk in r.iter_content(chunk_size=chunk_size):
                datasize = f.write(chunk)
                progress.update(datasize)

        # wget.download(resource_url, self._geonames_dump)

        print('Unzipping ...')
        with zipfile.ZipFile(self._geonames_dump_zip, "r") as zip_ref:
            zip_ref.extractall(self._working_dir)

    def __init__(self):
        self._working_dir = os.path.join(expanduser("~"), '.twitter-demographer', 'geolocation',
                                         'geonames')  # todo env var
        self._index_file = os.path.join(self._working_dir, 'geonames_trigrams.index')  # todo env var
        self._geonames_dump_zip = os.path.join(self._working_dir, 'geonames_dump.zip')  # todo env var
        self._geonames_dump_txt = os.path.join(self._working_dir, 'allCountries.txt')  # todo env var

        os.makedirs(self._working_dir, exist_ok=True)

        if not os.path.exists(self._index_file):
            if not os.path.exists(self._geonames_dump_zip):
                self._download_dump()

            index = None  # todo init index here

            with open(self._geonames_dump_txt, 'r') as f:
                for line in f:
                    gn = GeoNamesEntity(*line.strip().split('\t'))
                    print(gn)

                # todo add entries to index


if __name__ == '__main__':
    GeoNamesProvider()
