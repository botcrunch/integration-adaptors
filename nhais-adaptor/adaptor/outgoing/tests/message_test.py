import unittest
from testfixtures import compare
from adaptor.outgoing.message import MessageAdaptor
from fhirclient.models.patient import Patient
from fhirclient.models.humanname import HumanName
from fhirclient.models.identifier import Identifier
from fhirclient.models.address import Address
from edifact.models.name import Name


class MessageAdaptorTest(unittest.TestCase):
    """
    Tests the conversion of fhir to edifact
    """

    def test_create_patient_name(self):
        """ Test the creation edifact patient name object"""

        with self.subTest("Patient with just title, first name and surname"):
            name = HumanName({'prefix': ['Mr'], 'family': 'Parker', 'given': ['Peter']})
            expected = Name(title="Mr", family_name="Parker", first_given_forename="Peter")
            edi_name = MessageAdaptor.create_patient_name(name)
            compare(edi_name, expected)

        with self.subTest("Patient with all the name details"):
            name = HumanName({'prefix': ['Mr'], 'family': 'Parker', 'given': ['Peter', 'Spidey', 'Senses']})
            expected = Name(title="Mr", family_name="Parker", first_given_forename="Peter", middle_name="Spidey",
                            third_given_forename="Senses")
            edi_name = MessageAdaptor.create_patient_name(name)
            compare(edi_name, expected)

    def test_create_message_segment_patient_details(self):
        """
        Test the function to create an edifact message segment for patient details
        """

        with self.subTest("Patient with no previous names or addresses"):
            pat_address = Address(
                {'line': ['1 Spidey Way', 'Spiderville'], 'city': 'Spider Town', 'district': 'Spideyshire',
                 'postalCode': 'SP1 1AA'})
            nhs_number = Identifier({'value': 'NHSNO11111'})
            name = HumanName({'prefix': ['Mr'], 'family': 'Parker', 'given': ['Peter']})
            patient = Patient({'identifier': [nhs_number.as_json()], 'gender': 'male', 'name': [name.as_json()],
                               'birthDate': '2019-04-23',
                               'address': [pat_address.as_json()]})

            msg_seg_pat_details = MessageAdaptor.create_message_segment_patient_detail(patient)
            msg_seg_pat_details.to_edifact()
            print(msg_seg_pat_details.to_edifact())
