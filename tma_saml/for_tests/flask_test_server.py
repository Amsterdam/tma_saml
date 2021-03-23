import unittest

from tma_saml.for_tests import cert_and_key
from tma_saml.tma_saml import TMA_SAML_HEADER
from tma_saml.for_tests.fixtures import generate_saml_token_for_kvk, generate_saml_token_for_bsn


class FlaskServerTMATestCase(unittest.TestCase):
    """
    Test Server for using TMA SAML tokens in tests of Flaks, or Flask-based (for instance: connexion) servers.
    Example use:

        from hr import server

        class HrApiTestCase(tma_saml.FlaskServerTMATestCase):
            def setUp(self):
                # custom setup
                ...blah...
                # setup of FlaskServerTMATestCase, puts test-client under self.app
                self.app = self.get_tma_test_app(server.application)

            def test_simple(self):
                headers = self.add_e_herkenning_headers('69599076')
                response = self.app.get('/hr/vestigingen', headers=headers)
                assert '69599076' in response.data.decode()

            def test_complex(self):
                custom_headers = {'custom_field': 'custom_value'}
                headers = self.add_e_herkenning_headers('69599076', branchNumber='000037940627', headers=custom_headers)
                response = self.app.get('/hr/vestigingen', headers=headers)
                assert '69599076' in response.data.decode()

            def test_bsn(self):
                headers = self.add_digi_d_headers('123456789')
                response = self.app.get('/hr/users', headers=headers)
                assert '123456789' in response.data.decode()


    This tests following Server application

        import connexion
        import tma_saml
        from flask import current_app as app

        def vestiging_get():
            request = connexion.request
            certificate = app.config['TMA_CERTIFICATE']

            try:
                e_herkenning_attribs = tma_saml.get_e_herkenning_attribs(request, certificate)
            except tma_saml.SamlVerificationException:
                return "Exception in getting eHerkenning from SAML ", 400

            kvk_nummer = e_herkenning_attribs[tma_saml.HR_KVK_NUMBER_KEY]
            try:
                branch_nummer = e_herkenning_attribs[tma_saml.HR_BRANCH_KEY]

            # perform your business logic based on kvk_nummer and or branch_nummer


        def user_get():
            request = connexion.request
            certificate = app.config['TMA_CERTIFICATE']

            try:
                bsn = tma_saml.get_digi_d_bsn(request, certificate)
            except tma_saml.SamlVerificationException:
                return "Exception in getting bsn from SAML ", 400
            except tma_saml.InvalidBSNException:
                return "Exception in getting bsn from SAML ", 400

            # perform your business logic based on bsn

"""
    def get_tma_test_app(self, app):
        app.testing = True
        app.config.update(TMA_CERTIFICATE=cert_and_key.server_crt)
        return app.test_client()

    def _get_e_herkenning_saml_token(self, kvkNumber, branchNumber=None):
        return generate_saml_token_for_kvk(kvkNumber, branch_number=branchNumber)

    def _get_digi_d_saml_token(self, bsn):
        return generate_saml_token_for_bsn(bsn)

    def add_digi_d_headers(self, bsn, headers=None):
        if headers is None:
            headers = {}
        headers[TMA_SAML_HEADER] = self._get_digi_d_saml_token(bsn)
        return headers

    def add_e_herkenning_headers(self, kvkNumber, branchNumber=None, headers=None):
        if headers is None:
            headers = {}
        headers[TMA_SAML_HEADER] = self._get_e_herkenning_saml_token(kvkNumber, branchNumber)
        return headers


if __name__ == '__main__':
    unittest.main()
