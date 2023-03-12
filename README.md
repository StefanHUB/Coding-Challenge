# Coding-Challenge


## Organisation Structure
The organization structure is based on the parent argument of **OrganisationUnit**. The *parent* acts as a pointer towards the address of the parent organization unit.

## OrganisationUnitConfig Class

The **OrganisationUnitConfig** is a configuration object for an organisation unit, which has the following attributes:

 ● *has_fixed_membership_fee* (bool): Indicates whether the organisation has a fixed membership fee
 
 ● *fixed_membership_fee_amount* (int): The fixed membership fee amount

## OrganisationUnit Class

The **OrganisationUnit** class represents an organisation unit, which has the following attributes:

 ● *name* (str): The name of the organisation.
 
 ● *config* (OrganisationUnitConfig): The configuration object for the organisation.
 
 ● *parent* (OrganisationUnit): The parent organisation, acts as a pointer

## calculate_membership_fee Function

The function calculates the membership fee for an organisation unit based on the rent amount, rent period, and the organisation unit configuration. It returns the calculated membership fee as an integer.
The function has the following arguments:

 ● *rent_amount* (int): The rent amount.
 
 ● *rent_period* (str): The rent period ('month' or 'week').
 
 ● *organisation_unit* (OrganisationUnit): The organisation for which to calculate the membership.

 The function raises a ValueError exception if:

 ● The rent amount is less than zero

 ● The rent period is not either 'week' or 'month'
 
 ● The organisation unit is not an instance of **OrganisationUnit** class

 ● The rent amount is not valid for the respective rent period

## Unit Tests
The project includes unit tests to ensure the proper functioning of the code. There are three test classes:

 ● TestOrganisationUnitConfig: Tests the **OrganisationUnitConfig** class constructor.
 
 ● TestOrganisationUnit: Tests the **OrganisationUnit** class constructor.
 
 ● TestCalculateMembershipFee: Tests the calculate_membership_fee function.
 The TestCalculateMembershipFee class uses a hierarchy of **OrganisationUnit** objects for testing purposes
 
 The hierarchy used is the one that was given as an example
