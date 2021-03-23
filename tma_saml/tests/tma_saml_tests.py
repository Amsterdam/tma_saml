import unittest
from datetime import timedelta, datetime, timezone
from unittest.mock import patch

import signxml
from signxml import InvalidSignature

from tma_saml import UserType, TMA_SAML_HEADER, get_user_type, HR_KVK_NUMBER_KEY, HR_BRANCH_KEY
from tma_saml.exceptions import InvalidBSNException, SamlExpiredException
from tma_saml.for_tests import cert_and_key, fixtures
from tma_saml.for_tests.cert_and_key import secondary_server_pem, secondary_server_crt, server_crt
from tma_saml.tma_saml import _get_saml_assertion_attributes, _get_verified_data, get_digi_d_bsn, \
    get_e_herkenning_attribs, get_session_valid_until


class SamlTestCase(unittest.TestCase):
    def test_saml(self):
        bsn = fixtures.random_bsn()
        verified_data = _get_verified_data(fixtures.generate_saml_token_for_bsn(bsn), cert_and_key.server_crt)
        saml_attributes = _get_saml_assertion_attributes(verified_data)
        self.assertIn('uid', saml_attributes)
        self.assertEqual(str(bsn), saml_attributes['uid'])

    def test_tampered(self):
        bsn = fixtures.random_bsn()
        tampered_token = fixtures.generate_tampered_saml_token_(bsn, bsn + 1)
        self.assertRaises(signxml.exceptions.InvalidDigest,
                          _get_verified_data, tampered_token, cert_and_key.server_crt)
        try:
            _get_verified_data(tampered_token, cert_and_key.server_crt)
        except signxml.exceptions.InvalidDigest as e:
            self.assertEqual('Digest mismatch for reference 0', e.args[0])

    def test_check_operation_burger(self):
        token = fixtures.generate_saml_token_for_bsn('987654329')
        request = fixtures.Request({TMA_SAML_HEADER: token})

        user_type = get_user_type(request, cert_and_key.server_crt)
        self.assertEqual(user_type, UserType.BURGER)

        bsn = get_digi_d_bsn(request, cert_and_key.server_crt)
        self.assertEqual(bsn, '987654329')

    def test_check_operation_fails_invalid_bsn(self):
        token = fixtures.generate_saml_token_for_bsn('987654321')
        request = fixtures.Request({TMA_SAML_HEADER: token})
        self.assertRaises(InvalidBSNException, get_user_type, request, cert_and_key.server_crt)
        self.assertRaises(InvalidBSNException, get_digi_d_bsn, request, cert_and_key.server_crt)

    def test_check_operation_company(self):
        token = fixtures.generate_saml_token_for_kvk('1234')
        request = fixtures.Request({TMA_SAML_HEADER: token})

        user_type = get_user_type(request, cert_and_key.server_crt)
        self.assertEqual(user_type, UserType.BEDRIJF)

        e_herkenning_attributes = get_e_herkenning_attribs(request, cert_and_key.server_crt)
        self.assertEqual(e_herkenning_attributes[HR_KVK_NUMBER_KEY], '1234')

    def test_check_operation_company_branch(self):
        token = fixtures.generate_saml_token_for_kvk('1234', branch_number='321564')
        request = fixtures.Request({TMA_SAML_HEADER: token})

        user_type = get_user_type(request, cert_and_key.server_crt)
        self.assertEqual(user_type, UserType.BEDRIJF)

        e_herkenning_attributes = get_e_herkenning_attribs(request, cert_and_key.server_crt)
        self.assertEqual(e_herkenning_attributes[HR_KVK_NUMBER_KEY], '1234')
        self.assertEqual(e_herkenning_attributes[HR_BRANCH_KEY], '321564')

    def test_validity_verification_past(self):
        now = datetime.utcnow()
        invalid_not_before = now - timedelta(weeks=52)
        invalid_not_on_or_after = now - timedelta(weeks=51)
        token = fixtures.generate_saml_token_for_bsn('987654321', invalid_not_before, invalid_not_on_or_after)

        request = fixtures.Request({TMA_SAML_HEADER: token})
        self.assertRaises(SamlExpiredException, get_user_type, request, cert_and_key.server_crt)

    def test_validity_verification_future(self):
        now = datetime.utcnow()
        invalid_not_before = now + timedelta(weeks=52)
        invalid_not_on_or_after = now + timedelta(weeks=51)
        token = fixtures.generate_saml_token_for_bsn('987654321', invalid_not_before, invalid_not_on_or_after)

        request = fixtures.Request({TMA_SAML_HEADER: token})
        self.assertRaises(SamlExpiredException, get_user_type, request, cert_and_key.server_crt)

    def test_get_session_valid_until(self):
        now = datetime.utcnow()
        now = now.replace(microsecond=(now.microsecond // 1000) * 1000)  # decrease the resolution to match as it is saved in saml token
        not_on_or_after_expected = now + timedelta(minutes=15)

        bsn = fixtures.random_bsn()
        token = fixtures.generate_saml_token_for_bsn(bsn, not_on_or_after=not_on_or_after_expected)

        request = fixtures.Request({TMA_SAML_HEADER: token})

        not_on_or_after = get_session_valid_until(request, server_crt)

        not_on_or_after = not_on_or_after.replace(tzinfo=None)  # returned date does have a timezone
        self.assertEqual(not_on_or_after, not_on_or_after_expected)


class SamlSecondaryCertTestCase(unittest.TestCase):

    @patch('tma_saml.for_tests.fixtures.server_pem', secondary_server_pem)
    @patch('tma_saml.for_tests.fixtures.server_crt', secondary_server_crt)
    def test_secondary_cert_get_bsn(self):
        token = fixtures.generate_saml_token_for_bsn('987654329')

        # fail without secondary cert being set
        with self.assertRaises(InvalidSignature):
            _get_verified_data(token, server_crt)

        # set the environment to have the secondary tma cert
        with patch.dict('os.environ', {'TMA_CERTIFICATE_SECONDARY': secondary_server_crt}):
            _get_verified_data(token, server_crt)


if __name__ == '__main__':
    unittest.main()
