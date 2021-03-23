TMA SAML interpretation package
-------------------------------

Package to offload (functionally) the processing of SAML tokens as received from the TMA

Exposed Methods
===============

Three interpretation methods are available:
 - ``get_user_type``
 - ``get_e_herkenning_attribs``
 - ``get_digi_d_bsn``

.. code-block:: python

	import tma_saml

	# gets the user_type
	user_type = tma_saml.get_user_type(request, certificate)

	# gets the e_herkenning attributes
	e_herkenning_attributes = tma_saml.get_e_herkenning_attribs(request, certificate)

	# gets the bsn
	digi_d_bsn = tma_saml.get_digi_d_bsn(request, certificate)

Exposed Exceptions
==================

Above mentioned methods can raise ``SamlVerificationException`` and ``InvalidBSNException``

.. code-block:: python

	import tma_saml

	try:
		digi_d_bsn = tma_saml.get_digi_d_bsn(request, certificate)
	except SamlVerificationException as e:
		log.error(f"Error in verification of SAML token: {e}")
	except InvalidBSNException as e:
		log.error(f"Invalid BSN: {e}")

Exposed Objects
===============

An enum is available for types of users: ``UserType``

.. code-block:: python

	from tma_saml import UserType

	user_type = tma_saml.get_user_type(request, certificate)
	assert user_type == UserType.BURGER
	assert user_type == UserType.BEDRIJF

Exposed Constants
=================

Following Constants are exposed: ``TMA_SAML_HEADER``, ``HR_KVK_NUMBER_KEY`` and ``HR_BRANCH_KEY``

.. code-block:: python

	import tma_saml

	if tma_saml.TMA_SAML_HEADER in request.headers:
		e_herkenning_attributes = tma_saml.get_e_herkenning_attribs(request, certificate)
		kvk_nummer = e_herkenning_attributes[HR_KVK_NUMBER_KEY]
		branch_nummer =  e_herkenning_attributes[HR_BRANCH_KEY] if HR_BRANCH_KEY in e_herkenning_attributes else None

Exposed Test Client
===================

This package also exposes a Flask Test Client:

.. code-block:: python

	import tma_saml
	from hr import server

	class HrApiTestCase(tma_saml.FlaskServerTMATestCase):
		def setUp(self):
			# custom setup
			...blah...
			# setup of FlaskServerTMATestCase, puts test-client under self.app
			self.app = self.get_tma_test_app(server.application)

		def test_simple(self):
			headers = self.add_e_herkenning_headers('69599076')  # this kvk nummer is from the kvk test data
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


Development
-----------

Testing
=======
Run tests with: ``python setup.py test``

A specific test with: ``python setup.py test -s tma_saml.tests.tma_saml_tests.SamlTestCase``

Publishing
==========
run: ``python3 setup.py sdist``
upload the ``dist/tma_saml-0.2.tar.gz`` to the secure nexus