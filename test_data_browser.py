#!/usr/bin/env python3
"""
Test script to verify all navbar and data browser endpoints are working correctly.
Run this after starting the Flask app: python app.py
Then in another terminal: python test_data_browser.py
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"
tests_passed = 0
tests_failed = 0


def test_endpoint(method, endpoint, expected_status=200, description=""):
    """Generic endpoint tester."""
    global tests_passed, tests_failed
    url = f"{BASE_URL}{endpoint}"
    print(f"\n🧪 Testing: {description or endpoint}")
    print(f"   URL: {url}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, timeout=5)
        else:
            print(f"   ❌ Unknown method: {method}")
            tests_failed += 1
            return
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == expected_status:
            print(f"   ✅ PASS")
            tests_passed += 1
            
            # Try to show JSON if available
            try:
                data = response.json()
                if isinstance(data, dict):
                    for key in list(data.keys())[:3]:  # Show first 3 keys
                        print(f"      - {key}: {type(data[key]).__name__}")
            except:
                pass
            
            return response
        else:
            print(f"   ❌ FAIL - Expected {expected_status}, got {response.status_code}")
            tests_failed += 1
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ FAIL - Connection refused. Is Flask running? (python app.py)")
        tests_failed += 1
    except Exception as e:
        print(f"   ❌ FAIL - {str(e)}")
        tests_failed += 1


def test_data_endpoints():
    """Test paginated data endpoints."""
    global tests_passed, tests_failed
    
    print("\n" + "="*60)
    print("📊 TESTING DATA ENDPOINTS")
    print("="*60)
    
    # Test Pan-India data
    resp = test_endpoint(
        "GET",
        "/api/data/pan-india?page=1&per_page=10",
        200,
        "Pan-India data (page 1, 10 rows)"
    )
    
    if resp and resp.status_code == 200:
        data = resp.json()
        print(f"      Total records: {data.get('total', 'N/A')}")
        print(f"      Current page: {data.get('page', 'N/A')}")
        print(f"      Per page: {data.get('per_page', 'N/A')}")
        if data.get('data'):
            print(f"      Sample row: {data['data'][0]}")
    
    # Test Bengaluru data
    resp = test_endpoint(
        "GET",
        "/api/data/bengaluru?page=1&per_page=10",
        200,
        "Bengaluru data (page 1, 10 rows)"
    )
    
    if resp and resp.status_code == 200:
        data = resp.json()
        print(f"      Total records: {data.get('total', 'N/A')}")
        print(f"      Current page: {data.get('page', 'N/A')}")
        print(f"      Per page: {data.get('per_page', 'N/A')}")
        if data.get('data'):
            print(f"      Sample row: {data['data'][0]}")
    
    # Test different page sizes
    test_endpoint(
        "GET",
        "/api/data/pan-india?page=1&per_page=50",
        200,
        "Pan-India data (50 rows per page)"
    )
    
    test_endpoint(
        "GET",
        "/api/data/bengaluru?page=2&per_page=25",
        200,
        "Bengaluru data (page 2, 25 rows)"
    )


def test_page_routes():
    """Test page routes."""
    global tests_passed, tests_failed
    
    print("\n" + "="*60)
    print("📄 TESTING PAGE ROUTES")
    print("="*60)
    
    test_endpoint("GET", "/", 200, "Home page (should redirect)")
    test_endpoint("GET", "/estimate", 200, "Estimate page")
    test_endpoint("GET", "/analytics", 200, "Analytics page")
    test_endpoint("GET", "/data", 200, "Data Browser page")
    test_endpoint("GET", "/karnataka/bengaluru", 200, "Bengaluru dedicated page")


def test_existing_endpoints():
    """Test existing endpoints to ensure they still work."""
    global tests_passed, tests_failed
    
    print("\n" + "="*60)
    print("🔄 TESTING EXISTING ENDPOINTS (Regression Check)")
    print("="*60)
    
    test_endpoint("GET", "/api/all/options", 200, "All options endpoint")
    test_endpoint("GET", "/api/bengaluru/options", 200, "Bengaluru options endpoint")
    test_endpoint("GET", "/api/analytics/pan/state_summary", 200, "Pan-India state summary")
    test_endpoint("GET", "/api/analytics/bengaluru/location_summary", 200, "Bengaluru location summary")


def main():
    """Run all tests."""
    global tests_passed, tests_failed
    
    print("\n" + "🚀 " * 20)
    print("HOUSE PRICE PREDICTION - DATA BROWSER & NAVBAR TEST SUITE")
    print("🚀 " * 20)
    
    try:
        # Quick connectivity test
        print("\n⏳ Checking Flask connectivity...")
        try:
            requests.get(f"{BASE_URL}/", timeout=2)
            print("✅ Flask app is running!")
        except:
            print("❌ Flask app is NOT running!")
            print("   Start it with: python app.py")
            return
        
        # Run all test groups
        test_page_routes()
        test_data_endpoints()
        test_existing_endpoints()
        
        # Summary
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        total = tests_passed + tests_failed
        print(f"✅ Passed: {tests_passed}/{total}")
        print(f"❌ Failed: {tests_failed}/{total}")
        
        if tests_failed == 0:
            print("\n🎉 ALL TESTS PASSED! Your data browser is ready to use.")
            print(f"   Visit: {BASE_URL}/ in your browser")
        else:
            print(f"\n⚠️  {tests_failed} test(s) failed. Check the output above.")
        
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")


if __name__ == "__main__":
    main()
