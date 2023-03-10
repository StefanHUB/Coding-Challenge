import unittest
from flatbond import OrganisationUnitConfig, OrganisationUnit, calculate_membership_fee

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
        config4 = OrganisationUnitConfig(True, 25000)
        client = OrganisationUnit('Client', config)
        div_a = OrganisationUnit('Division A',config, parent = client)
        div_b = OrganisationUnit('Division B', config2, parent = client)
        area_a = OrganisationUnit('Area A', config3, parent = div_a )
        area_b = OrganisationUnit('Area B', config,  parent = div_a )
        area_c = OrganisationUnit('Area C', config3, parent = div_b )
        area_d = OrganisationUnit('Area D', config, parent = div_b )
        branch_a = OrganisationUnit('Branch A', parent = area_a )  
        branch_b = OrganisationUnit('Branch B', config, parent = area_a )
        branch_c = OrganisationUnit('Branch C', config, parent = area_a )
        branch_d = OrganisationUnit('Branch D', parent = area_a )
        branch_e = OrganisationUnit('Branch E', config, parent = area_b )
        branch_f = OrganisationUnit('Branch F', config, parent = area_b )
        branch_g = OrganisationUnit('Branch G', config, parent = area_b )
        branch_h = OrganisationUnit('Branch H', config, parent = area_b )
        branch_i = OrganisationUnit('Branch I', config, parent = area_c )
        branch_j = OrganisationUnit('Branch J', config, parent = area_c )
        branch_k = OrganisationUnit('Branch K', config4, parent = area_c )
        branch_l = OrganisationUnit('Branch L', config, parent = area_c )
        branch_m = OrganisationUnit('Branch M', parent = area_d )
        branch_n = OrganisationUnit('Branch N', config, parent = area_d )
        branch_o = OrganisationUnit('Branch O', config, parent = area_d )
        branch_p = OrganisationUnit('Branch P', config, parent = area_d )
        fee = calculate_membership_fee(20000, 'month', branch_d)
        self.assertEqual(fee, 45000)

if __name__ == '__main__':
    unittest.main()