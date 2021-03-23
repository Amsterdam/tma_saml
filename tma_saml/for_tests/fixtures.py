import logging
from base64 import b64encode
from datetime import datetime, timedelta
from random import randint

from lxml import etree
from signxml import XMLSigner

from tma_saml.for_tests.cert_and_key import server_pem, server_crt
from tma_saml.tma_saml import HR_ATTRIBUTES, HR_BRANCH_KEY, HR_KVK_NUMBER_KEY, DIGI_D_ATTRIBUTES, DIGI_D_UID_KEY

log = logging.getLogger(__name__)

ATTRIBUTE_XML_TEMPLATE = """        <saml:Attribute Name="{}" xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">
            <saml:AttributeValue xmlns:xs="http://www.w3.org/2001/XMLSchema"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">{}</saml:AttributeValue>
        </saml:Attribute>
"""
ASSERTION_XML_TEMPLATE = """<saml:Assertion Version="2.0" ID="{id}" xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">
    <saml:Conditions NotBefore="{not_before}" NotOnOrAfter="{not_on_or_after}"/>
    <saml:AttributeStatement xmlns:saml="urn:oasis:names:tc:SAML:2.0:assertion">
{attributes}    </saml:AttributeStatement>
</saml:Assertion>"""
xml_signer = XMLSigner(signature_algorithm='rsa-sha1', digest_algorithm='sha1')


def _get_attribute_statement(dict_obj):
    attributes = ""
    for k, v in dict_obj.items():
        attributes += (ATTRIBUTE_XML_TEMPLATE.format(k, v))
    return attributes


def _get_assertion(dict_obj, not_before=None, not_on_or_after=None):
    now = datetime.utcnow()

    # format from the TMA:
    # not_before "2019-07-04T08:46:35.134Z",
    # not_on_or_after "2019-07-04T08:59:55.134Z"
    if not_before is None:
        not_before = now - timedelta(seconds=1)
    if not_on_or_after is None:
        not_on_or_after = now + timedelta(minutes=15)

    if type(not_before) is datetime:
        not_before = '{}z'.format(not_before.isoformat(timespec='milliseconds'))
    if type(not_on_or_after) is datetime:
        not_on_or_after = '{}z'.format(not_on_or_after.isoformat(timespec='milliseconds'))
    attributes = _get_attribute_statement(dict_obj)
    return ASSERTION_XML_TEMPLATE.format(
        id=random_assertion_id(),
        attributes=attributes,
        not_before=not_before,
        not_on_or_after=not_on_or_after
    )


def _sign_assertion(assertion):
    saml_assertion_etree = etree.fromstring(assertion)
    signed_assertion_etree = xml_signer.sign(saml_assertion_etree, key=server_pem,
                                             cert=server_crt)
    return etree.tostring(signed_assertion_etree, encoding="utf-8", xml_declaration=True)


def generate_saml_token_for_kvk(kvk_number, branch_number=None):
    attributes = {HR_ATTRIBUTES[HR_KVK_NUMBER_KEY]: kvk_number}
    if branch_number:
        attributes[HR_ATTRIBUTES[HR_BRANCH_KEY]] = branch_number
    assertion = _get_assertion(attributes)
    signed_assertion = _sign_assertion(assertion)
    saml_token = b64encode(signed_assertion)

    return saml_token


def generate_saml_token_for_bsn(bsn, not_before=None, not_on_or_after=None):
    assertion = _get_assertion({DIGI_D_ATTRIBUTES[DIGI_D_UID_KEY]: bsn}, not_before, not_on_or_after)
    signed_assertion = _sign_assertion(assertion)
    saml_token = b64encode(signed_assertion)

    return saml_token


def generate_tampered_saml_token_(bsn_signed, bsn_tampered):
    saml_assertion_etree = etree.fromstring(_get_assertion({'uid': bsn_signed}))
    signed_assertion_etree = xml_signer.sign(saml_assertion_etree, key=server_pem,
                                             cert=server_crt)
    signed_assertion_etree.find(".//saml:AttributeValue", namespaces={'saml': 'urn:oasis:names:tc:SAML:2.0:assertion'})\
        .text = str(bsn_tampered)
    tampered_assertion_string = etree.tostring(signed_assertion_etree, encoding="utf-8", xml_declaration=True)
    tampered_token = b64encode(tampered_assertion_string)
    return tampered_token


def random_bsn():
    return randint(100000001, 999999998)


def random_assertion_id():
    return randint(10000001, 99999998)


class Request:
    def __init__(self, dict_obj):
        self.headers = dict_obj
