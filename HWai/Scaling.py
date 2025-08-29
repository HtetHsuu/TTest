import requests, json, random

BASE_URL = "http://172.17.193.78:8080/hapi-fhirstarters-simple-server/fhir"
headers = {"Content-Type": "application/fhir+json"}

names = [("Kim", "SiSi"), ("Lee", "JiJi"), ("Park", "WooWoo"), ("Choi", "MinMin")]

patient_ids = []
for family, given in names:
    patient = {
        "resourceType": "Patient",
        "name": [{"family": family, "given": [given]}],
        "gender": random.choice(["male", "female"]),
        "birthDate": f"{random.randint(1970, 2000)}-01-01"
    }
    r = requests.post(f"{BASE_URL}/Patient", headers=headers, data=json.dumps(patient))
    print("Patient:", r.status_code, r.text)
    if r.status_code == 201:
        patient_ids.append(r.json()["id"])

for pid in patient_ids:
    observation = {
        "resourceType": "Observation",
        "status": "final",
        "code": {"coding": [{"system": "http://loinc.org", "code": "8867-4", "display": "Heart rate"}]},
        "subject": {"reference": f"Patient/{pid}"},
        "valueQuantity": {"value": random.randint(60, 110), "unit": "beats/minute"}
    }
    r = requests.post(f"{BASE_URL}/Observation", headers=headers, data=json.dumps(observation))
    print("Observation:", r.status_code, r.text)
