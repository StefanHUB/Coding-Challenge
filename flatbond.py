"""
The organisation structure is going to be based on the parent arg from OrganisationUnit which
will act as a pointer that will be pointing towards the address of the parent organisation unit

"""


class OrganisationUnitConfig:
    """
    A configuration object for an organisation unit


    Args:
        has_fixed_membership_fee (bool): Whether the organisation has a fixed membership fee
        fixed_membership_fee_amount (int): The fixed membership fee amount

    """
    def __init__(self, has_fixed_membership_fee: bool = None, fixed_membership_fee_amount: int = None) -> None:
        self.has_fixed_membership_fee = has_fixed_membership_fee
        self.fixed_membership_fee_amount = fixed_membership_fee_amount


class OrganisationUnit:
    """
    Represents an organisation unit


    Args:
        name (str): The name of the organisation.
        config (OrganisationUnitConfig): The configuration object for the organisation.
        parent (OrganisationUnit): The parent organisation, acts as a pointer
    """
    def __init__(self, name: str, config: OrganisationUnitConfig = None, parent: 'OrganisationUnit' = None) -> None:
        self.name = name
        self.config = config
        self.parent = parent


def calculate_membership_fee(rent_amount: int, rent_period: str, organisation_unit: OrganisationUnit) -> int:
    """
    Calculates the membership fee for an OrganisationUnit

    Args:
        rent_amount : The rent amount.
        rent_period : The rent period ('month' or 'week').
        organisation_unit : The organisation for which to calculate the membership.

    Returns:
        int: The actual membership fee.

    Raises:
        ValueError: If the rent amount is not valid for the respective rent period
                    If the rent period is not either 'week' or 'month'
    """
    membership_fee = 0
    VAT = 0.2

    # Input Validation
    if rent_amount < 1:
        raise ValueError("Invalid rent amount")
    if rent_period not in ('month', 'week'):
        raise ValueError("Invalid rent period")
    if not isinstance(organisation_unit, OrganisationUnit):
        raise ValueError("Invalid organisation")

    # Rent validation
    if rent_period == "month" and (rent_amount < 110 * 100 or rent_amount > 8660 * 100):
        raise ValueError("Monthly rent cannot be validated")
    if rent_period == "week" and (rent_amount < 25 * 100 or rent_amount > 2000 * 100):
        raise ValueError("Weekly rent cannot be validated")

    # Calculate fixed membership fee
    if organisation_unit.config is not None and organisation_unit.config.has_fixed_membership_fee:
        membership_fee = organisation_unit.config.fixed_membership_fee_amount

    # Calculate unfixed membership fee
    elif organisation_unit.config is not None:
        if rent_period == "month":
            membership_fee = rent_amount / 4 + VAT * (rent_amount / 4)
            if (rent_amount/4) < 120 * 100:
                membership_fee = 12000 + VAT * 12000
        elif rent_period == "week":
            membership_fee = rent_amount + VAT * rent_amount
            if (rent_amount) < 120 * 100:
                membership_fee = 12000 + VAT * 12000

    # Check parents recursively to find an existing configuration
    if organisation_unit.config is None and organisation_unit.parent is not None:
        membership_fee = calculate_membership_fee(rent_amount, rent_period, organisation_unit.parent)

    return int(membership_fee)
