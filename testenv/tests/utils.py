import os
import os.path
from io import StringIO

from lxml import etree
from OpenSSL import crypto


def validate_xml(xml_string, xsd_path):
    with open(xsd_path) as fh:
        xmlschema_doc = etree.parse(fh)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    # Decode bytes object and preserve strings and unicode(py2).
    if isinstance(xml_string, bytes):
        xml_string = xml_string.decode("utf-8")
    return xmlschema.validate(etree.parse(StringIO(xml_string)))


class FakeRequest:

    def __init__(self, data):
        self.saml_request = data


def generate_certificate(fname, path):
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)
    cert = crypto.X509()
    cert.get_subject().C = 'IT'
    cert.gmtime_adj_notBefore(-50 * 365 * 24 * 60 * 60)
    cert.gmtime_adj_notAfter(50 * 365 * 24 * 60 * 60)
    cert.set_pubkey(key)
    cert.sign(key, str('sha256'))
    open(os.path.join(path, '{}.crt'.format(fname)), "wb").write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open(os.path.join(path, '{}.key'.format(fname)), "wb").write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, key))
