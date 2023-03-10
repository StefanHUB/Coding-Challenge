import unittest
from flatbond import OrganisationUnitConfig, OrganisationUnit, calculate_membership_fee


class TestOrganisationUnitConfig(unittest.TestCase):
    # Test organisation configuration constructor
    def test_init(self):
        config = OrganisationUnitConfig(True, 1000)
        self.assertEqual(config.has_fixed_membership_fee, True)
        self.assertEqual(config.fixed_membership_fee_amount, 1000)


class TestOrganisationUnit(unittest.TestCase):
    # Test organisation unit constructor
    def test_init(self):
        config = OrganisationUnitConfig(True, 1000)
        unit = OrganisationUnit('Unit', config)
        self.assertEqual(unit.config.has_fixed_membership_fee, True)
        self.assertEqual(unit.config.fixed_membership_fee_amount, 1000)
        self.assertEqual(unit.name, 'Unit')
        self.assertEqual(unit.config, config)


class TestCalculateMembershipFee(unittest.TestCase):
    # Create a hierarchy of organisation units for testing purposes
    def setUp(self):
        config = OrganisationUnitConfig(False, 0)
        config2 = OrganisationUnitConfig(True, 350000)
        config3 = OrganisationUnitConfig(True, 45000)
        config4 = OrganisationUnitConfig(True, 25000)
        client = OrganisationUnit('Client', config, parent=None)
        div_a = OrganisationUnit('Division A', config, parent=client)
        div_b = OrganisationUnit('Division B', config2, parent=client)
        area_a = OrganisationUnit('Area A', config3, parent=div_a)
        area_b = OrganisationUnit('Area B', parent=div_a)
        area_c = OrganisationUnit('Area C', config3, parent=div_b)
        area_d = OrganisationUnit('Area D', config, parent=div_b)
        self.branch_a = OrganisationUnit('Branch A', parent=area_a)
        self.branch_b = OrganisationUnit('Branch B', config, parent=area_a)
        self.branch_c = OrganisationUnit('Branch C', config, parent=area_a)
        self.branch_d = OrganisationUnit('Branch D', parent=area_a)
        self.branch_e = OrganisationUnit('Branch E', config, parent=area_b)
        self.branch_f = OrganisationUnit('Branch F', config, parent=area_b)
        self.branch_g = OrganisationUnit('Branch G', config, parent=area_b)
        self.branch_h = OrganisationUnit('Branch H', config, parent=area_b)
        self.branch_i = OrganisationUnit('Branch I', config, parent=area_c)
        self.branch_j = OrganisationUnit('Branch J', config, parent=area_c)
        self.branch_k = OrganisationUnit('Branch K', config4, parent=area_c)
        self.branch_l = OrganisationUnit('Branch L', config, parent=area_c)
        self.branch_m = OrganisationUnit('Branch M', parent=area_d)
        self.branch_n = OrganisationUnit('Branch N', config, parent=area_d)
        self.branch_o = OrganisationUnit('Branch O', config, parent=area_d)
        self.branch_p = OrganisationUnit('Branch P', config, parent=area_d)

    # Min week -> 2,500 ; Max week -> 200,000 ; Min month -> 11,000 ; Max month -> 860,000
    def test_validation(self):
        unit = OrganisationUnit('Child', None, self.branch_b)
        with self.assertRaises(ValueError):
            calculate_membership_fee(200001, 'week', unit)
        with self.assertRaises(ValueError):
            calculate_membership_fee(2499, 'week', unit)
        with self.assertRaises(ValueError):
            calculate_membership_fee(10999, 'month', unit)
        with self.assertRaises(ValueError):
            calculate_membership_fee(866001, 'month', unit)
        with self.assertRaises(ValueError):
            calculate_membership_fee(3000, 'wee', unit)

    # Test calculation when organisation configuration has fixed membership fee

    def test_with_fixed_membership_fee(self):
        config = OrganisationUnitConfig(True, 2000)
        unit = OrganisationUnit('Unit', config, self.branch_k)
        fee1 = calculate_membership_fee(2500, 'week', unit)
        self.assertEqual(fee1, 2000)
        fee2 = calculate_membership_fee(12000, 'week', self.branch_j)
        self.assertEqual(fee2, 14400)

    # Test calculation when organisation configuration does not have fixed membership fee
    def test_with_unfixed_membership_fee(self):
        fee = calculate_membership_fee(20000, 'month', self.branch_m)
        self.assertEqual(fee, 9000)

    # Test minimum membership, if rent lower than 120$ membership will be fixed at 120$ + VAT
    def test_minimum_membership(self):
        fee = calculate_membership_fee(12000, 'week', self.branch_l)
        fee1 = calculate_membership_fee(11000, 'week', self.branch_l)
        self.assertEqual(fee, 14400)
        self.assertEqual(fee1, 14400)

    # Test recursion when current organisation unit does not have a configuration
    def test_recursion(self):
        fee = calculate_membership_fee(20000, 'month', self.branch_d)
        self.assertEqual(fee, 45000)


if __name__ == '__main__':
    unittest.main()
