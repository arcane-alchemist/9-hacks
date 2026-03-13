import json
from main import app
from fastapi.testclient import TestClient

def run_test():
    try:
        client = TestClient(app)
        
        print("\n=== 1. Testing GET /health-questions/labour ===")
        response = client.get("/health-questions/labour")
        print(f"Status: {response.status_code}")
        questions_data = response.json()
        print(json.dumps(questions_data, indent=2))
        
        questions = questions_data.get("questions", [])
        
        print("\n=== 2. Testing POST /health-check ===")
        # Simulating a vulnerable agricultural/construction labourer scenario
        payload = {
            "domain": "labour",
            "answers": {
                questions[0]: "no",         # No written employment contract
                questions[1]: "yes",        # Paid in bank
                questions[2]: "no",         # No salary slips
                questions[3]: "not_sure",   # Working hours not clearly documented
                questions[4]: "no"          # Overtime not compensated nicely
            }
        }
        
        print(f"Submitting Payload:\n{json.dumps(payload, indent=2)}")
        
        response2 = client.post("/health-check", json=payload)
        print(f"\nStatus: {response2.status_code}")
        print(json.dumps(response2.json(), indent=2))

    except ImportError:
        print("httpx not installed to use TestClient. Testing internal function directly...")
        from health_analyzer import evaluate_health_check
        from health_questions import get_questions_for_domain
        q = get_questions_for_domain("labour")
        payload = {
            "domain": "labour",
            "answers": {
                q[0]: "no",
                q[1]: "yes",
                q[2]: "no",
                q[3]: "not_sure",
                q[4]: "no"
            }
        }
        res = evaluate_health_check("labour", payload["answers"])
        print(json.dumps(res, indent=2))
    except Exception as e:
         print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    run_test()
