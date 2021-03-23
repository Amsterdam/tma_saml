import os
from base64 import b64decode
from datetime import datetime, timezone

import dateutil.parser
from signxml import XMLVerifier

from .exceptions import SamlVerificationException, InvalidBSNException, SamlExpiredException
from .user_type import UserType

TMA_SAML_HEADER = 'x-saml-attribute-token1'

NAMESPACE = '{urn:oasis:names:tc:SAML:2.0:assertion}'
STATEMENT_TAG = f'{NAMESPACE}AttributeStatement'
ATTRIBUTE_TAG = f'{NAMESPACE}Attribute'
ATTR_VALUE_TAG = f'{NAMESPACE}AttributeValue'
CONDITION_TAG = f'{NAMESPACE}Conditions'

DIGI_D_UID_KEY = 'digi_d_bsn'

DIGI_D_ATTRIBUTES = {DIGI_D_UID_KEY: 'uid'}

HR_SUBDOSSIER_KEY = 'subdossiernummer'
HR_BRANCH_KEY = 'branchNumber'
HR_KVK_NUMBER_KEY = 'kvkNumber'

HR_ATTRIBUTES = {
    HR_KVK_NUMBER_KEY: 'urn:etoegang:1.9:EntityConcernedID:KvKnr',
    HR_BRANCH_KEY: 'urn:etoegang:1.9:ServiceRestriction:Vestigingsnr',
    # deprecated, but still possible:
    HR_SUBDOSSIER_KEY: 'urn:etoegang:1.9:ServiceRestriction:SubdossierNr',
}


def _get_saml_assertion_attributes(saml_xml):
    statement = saml_xml.find(STATEMENT_TAG)
    return {attrib.attrib['Name']: attrib.find(ATTR_VALUE_TAG).text
            for attrib in statement.iter(ATTRIBUTE_TAG)}


def _get_verified_data(token, cert):
    secondary_cert = os.getenv('TMA_CERTIFICATE_SECONDARY', None)
    try:
        return XMLVerifier().verify(b64decode(token), x509_cert=cert).signed_xml
    except Exception as e:
        if secondary_cert:
            return XMLVerifier().verify(b64decode(token), x509_cert=secondary_cert).signed_xml
        else:
            raise e from None  # `from None` reraise without the current context. py3.5+


def _verify_validity(saml_xml):
    """
    Check if the SAML condition NotBefore and NotOnOrAfter is met.
    :param saml_xml:
    :return:
    """
    not_before, not_on_or_after = _get_validity(saml_xml)

    now = datetime.now(timezone.utc)

    if not_before < now < not_on_or_after:
        return
    else:
        raise SamlExpiredException


def _get_validity(saml_xml):
    condition = saml_xml.find(CONDITION_TAG)

    # '2019-07-05T06:28:34.328z' -> '2019-07-05T06:28:34.328+00:00'
    not_before = condition.attrib['NotBefore']
    not_before = dateutil.parser.isoparse(not_before)

    # '2019-07-05T08:28:34.328z' -> '2019-07-05T08:28:34.328:00:00'
    not_on_or_after = condition.attrib['NotOnOrAfter']
    not_on_or_after = dateutil.parser.isoparse(not_on_or_after)

    return not_before, not_on_or_after


def _verify_saml_token_and_retrieve_saml_attributes(saml_token, saml_cert):
    if not saml_token:
        raise SamlVerificationException('Missing SAML token')

    try:
        verified_data = _get_verified_data(saml_token, saml_cert)
        _verify_validity(verified_data)
        saml_attributes = _get_saml_assertion_attributes(verified_data)
    except SamlExpiredException:
        raise
    except Exception as e:
        raise SamlVerificationException(e)

    return saml_attributes


def _get_hr_attributes_from_saml_token(saml_token, certificate):
    saml_attributes = _verify_saml_token_and_retrieve_saml_attributes(
        saml_token=saml_token,
        saml_cert=certificate
    )

    return {key: saml_attributes[value]
            for key, value in HR_ATTRIBUTES.items()
            if value in saml_attributes}


def _get_bsn_from_saml_token(saml_token, certificate):
    saml_attributes = _verify_saml_token_and_retrieve_saml_attributes(
        saml_token=saml_token,
        saml_cert=certificate
    )

    raw_bsn = saml_attributes[DIGI_D_ATTRIBUTES[DIGI_D_UID_KEY]]
    # BSN of 8 character misses a 0 prefix which is required for elfproef
    if len(raw_bsn) == 8:
        raw_bsn = '0' + raw_bsn

    # BSN Should be 9 characters long.
    if len(raw_bsn) == 9:
        bsn_sum = 0
        for index, nr in enumerate(reversed(raw_bsn)):
            if index == 0:
                multiplier = -1
            else:
                multiplier = index + 1
            bsn_sum += int(nr) * multiplier

        # Elfproef
        if bsn_sum % 11 == 0:
            return raw_bsn

    raise InvalidBSNException()


def get_e_herkenning_attribs(request, certificate):
    """
    Get the valid and signed eHerkenning attributes from a request object.

    Example use:

        request = connexion.request
        certificate = app.config['TMA_CERTIFICATE']
        e_herkenning_attribs = tma_saml.get_e_herkenning_attribs(request, certificate)

    :param request: the request object, containing headers, one of which the SAML token
    :param certificate: the client certificate to verify the signature with
    :return: a dict with the valid and signed eHerkenning attributes
    :raises: SamlVerificationException
    """
    saml_token = request.headers.get(TMA_SAML_HEADER)
    return _get_hr_attributes_from_saml_token(saml_token, certificate)


def get_digi_d_bsn(request, certificate):
    """
    Get the valid and signed BSN from a request object.

    Example use:

        request = connexion.request
        certificate = app.config['TMA_CERTIFICATE']
        digi_d_attrib = tma_saml.get_digi_d_attribs(request, certificate)

    :param request: the request object, containing headers, one of which the SAML token
    :param certificate: the client certificate to verify the signature with
    :return: a string containing the bsn
    :raises: SamlVerificationException, InvalidBSNException
    """
    saml_token = request.headers.get(TMA_SAML_HEADER)
    return _get_bsn_from_saml_token(saml_token, certificate)


def get_user_type(request, certificate) -> UserType:
    """
    Get the userType from a request object.

    Example use:

        request = connexion.request
        certificate = app.config['TMA_CERTIFICATE']
        user_type = tma_saml.get_user_type(request, certificate)

    :param request: the request object, containing headers, one of which the SAML token
    :param certificate: the client certificate to verify the signature with
    :return: a dict with the valid and signed eHerkenning attributes
    :raises: SamlVerificationException, InvalidBSNException
    """

    saml_token = request.headers.get(TMA_SAML_HEADER)
    saml_attributes = _verify_saml_token_and_retrieve_saml_attributes(
        saml_token=saml_token,
        saml_cert=certificate
    )

    if HR_ATTRIBUTES[HR_KVK_NUMBER_KEY] in saml_attributes:
        return UserType.BEDRIJF
    else:
        if DIGI_D_ATTRIBUTES[DIGI_D_UID_KEY] not in saml_attributes:
            raise SamlVerificationException(f"Missing attribute {DIGI_D_ATTRIBUTES[DIGI_D_UID_KEY]} in SAML token")

        if _get_bsn_from_saml_token(saml_token, certificate):
            return UserType.BURGER

        raise InvalidBSNException()


def get_session_valid_until(request, saml_cert):
    saml_token = request.headers.get(TMA_SAML_HEADER)

    verified_data = _get_verified_data(saml_token, saml_cert)
    _verify_validity(verified_data)

    not_before, not_on_or_after = _get_validity(verified_data)

    return not_on_or_after

