from xml_data_generator.xml_archive_builder import XMLBuilder, generate_random_string


class TestXMLBuilder:
    def test_xml(self):
        r_str = generate_random_string()
        xml_build = XMLBuilder(r_str)
        xml = xml_build.generate_xml()
        print(xml)
        assert xml
