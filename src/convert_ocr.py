import sys
from urllib import request
sys.path.append('/home/cloud/python-saxon')
import saxonc
import requests
import re
import os

def transformHOCR(urls, folder, logger):
    print("Transform hOCR")
    with saxonc.PySaxonProcessor(license=False) as proc:
        xsltproc = proc.new_xslt_processor()
        xsltproc.compile_stylesheet(stylesheet_file="/home/cloud/baytsify/xslt/hOCR2ALTO.xsl")

        for u in urls:
            filename = re.sub(r'https://api.digitale-sammlungen.de/ocr/(.+)/(.+)', r'\1_\2.xml', u)
            try:
                r = requests.get(u)
            except:
                logger.error(f"Konnte {u} nicht abrufen")
                pass
            else:
                r.encoding = 'utf-8'
                try:
                    document = proc.parse_xml(xml_text=r.text)
                    xsltproc.set_source(xdm_node=document)
                    result = xsltproc.transform_to_string()
                except:
                    logger.error(f"Konnte {u} nicht transformieren")
                    pass
                else:
                    with open(os.path.join(folder, filename), 'w') as f:
                        f.write(result)
                        print(f"Wrote {filename}")

if __name__ == '__main__':
    urls = ['https://api.digitale-sammlungen.de/ocr/bsb00063967/740', 'https://api.digitale-sammlungen.de/ocr/bsb00063967/739']
    transformHOCR(urls, '/home/cloud/baytsify/OCR')