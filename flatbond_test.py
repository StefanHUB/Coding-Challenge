import unittest
from flatbond import OrganisationUnitConfig, OrganisationUnit, calculate_membership_fee



class TestOrganisationUnitConfig(unittest.TestCase):

# Test organisation configuration constructor
    def test_init(self):
        config = OrganisationUnitConfig(True, 1000)
        self.assertEqual(config.has_fixed_membership_fee, True)
        self.assertEqual(config.fixed_membership_fee_amount, 1000)

class TestCalculateMembershipFee(unittest.TestCase):

    def setUp(self):
        self.config = OrganisationUnitConfig(False, 0)
        self.config2 = OrganisationUnitConfig(True, 350000)
        self.config3 = OrganisationUnitConfig(True, 45000)
        self.config4 = OrganisationUnitConfig(True, 25000)
        self.client = OrganisationUnit('Client', self.config, parent=None)
        self.div_a = OrganisationUnit('Division A', self.config, parent=self.client)
        self.div_b = OrganisationUnit('Division B', self.config2, parent=self.client)
        self.area_a = OrganisationUnit('Area A', self.config3, parent=self.div_a)
        self.area_b = OrganisationUnit('Area B', parent=self.div_a)
        self.area_c = OrganisationUnit('Area C', self.config3, parent=self.div_b)
        self.area_d = OrganisationUnit('Area D', self.config, parent=self.div_b)
        self.branch_a = OrganisationUnit('Branch A', parent=self.area_a)  
        self.branch_b = OrganisationUnit('Branch B', self.config, parent=self.area_a)
        self.branch_c = OrganisationUnit('Branch C', self.config, parent=self.area_a)
        self.branch_d = OrganisationUnit('Branch D', parent=self.area_a)
        self.branch_e = OrganisationUnit('Branch E', self.config, parent=self.area_b)
        self.branch_f = OrganisationUnit('Branch F', self.config, parent=self.area_b)
        self.branch_g = OrganisationUnit('Branch G', self.config, parent=self.area_b)
        self.branch_h = OrganisationUnit('Branch H', self.config, parent=self.area_b)
        self.branch_i = OrganisationUnit('Branch I', self.config, parent=self.area_c)
        self.branch_j = OrganisationUnit('Branch J', self.config, parent=self.area_c)
        self.branch_k = OrganisationUnit('Branch K', self.config4, parent=self.area_c)
        self.branch_l = OrganisationUnit('Branch L', self.config, parent=self.area_c)
        self.branch_m = OrganisationUnit('Branch M', parent=self.area_d)
        self.branch_n = OrganisationUnit('Branch N', self.config, parent=self.area_d)
        self.branch_o = OrganisationUnit('Branch O', self.config, parent=self.area_d)
        self.branch_p = OrganisationUnit('Branch P', self.config, parent=self.area_d)


# Test organisation unit constructor
    def test_init(self):
        config = OrganisationUnitConfig(True, 1000)
        unit = OrganisationUnit('Unit', config)
        self.assertEqual(unit.config.has_fixed_membership_fee, True)
        self.assertEqual(unit.config.fixed_membership_fee_amount, 1000)
        self.assertEqual(unit.name, 'Unit')
        self.assertEqual(unit.config, config)

# Min week -> 2500, Max week -> 200000, Min month -> 11000, Max month -> 860000
    def test_validation(self):
        config = OrganisationUnitConfig(True, 1000)
        parent_unit = OrganisationUnit('Parent',config)
        unit = OrganisationUnit('Child', None, parent_unit)
        with self.assertRaises(ValueError):
            calculate_membership_fee(200001, 'week', unit)
        with self.assertRaises(ValueError):
            calculate_membership_fee(2499, 'week', unit)
        with self.assertRaises(ValueError):
            calculate_membership_fee(10999, 'month', unit)
        with self.assertRaises(ValueError):
            calculate_membership_fee(866001, 'month', unit)

# Test calculation when organisation configuration has fixed membership fee
    def test_with_fixed_membership_fee(self):
        config = OrganisationUnitConfig(True, 1000)
        parent_unit = OrganisationUnit('Client', config)
        unit = OrganisationUnit('Branch', None, parent_unit)
        fee = calculate_membership_fee(2500, 'week', unit)
        self.assertEqual(fee, 1000)
        fee = calculate_membership_fee(3000, 'week', self.area_a)
        self.assertEqual(fee, 45000)

# Test calculation when organisation configuration does not have fixed membership fee
    def test_with_unfixed_membership_fee(self):
        fee = calculate_membership_fee(20000, 'month', self.branch_m)
        self.assertEqual(fee, 9000)
    

    
# Minimum membership, if rent lower than 120$ membership will be fixed at 120$ + VAT
    def test_minimum_membership(self):
        fee = calculate_membership_fee(12000,'week',self.branch_l)
        fee1 = calculate_membership_fee(11000,'week',self.branch_l)
        self.assertEqual(fee , 14400)
        self.assertEqual(fee1, 14400)

# Test recursion when organisation unit does not have a config
    def test_flat(self):
        fee = calculate_membership_fee(20000, 'month', self.branch_d)
        self.assertEqual(fee, 45000)


if __name__ == '__main__':
    unittest.main()