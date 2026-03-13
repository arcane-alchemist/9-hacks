"""DLSA (District Legal Services Authority) database and lookup."""

import json
from pathlib import Path
from typing import Optional
from models import DLSAOffice


# Demo DLSA data for 22 Indian districts
DLSA_DATABASE = {
    "100001": {
        "district": "Delhi",
        "name": "District Legal Services Authority, Delhi",
        "address": "High Court of Delhi, New Delhi - 110003",
        "phone": "011-23739220",
        "timings": "Monday-Friday: 9:30 AM - 5:30 PM",
        "free": True
    },
    "400001": {
        "district": "Mumbai",
        "name": "District Legal Services Authority, Mumbai",
        "address": "High Court of Bombay, Mumbai - 400001",
        "phone": "022-22614617",
        "timings": "Monday-Friday: 9:00 AM - 5:30 PM",
        "free": True
    },
    "110001": {
        "district": "Delhi (Alt)",
        "name": "DLSA Delhi - Secondary Office",
        "address": "Tis Hazari Courts, Delhi - 110054",
        "phone": "011-23635001",
        "timings": "Monday-Friday: 9:30 AM - 5:00 PM",
        "free": True
    },
    "560001": {
        "district": "Bangalore",
        "name": "District Legal Services Authority, Bangalore",
        "address": "High Court of Karnataka, Bangalore - 560001",
        "phone": "080-22253039",
        "timings": "Monday-Friday: 9:30 AM - 5:00 PM",
        "free": True
    },
    "700001": {
        "district": "Kolkata",
        "name": "District Legal Services Authority, Kolkata",
        "address": "High Court of Calcutta, Kolkata - 700001",
        "phone": "033-22203039",
        "timings": "Monday-Friday: 9:00 AM - 5:30 PM",
        "free": True
    },
    "411001": {
        "district": "Pune",
        "name": "District Legal Services Authority, Pune",
        "address": "District Court, Pune - 411001",
        "phone": "020-26614200",
        "timings": "Monday-Friday: 9:30 AM - 5:00 PM",
        "free": True
    },
    "380001": {
        "district": "Ahmedabad",
        "name": "District Legal Services Authority, Ahmedabad",
        "address": "High Court of Gujarat, Ahmedabad - 380001",
        "phone": "079-27542100",
        "timings": "Monday-Friday: 9:30 AM - 5:30 PM",
        "free": True
    },
    "600001": {
        "district": "Chennai",
        "name": "District Legal Services Authority, Chennai",
        "address": "High Court of Madras, Chennai - 600001",
        "phone": "044-25367770",
        "timings": "Monday-Friday: 9:00 AM - 5:30 PM",
        "free": True
    },
    "500001": {
        "district": "Hyderabad",
        "name": "District Legal Services Authority, Hyderabad",
        "address": "High Court of Telangana, Hyderabad - 500001",
        "phone": "040-23553222",
        "timings": "Monday-Friday: 9:30 AM - 5:00 PM",
        "free": True
    },
    "360001": {
        "district": "Rajkot",
        "name": "District Legal Services Authority, Rajkot",
        "address": "District Court, Rajkot - 360001",
        "phone": "0281-2460500",
        "timings": "Monday-Friday: 9:30 AM - 5:00 PM",
        "free": True
    },
    "380005": {
        "district": "Vadodara",
        "name": "District Legal Services Authority, Vadodara",
        "address": "District Court, Vadodara - 380005",
        "phone": "0265-2451000",
        "timings": "Monday-Friday: 9:30 AM - 5:00 PM",
        "free": True
    },
    "700003": {
        "district": "Kolkata (Alt)",
        "name": "DLSA Kolkata - Secondary Office",
        "address": "District Court, Alipore, Kolkata - 700027",
        "phone": "033-24717888",
        "timings": "Monday-Friday: 9:00 AM - 5:30 PM",
        "free": True
    },
    "302001": {
        "district": "Jaipur",
        "name": "District Legal Services Authority, Jaipur",
        "address": "High Court of Rajasthan, Jaipur - 302001",
        "phone": "0141-2740100",
        "timings": "Monday-Friday: 9:30 AM - 5:00 PM",
        "free": True
    },
    "226001": {
        "district": "Lucknow",
        "name": "District Legal Services Authority, Lucknow",
        "address": "High Court of Allahabad, Lucknow - 226001",
        "phone": "0522-2414800",
        "timings": "Monday-Friday: 9:30 AM - 5:00 PM",
        "free": True
    },
    "411004": {
        "district": "Pune (Alt)",
        "name": "DLSA Pune - Secondary Office",
        "address": "Tehsil Office, Pune - 411004",
        "phone": "020-24205555",
        "timings": "Monday-Friday: 9:30 AM - 5:00 PM",
        "free": True
    },
    "682011": {
        "district": "Kochi",
        "name": "District Legal Services Authority, Kochi",
        "address": "High Court of Kerala, Kochi - 682011",
        "phone": "0484-2395100",
        "timings": "Monday-Friday: 9:00 AM - 5:30 PM",
        "free": True
    },
    "585101": {
        "district": "Belgaum",
        "name": "District Legal Services Authority, Belgaum",
        "address": "District Court, Belgaum - 585101",
        "phone": "0831-2200100",
        "timings": "Monday-Friday: 9:30 AM - 5:00 PM",
        "free": True
    },
    "400080": {
        "district": "Navi Mumbai",
        "name": "District Legal Services Authority, Navi Mumbai",
        "address": "District Court, Navi Mumbai - 400080",
        "phone": "022-27560200",
        "timings": "Monday-Friday: 9:30 AM - 5:00 PM",
        "free": True
    },
    "530001": {
        "district": "Visakhapatnam",
        "name": "District Legal Services Authority, Visakhapatnam",
        "address": "District Court, Visakhapatnam - 530001",
        "phone": "0891-2760100",
        "timings": "Monday-Friday: 9:30 AM - 5:00 PM",
        "free": True
    },
    "627001": {
        "district": "Tirunelveli",
        "name": "District Legal Services Authority, Tirunelveli",
        "address": "District Court, Tirunelveli - 627001",
        "phone": "0462-2330100",
        "timings": "Monday-Friday: 9:00 AM - 5:30 PM",
        "free": True
    },
    "143001": {
        "district": "Amritsar",
        "name": "District Legal Services Authority, Amritsar",
        "address": "Punjab & Haryana High Court (Chandigarh) - Regional Office",
        "phone": "0183-2223400",
        "timings": "Monday-Friday: 9:30 AM - 5:00 PM",
        "free": True
    },
    "342001": {
        "district": "Bikaner",
        "name": "District Legal Services Authority, Bikaner",
        "address": "District Court, Bikaner - 342001",
        "phone": "0151-2444100",
        "timings": "Monday-Friday: 9:30 AM - 5:00 PM",
        "free": True
    }
}


def get_dlsa_by_pincode(pincode: str) -> Optional[DLSAOffice]:
    """
    Get DLSA office details by pincode.
    
    Args:
        pincode: 6-digit pincode string
        
    Returns:
        DLSAOffice object if found, None otherwise
    """
    if pincode not in DLSA_DATABASE:
        return None
    
    data = DLSA_DATABASE[pincode]
    return DLSAOffice(
        name=data["name"],
        address=data["address"],
        phone=data["phone"],
        timings=data["timings"],
        free=data["free"]
    )


def get_dlsa_by_district(district_name: str) -> Optional[DLSAOffice]:
    """
    Get DLSA office details by district name (case-insensitive).
    
    Args:
        district_name: District name
        
    Returns:
        DLSAOffice object if found, None otherwise
    """
    district_lower = district_name.lower()
    
    for pincode, data in DLSA_DATABASE.items():
        if data["district"].lower() == district_lower:
            return DLSAOffice(
                name=data["name"],
                address=data["address"],
                phone=data["phone"],
                timings=data["timings"],
                free=data["free"]
            )
    
    return None


def list_all_districts() -> list[str]:
    """Get list of all available districts in database."""
    return list(set(data["district"] for data in DLSA_DATABASE.values()))
