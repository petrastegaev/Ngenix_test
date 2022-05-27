import asyncio
import os
import random
import uuid
from zipfile import ZipFile


class XMLBuilder:
    """Builds specified xml"""

    def generate_xml(self):
        level_value = random.randrange(1, 101)
        xml_objects = self._generate_xml_object()
        uniq_value = generate_random_string()
        xml = """<root><var name='id' value='{uniq_value}'/><var name='level' value='{level_value}'/><objects>{xml_objects}</objects></root>""".format(
            uniq_value=uniq_value,
            level_value=level_value,
            xml_objects=xml_objects)
        return xml, uniq_value

    @staticmethod
    def _generate_xml_object():
        """Generating XML objects from 1 to 10"""
        xml_objects = ''
        while random.randrange(0, 10):
            object_name = generate_random_string()
            xml_object = """<object name='{object_name}'/>""".format(object_name=object_name)
            xml_objects = xml_objects + xml_object
        return xml_objects


class ArchiveBuilder:
    """Building Archive"""

    def __init__(self):
        self._archives_num: int = os.getenv("ARCHIVES_NUM", 50)
        self._xml_num: int = os.getenv("XML_NUM", 100)
        self._uniq_set = set()

    async def _generate_archive(self, zip_name):
        with ZipFile(zip_name, 'w') as myzip:
            for i in range(self._xml_num):
                xml_build = XMLBuilder()
                xml, uniq_value = xml_build.generate_xml()
                while uniq_value in self._uniq_set:
                    xml, uniq_value = xml_build.generate_xml()
                self._uniq_set.add(uniq_value)
                filename = 'xml{}.xml'.format(i)
                myzip.writestr(filename, xml)

    async def generate_archives(self):
        zip_name: str = os.getenv("ZIP_DIR", '/tmp/') + 'archive{}.zip'
        return await asyncio.gather(*[self._generate_archive(zip_name.format(i)) for i in range(self._archives_num)])


def generate_random_string() -> str:  # Using uuid for now
    r_string = uuid.uuid4()
    return r_string
