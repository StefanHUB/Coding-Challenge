
class OrganisationUnitConfig:
    """
    A configuration object for an OrganisationUnit.

    Args:
        has_fixed_membership_fee (bool): Whether the organisation has a fixed membership fee.
        fixed_membership_fee_amount (int): The fixed membership fee amount.

    """
    def __init__(self, has_fixed_membership_fee : bool = None, fixed_membership_fee_amount : int = None) -> None:
        self.has_fixed_membership_fee = has_fixed_membership_fee
        self.fixed_membership_fee_amount = fixed_membership_fee_amount


class OrganisationUnit:
    """
    Represents an OrganisationUnit.

    Args:
        name (str): The name of the organisation.
        config (OrganisationUnitConfig): The configuration object for the organisation.
        parent (OrganisationUnit): The parent organisation, acts as a pointer to create an organisation structure
    """
    def __init__(self, name:str, config : OrganisationUnitConfig = None, parent : 'OrganisationUnit' = None) -> None:
        self.name = name
        self.config = config
        self.parent = parent



def calculate_membership_fee(rent_amount:int, rent_period:str, organisation_unit:OrganisationUnit) -> int:
    """
    Calculates the membership fee for an OrganisationUnit.

    Args:
        rent_amount (int): The rent amount.
        rent_period (str): The rent period ('month' or 'week').
        organisation_unit (OrganisationUnit): The organisation for which to calculate the membership fee.

    Returns:
        int: The calculated membership fee.

    Raises:
        ValueError: If the rent amount is not valid for the respective rent period.
    """
    membership_fee = 0
    vat = 0.2

    # Rent validation

    if rent_period == "month" and  (rent_amount < 110 * 100 or rent_amount > 8660 * 100):
        raise ValueError("Monthly rent cannot be validated")
    if rent_period == "week" and (rent_amount < 25 * 100 or rent_amount > 2000 * 100):
        raise ValueError("Weekly rent cannot be validated")
    if rent_period != "month" and rent_period != "week":
        raise ValueError("Invalid rent period")

    
    # Calculate fixed membership fee  
    if organisation_unit.config is not None and organisation_unit.config.has_fixed_membership_fee:
        membership_fee = organisation_unit.config.fixed_membership_fee_amount

    # Calculate unfixed membership fee
    elif organisation_unit.config is not None:
        if rent_period == "month":       
            membership_fee = rent_amount / 4 + vat*rent_amount
        if rent_period == "week":
            membership_fee = rent_amount + vat*rent_amount
        if (rent_amount) < 120 * 100:
            membership_fee = 120 * 100 + vat * 120 * 100
    
    # Check parents recursively to find an existing configuration     
    if organisation_unit.config is None and organisation_unit.parent is not None:
        membership_fee = calculate_membership_fee(rent_amount,rent_period,organisation_unit.parent)

    return membership_fee

