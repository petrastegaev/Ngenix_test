import asyncio
from xml_archive_builder import ArchiveBuilder

def main():
    ab = ArchiveBuilder()
    ab.generate_archives()

if __name__ == '__main__':
    main()