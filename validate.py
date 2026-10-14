from pathlib import Path
import re
from lxml import etree

folder=Path(__file__).resolve().parent
xml_file=folder/'timeTable.xml'
dtd_file=folder/'timetable.dtd'

try:
    document=etree.parse(str(xml_file),etree.XMLParser(load_dtd=True,no_network=True))
    print('XML well-formed: да')
except etree.XMLSyntaxError as error:
    print(f'XML well-formed: нет ({error})')
    raise SystemExit(1)

with dtd_file.open('rb') as stream:
    dtd=etree.DTD(stream)
if not dtd.validate(document):
    print('DTD valid: нет')
    for entry in dtd.error_log:
        print(entry.message)
    raise SystemExit(1)
print('DTD valid: да')

numbers=document.xpath('/timeTable/lessons/lesson/@no')
if not all(re.fullmatch(r'[0-9]+',number) for number in numbers):
    print('Номера занятий: есть нечисловые значения')
    raise SystemExit(1)
print('Номера занятий: все состоят из цифр')
