from pydantic import BaseModel, Field, ValidationError
from typing import Optional, Union, List
from enum import Enum


class PersonalInfo(str, Enum):
    CONTRACT = "EMPLOYMENT CONTRACT FULL WORK"
    TOURISM_VISA = "eVisa - Tourism"
    EMPLOYMENT_VISA = "eVisa - Employment"
    RESIDENCE = "Residence"
    CHANGE_STATUS = "Change Status"
    HEALTHCARE = "Healthcare Professional Registration Certificate"
    PASSPORT = "Passport"


class ContractData(BaseModel):
    work_style: Optional[str] = Field(
        None, description="Type of work (e.g., Full time, Part time, Temporary)"
    )
    transaction_number: Optional[List[str]] = Field(
        None, description="Transaction number used by MOHRE"
    )
    name: Optional[str] = Field(None, description="Full legal name of the employee")
    nationality: Optional[str] = Field(None, description="Nationality of the employee")
    passport_number: Optional[str] = Field(None, description="Passport number")
    date_of_birth: Optional[List[str]] = Field(
        None, description="Date of birth (YYYY-MM-DD or as found)"
    )
    academic_qualification: Optional[str] = Field(
        None, description="Academic qualification"
    )
    contract_start: Optional[str] = Field(
        None, description="Start date of the contract"
    )
    contract_end: Optional[str] = Field(None, description="End date of the contract")


class VisaData(BaseModel):
    issue_date: Optional[str] = Field(
        None, description="Visa issue date (YYYY-MM-DD or as found) or similar format"
    )
    place_of_issue: Optional[str] = Field(
        None,
        description="Place of issue where the visa was issued and stamped by the Country government",
    )
    valid_until: Optional[str] = Field(None, description="Visa expiration date")
    uid_number: Optional[str] = Field(None, description="UID number (9 to 15 digits)")
    full_name: Optional[str] = Field(None, description="Full name of the visa holder")
    nationality: Optional[str] = Field(None, description="Nationality")
    place_of_birth: Optional[str] = Field(None, description="Place of birth")
    date_of_birth: Optional[str] = Field(None, description="Date of birth")
    passport_number: Optional[str] = Field(None, description="Passport number")
    profession: Optional[str] = Field(None, description="Profession listed")


class ResidenceData(BaseModel):
    id_number: Optional[str] = Field(
        None, description="ID number, may contain Arabic characters"
    )
    passport_number: Optional[str] = Field(None, description="Passport number")
    name: Optional[str] = Field(None, description="Full name")
    profession: Optional[str] = Field(None, description="Profession")
    issue_date: Optional[str] = Field(None, description="Issue date")
    expiry_date: Optional[str] = Field(None, description="Expiration date")


class ChangeStatusData(BaseModel):
    uid_number: Optional[str] = Field(None, description="UID number")
    name: Optional[str] = Field(None, description="Full name")
    nationality: Optional[str] = Field(None, description="Nationality")
    profession: Optional[str] = Field(None, description="Profession")
    passport_number: Optional[str] = Field(None, description="Passport number")
    employer_name: Optional[str] = Field(None, description="Employer name")
    residence_stamping_deadline: Optional[str] = Field(
        None, description="Deadline for residence stamping"
    )


class HealthcareRegistrationData(BaseModel):
    professional_name: Optional[str] = Field(
        None, description="Name of healthcare professional"
    )
    dha_unique_id: Optional[str] = Field(None, description="DHA Unique Identifier")


class PassportData(BaseModel):
    passport_number: Optional[str] = Field(None, description="Passport number")
    name: Optional[str] = Field(None, description="Full name on passport")
    date_of_birth: Optional[str] = Field(None, description="Date of birth")
    date_of_issue: Optional[str] = Field(None, description="Date of issue")
    date_of_expiry: Optional[str] = Field(None, description="Date of expiry")
    profession: Optional[str] = Field(None, description="Profession listed")


# Unified Document Schema
class DocumentSchema(BaseModel):
    document_type: PersonalInfo = Field(..., description="The document type")
    contractDetails: Optional[List[ContractData]] = Field(
        None, description="Extracted contract details"
    )
    visaDetails: Optional[List[VisaData]] = Field(
        None, description="Extracted visa details"
    )
    residenceDetails: Optional[List[ResidenceData]] = Field(
        None, description="Extracted residence details"
    )
    changeStatusDetails: Optional[List[ChangeStatusData]] = Field(
        None, description="Extracted change status details"
    )
    healthcareDetails: Optional[List[HealthcareRegistrationData]] = Field(
        None, description="Extracted healthcare details"
    )
    passportDetails: Optional[List[PassportData]] = Field(
        None, description="Extracted passport details"
    )
