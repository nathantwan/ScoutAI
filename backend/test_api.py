#!/usr/bin/env python3
"""
Comprehensive test script for ScoutAI FastAPI backend
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Make sure it's running on localhost:8000")
        return False

def test_model_status():
    """Test the model status endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/status")
        print(f"Model status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data}")
            return data.get('model_loaded', False)
        else:
            print(f"Error: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server")
        return False

def test_model_training():
    """Test model training"""
    try:
        print("Training model with 1000 samples...")
        response = requests.post(f"{BASE_URL}/api/v1/train-sync", params={"num_samples": 1000})
        print(f"Training: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Training completed!")
            print(f"Results: {data.get('results', {})}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server")
        return False

def test_recommendations():
    """Test the recommendations endpoint"""
    test_data = {
        "current_pick": 1,
        "current_round": 1,
        "user_roster": {
            "QB": [],
            "RB": [],
            "WR": [],
            "TE": [],
            "K": [],
            "DST": []
        },
        "available_players": [
            {
                "name": "Christian McCaffrey",
                "position": "RB",
                "team": "SF",
                "adp": 1.5,
                "projected_points": 280.5
            },
            {
                "name": "Tyreek Hill",
                "position": "WR",
                "team": "MIA",
                "adp": 3.2,
                "projected_points": 265.8
            },
            {
                "name": "Patrick Mahomes",
                "position": "QB",
                "team": "KC",
                "adp": 4.1,
                "projected_points": 320.2
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/suggest",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"Recommendations: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Got {len(result.get('recommendations', []))} recommendations")
            for i, rec in enumerate(result.get('recommendations', [])):
                print(f"  {i+1}. {rec['player']['name']} ({rec['player']['position']}) - {rec['confidence_score']:.1%} confidence")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server")
        return False

def test_model_info():
    """Test the model info endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/v1/model-info")
        print(f"Model info: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Model info: {data}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server")
        return False

def main():
    """Run all tests"""
    print("Testing ScoutAI FastAPI Backend")
    print("=" * 40)
    
    tests = [
        ("Health Check", test_health),
        ("Model Status", test_model_status),
        ("Model Training", test_model_training),
        ("Model Info", test_model_info),
        ("Recommendations", test_recommendations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            print("✅ PASSED")
            passed += 1
        else:
            print("❌ FAILED")
    
    print(f"\n{'=' * 40}")
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is ready.")
    else:
        print("⚠️  Some tests failed. Check the server logs.")

if __name__ == "__main__":
    main() 