"""Letter generation module with pre-written templates."""

from datetime import datetime


def generate_labour_complaint(user_name: str, district: str, date: str, details: str) -> str:
    """Generate labour complaint letter to Labour Commissioner."""
    return f"""COMPLAINT TO THE LABOUR COMMISSIONER

Date: {date}
To,
The Labour Commissioner,
{district}

Name & Address of Complainant:
{user_name}

Subject: Formal Complaint for Violation of Payment of Wages Act, 1936

Dear Sir/Madam,

I, {user_name}, a resident of {district}, hereby lodge a formal complaint against my employer for violation of the Payment of Wages Act, 1936. 

Details of the violation:
{details}

Under Section 15 of the Payment of Wages Act, 1936, I am entitled to receive payment of wages within the prescribed time. The above actions constitute a clear violation of my legal rights.

I request you to take immediate action to investigate this matter and ensure my rightful dues are paid.

Yours faithfully,

{user_name}
Date: {date}

"""


def generate_rti_application(user_name: str, district: str, date: str, details: str) -> str:
    """Generate Right to Information (RTI) application."""
    return f"""REQUEST UNDER RIGHT TO INFORMATION ACT, 2005

Date: {date}
To,
The Public Information Officer / CPIO,
{district}

Name: {user_name}

Subject: Application under Section 6 of the Right to Information Act, 2005

Dear Sir/Madam,

Pursuant to Section 6 of the Right to Information Act, 2005, I, {user_name}, hereby request the following information from your office.

Information Requested:
{details}

I request this information to be provided within 30 days as per Section 7 of the RTI Act, 2005. If the information pertains to a third party, I understand that your office may extend the timeline by an additional 30 days.

I am willing to pay the prescribed fee for providing this information.

Yours faithfully,

{user_name}
Address: [To be filled by applicant]
Phone: [To be filled by applicant]
Date: {date}

"""


def generate_fir_draft(user_name: str, district: str, date: str, details: str) -> str:
    """Generate FIR (First Information Report) draft for filing at police station."""
    return f"""DRAFT FIRST INFORMATION REPORT (FIR)

To be filed at the nearest Police Station in {district}

Complainant Details:
Name: {user_name}
Address: [To be filled]
Phone: [To be filled]

Date of Report: {date}

DETAILS OF THE INCIDENT:

{details}

I hereby report the above incident and request the Police to register an FIR and initiate investigation under the applicable sections of the Indian Penal Code.

I am willing to cooperate fully with the police investigation and provide any additional information required.

Yours faithfully,

Signature: _______________
Name: {user_name}
Date: {date}

Note: This is a draft. Original report should be filed in person at the police station with any relevant evidence/documents and photographic identification.

"""


def generate_dv_protection_order(user_name: str, district: str, date: str, details: str) -> str:
    """Generate application for Domestic Violence Protection Order under DV Act Section 12."""
    return f"""APPLICATION FOR PROTECTION ORDER

Under Section 12 of the Protection of Women from Domestic Violence Act, 2005

Date: {date}
To,
The Magistrate,
{district} District Court

Applicant (Aggrieved Person):
Name: {user_name}
Address: [To be filled]

Subject: Application for Issuance of Protection Order

Respected Sir/Madam,

I, {user_name}, hereby apply for issuance of a Protection Order against [respondent name] under Section 12 of the Protection of Women from Domestic Violence Act, 2005.

Facts and Circumstances:
{details}

The above acts constitute domestic violence as defined under Section 3 of the Protection of Women from Domestic Violence Act, 2005.

I seek the following reliefs:
1. Protection Order to ensure my physical safety
2. Residence Order in my favor
3. Compensation for losses
4. Any other relief the court deems appropriate

I am aggrieved party and seek court's intervention for my safety and protection.

Yours faithfully,

Signature: _______________
Name: {user_name}
Date: {date}

Note: Legal aid is available. Contact the nearest District Legal Services Authority for free legal assistance.

"""


def generate_letter(letter_type: str, user_name: str, district: str, date: str, details: str) -> str:
    """
    Generate a letter template.
    
    Args:
        letter_type: One of 'labour_complaint', 'rti_application', 'fir_draft', 'dv_protection_order'
        user_name: Name of applicant
        district: District name
        date: Date in DD-MM-YYYY format
        details: Specific details to include
        
    Returns:
        Formatted letter as string
    """
    templates = {
        "labour_complaint": generate_labour_complaint,
        "rti_application": generate_rti_application,
        "fir_draft": generate_fir_draft,
        "dv_protection_order": generate_dv_protection_order,
    }
    
    if letter_type not in templates:
        raise ValueError(f"Invalid letter type: {letter_type}")
    
    return templates[letter_type](user_name, district, date, details)
