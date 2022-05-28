import os
from concurrent.futures import ProcessPoolExecutor as Pool
from xml.etree import ElementTree as ET
from zipfile import ZipFile
import glob
import csv
import multiprocessing


class XMLParser:
    def __init__(self):
        self._archive_list: tuple = self._get_archive_list()
        cpu = multiprocessing.cpu_count()
        _xml_num: int = os.getenv("XML_NUM", 100)
        if cpu <= _xml_num:
            self.outer_loop_proc = 1
            self.inner_loop_proc = cpu - 1
        else:
            self.outer_loop_proc = cpu // _xml_num
            self.inner_loop_proc = cpu - (cpu % _xml_num)

    def process_archives(self):
        lst = self._archive_list
        with Pool(self.outer_loop_proc) as pool:
            futures = pool.map(self._process_archive, lst)
            xml_id_list = []
            xml_object_list = []
            for future in futures:
                xml_id_list_chnk, xml_object_list_chnk = future
                xml_id_list += xml_id_list_chnk
                xml_object_list += xml_object_list_chnk
            self._write_csv('1.csv', xml_id_list, 'level')
            self._write_csv('2.csv', xml_object_list, 'name')

    @staticmethod
    def _write_csv(file, rows, colname):
        head = ['id', colname]
        with open(file, "w") as csvfile:
            write = csv.writer(csvfile)
            write.writerow(head)
            write.writerows(rows)

    def _process_archive(self, archive):
        with ZipFile(archive, 'r') as f:
            filenames = f.namelist()
            with Pool(self.inner_loop_proc) as pool:
                futures = []
                for file in filenames:
                    xml = f.read(file).decode("utf-8")
                    future = pool.submit(self._parse_xml_file, xml)
                    futures.append(future)
                xml_id_list = []
                xml_object_list = []
                try:
                    for future in futures:  # Надо было конечно использовать очередь, но я не успеваю
                        xml_id, level, xml_objects = future.result()
                        xml_id_list.append([xml_id, level])
                        xml_object_list += [[x] + [xml_id] for x in xml_objects]
                except Exception as e:
                    print(e)
            return xml_id_list, xml_object_list

    @staticmethod
    def _parse_xml_file(xml):
        root = ET.fromstring(xml)
        xml_objects = []
        try:
            for elem in root.iter():
                if elem.tag == 'var':
                    if elem.attrib['name'] == 'id':
                        xml_id = elem.attrib['value']
                    elif elem.attrib['name'] == 'level':
                        level = elem.attrib['value']
                elif elem.tag == 'object':
                    xml_object = elem.attrib['name']
                    xml_objects.append(xml_object)
        except Exception as e:
            print(e)
        return xml_id, level, xml_objects

    @staticmethod
    def _get_archive_list():
        zip_dir = os.getenv("ZIP_DIR", '/tmp/')
        pattern = zip_dir + 'archive*'
        filelist = glob.glob(pattern)
        return filelist
