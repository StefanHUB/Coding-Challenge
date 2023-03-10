"""
■ Minimum rent amount is £25 per week or £110 per month 
■ Maximum rent amount is £2000 per week or £8660 per month 

○ VAT is 20%


"""
# Configuration

class OrganisationUnitConfig:
    def __init__(self, has_fixed_membership_fee : bool = None, fixed_membership_fee_amount : int = None):
        self.has_fixed_membership_fee = has_fixed_membership_fee
        self.fixed_membership_fee_amount = fixed_membership_fee_amount

# Organisation

class OrganisationUnit:
    def __init__(self, name:str, config : OrganisationUnitConfig = None, parent : 'OrganisationUnit' = None):
        self.name = name
        self.config = config
        self.parent = parent


def calculate_membership_fee(rent_amount:int, rent_period:str, organisation_unit:OrganisationUnit) -> int:

    membership_fee = None

# Validation

    if rent_period == "month" and  (rent_amount < 110 * 100 or rent_amount > 8660 * 100):
        raise ValueError("Monthly rent cannot be validated")
    
    if rent_period == "week" and (rent_amount < 25 * 100 or rent_amount > 2000 * 100):
        raise ValueError("Weekly rent cannot be validated")
    
# Fixed membership fee
    
    if organisation_unit.config is not None and organisation_unit.config.has_fixed_membership_fee:
        membership_fee = organisation_unit.config.fixed_membership_fee_amount

# Unfixed membership fee

    elif organisation_unit.config is not None:
        if rent_period == "month":       
            membership_fee = rent_amount / 4 + 0.2*rent_amount
        if rent_period == "week":
            membership_fee = rent_amount + 0.2*rent_amount
        if (rent_amount) < 120 * 100:
            membership_fee = 120*100 + 0.2*rent_amount
    
# Check parents recursively to find an existing configuration
          
    if organisation_unit.config is None and organisation_unit.parent is not None:
        membership_fee = calculate_membership_fee(rent_amount,rent_period,organisation_unit.parent)

    
            
    return membership_fee   

# x = OrganisationUnitConfig(False, 0)
# v = OrganisationUnitConfig(True, 2000)
# y = OrganisationUnit("Area", x, parent = None)
# z = OrganisationUnit("Branch", config=None, parent = None)



print(calculate_membership_fee(2600, "week", y))
