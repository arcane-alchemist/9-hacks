"""Simple test script for JusticeAI endpoints."""

import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_health():
    """Test health check endpoint."""
    print_section("TEST 1: Health Check")
    response = requests.get(f"{BASE_URL}/")
    print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200

def test_query_hindi():
    """Test query endpoint with Hindi input (labour domain)."""
    print_section("TEST 2: Query - Hindi Labour Issue")
    
    payload = {
        "text": "Mera boss mujhe 3 mahine se salary nahi diya, kya karun?",
        "pincode": "110001",
        "situation_type": None
    }
    
    print(f"Request:\n{json.dumps(payload, indent=2)}\n")
    response = requests.post(f"{BASE_URL}/query", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Detected Language: {result['detected_language']}")
        print(f"Domain: {result['domain']}")
        print(f"Rights Summary (in user's language):\n{result['rights_summary']}\n")
        print(f"Cited Sections: {result['cited_sections']}")
        print(f"Action Steps:\n")
        for i, step in enumerate(result['action_steps'], 1):
            print(f"  {i}. {step}")
        print(f"\nDLSA Office: {result['dlsa_office']['name'] if result['dlsa_office'] else 'Not found'}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def test_query_english():
    """Test query endpoint with English input (DV domain)."""
    print_section("TEST 3: Query - English Domestic Violence Issue")
    
    payload = {
        "text": "My husband beats me and my children. What are my legal rights?",
        "pincode": "400001",
        "situation_type": None
    }
    
    print(f"Request:\n{json.dumps(payload, indent=2)}\n")
    response = requests.post(f"{BASE_URL}/query", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Detected Language: {result['detected_language']}")
        print(f"Domain: {result['domain']}")
        print(f"Letter Types: {result['letter_types']}")
        print(f"Complexity Flag: {result['complexity_flag']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def test_query_tamil():
    """Test query endpoint with Tamil input (RTI domain)."""
    print_section("TEST 4: Query - Tamil RTI Issue")
    
    payload = {
        "text": "எனது பெலவெறியு கட்டணம் பற்றிய தகவல் வேண்டும்",
        "pincode": None,
        "situation_type": "rti"
    }
    
    print(f"Request (Tamil text, RTI domain):\n{json.dumps(payload, indent=2)}\n")
    response = requests.post(f"{BASE_URL}/query", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Detected Language: {result['detected_language']}")
        print(f"Domain: {result['domain']}")
        print(f"Clarification Needed: {result['clarification_needed']}")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def test_generate_letter_labour():
    """Test letter generation - Labour complaint."""
    print_section("TEST 5: Generate Letter - Labour Complaint")
    
    payload = {
        "type": "labour_complaint",
        "user_name": "Raj Kumar Singh",
        "district": "Delhi",
        "date": "13-03-2026",
        "details": "My employer has not paid my salary for 3 months. I have submitted all documents but no payment received."
    }
    
    print(f"Request:\n{json.dumps(payload, indent=2)}\n")
    response = requests.post(f"{BASE_URL}/generate-letter", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Template Type: {result['template_type']}")
        print(f"\nLetter Content (first 500 chars):\n")
        print(result['letter_content'][:500])
        print("...")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def test_generate_letter_dv():
    """Test letter generation - DV protection order."""
    print_section("TEST 6: Generate Letter - DV Protection Order")
    
    payload = {
        "type": "dv_protection_order",
        "user_name": "Priya Sharma",
        "district": "Mumbai",
        "date": "13-03-2026",
        "details": "My husband physically abuses me and denies me access to household property. I fear for my safety and that of my children."
    }
    
    print(f"Request:\n{json.dumps(payload, indent=2)}\n")
    response = requests.post(f"{BASE_URL}/generate-letter", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"Template Type: {result['template_type']}")
        print(f"\nLetter Content (first 500 chars):\n")
        print(result['letter_content'][:500])
        print("...")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

def test_generate_letter_rti():
    """Test letter generation - RTI application."""
    print_section("TEST 7: Generate Letter - RTI Application")
    
    payload = {
        "type": "rti_application",
        "user_name": "Arun Patel",
        "district": "Bangalore",
        "date": "13-03-2026",
        "details": "Request for information on budget allocation for public health services in FY 2025-26"
    }
    
    response = requests.post(f"{BASE_URL}/generate-letter", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ RTI Application generated successfully")
        print(f"First 300 chars:\n{result['letter_content'][:300]}...")
    else:
        print(f"Error: {response.status_code}")

def test_dlsa_lookup():
    """Test DLSA office lookup."""
    print_section("TEST 8: DLSA Lookup - Multiple Pincodes")
    
    pincodes = ["110001", "400001", "560001", "600001", "999999"]
    
    for pincode in pincodes:
        response = requests.get(f"{BASE_URL}/dlsa/{pincode}")
        
        if response.status_code == 200:
            result = response.json()
            if result['found']:
                office = result['office']
                print(f"\n✓ Pincode {pincode}:")
                print(f"  Name: {office['name']}")
                print(f"  Phone: {office['phone']}")
            else:
                print(f"\n✗ Pincode {pincode}: {result['message']}")
        else:
            print(f"\n✗ Pincode {pincode}: Error {response.status_code}")

def test_invalid_request():
    """Test error handling."""
    print_section("TEST 9: Error Handling - Invalid Letter Type")
    
    payload = {
        "type": "invalid_letter_type",
        "user_name": "Test User",
        "district": "Delhi",
        "date": "13-03-2026",
        "details": "Test details"
    }
    
    response = requests.post(f"{BASE_URL}/generate-letter", json=payload)
    
    if response.status_code != 200:
        print(f"✓ Correctly returned error status: {response.status_code}")
        print(f"Error message: {response.json()['detail']}")
    else:
        print("✗ Should have returned error")

def main():
    """Run all tests."""
    print("\n🧪 JusticeAI Backend - Test Suite\n")
    
    try:
        test_health()
        sleep(1)
        
        # test_query_hindi()
        # sleep(2)
        
        test_query_english()
        sleep(2)
        
        # test_query_tamil()
        # sleep(2)
        
        test_generate_letter_labour()
        sleep(1)
        
        test_generate_letter_dv()
        sleep(1)
        
        test_generate_letter_rti()
        sleep(1)
        
        test_dlsa_lookup()
        sleep(1)
        
        test_invalid_request()
        
        print_section("✅ All Tests Complete!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("Make sure the server is running: python main.py")

if __name__ == "__main__":
    main()
