import unittest
from membership import OrganisationUnitConfig, OrganisationUnit, calculate_membership_fee

class TestOrganisationUnitConfig(unittest.TestCase):

    def test_init(self):
        config = OrganisationUnitConfig(True, 1000)
        self.assertEqual(config.has_fixed_membership_fee, True)
        self.assertEqual(config.fixed_membership_fee_amount, 1000)

class TestCalculateMembershipFee(unittest.TestCase):

    def test_with_fixed_membership_fee(self):
        config = OrganisationUnitConfig(True, 1000)
        parent_unit = OrganisationUnit('Client', config)
        unit = OrganisationUnit('Branch', None, parent_unit)
        fee = calculate_membership_fee(2500, 'week', unit)
        self.assertEqual(fee, 1000)

    def test_with_unfixed_membership_fee(self):
        config = OrganisationUnitConfig(False, 0)
        parent_unit = OrganisationUnit('Parent', config)
        unit = OrganisationUnit('Child', None, parent_unit)
        fee = calculate_membership_fee(20000, 'month', unit)
        self.assertEqual(fee, 9000)

    def test_with_invalid_rent_period(self):
        parent_unit = OrganisationUnit('Parent')
        unit = OrganisationUnit('Child', None, parent_unit)
        with self.assertRaises(ValueError):
            calculate_membership_fee(1000, 'month', unit)
            
    def test_flat(self):
        config = OrganisationUnitConfig(False, 0)
        config2 = OrganisationUnitConfig(True, 350000)
        config3 = OrganisationUnitConfig(True, 45000)
        unit = OrganisationUnit('Client', config)
        unit1 = OrganisationUnit('Branch 1', parent = unit)
        unit2 = OrganisationUnit('Branch 2', config2, parent = unit)
        area1 = OrganisationUnit('Area 1', parent = unit2 )  
        fee = calculate_membership_fee(20000, 'month', area1)
        self.assertEqual(fee, 350000)

if __name__ == '__main__':
    unittest.main()