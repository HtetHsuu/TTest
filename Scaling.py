import requests, json

server_url = "http://172.17.193.78:8080/hapi-fhirstarters-simple-server"
headers = {'Content-Type': 'application/fhir+json'}

# --- Create Patient ---
patient_data = {
    "resourceType": "Patient",
    "name": [{"family": "Kim", "given": ["Siyul"]}],
    "gender": "female",
    "birthDate": "2000-01-01"
}

res = requests.post(f"{server_url}/Patient", data=json.dumps(patient_data), headers=headers)
patient_id = res.headers['Content-Location'].split("/")[-1]
print("Patient ID:", patient_id)

# --- Alcohol Consumption Observation ---
alcohol_obs = {
    "resourceType": "Observation",
    "status": "final",
    "category": [{"coding": [{"system": "http://terminology.hl7.org/CodeSystem/observation-category", "code": "social-history"}]}],
    "code": {"coding": [{"system": "http://loinc.org", "code": "74013-4", "display": "Alcohol use"}]},
    "subject": {"reference": f"Patient/{patient_id}"},
    "valueString": "Occasional"
}
requests.post(f"{server_url}/Observation", data=json.dumps(alcohol_obs), headers=headers)

# --- Sexual Activity Observation ---
sexual_obs = {
    "resourceType": "Observation",
    "status": "final",
    "code": {"coding": [{"system": "http://loinc.org", "code": "70294-6", "display": "Sexual activity"}]},
    "subject": {"reference": f"Patient/{patient_id}"},
    "valueString": "Active"
}
requests.post(f"{server_url}/Observation", data=json.dumps(sexual_obs), headers=headers)

# --- Medications ---
medication = {
    "resourceType": "MedicationStatement",
    "status": "active",
    "medicationCodeableConcept": {"text": "Ibuprofen 200mg"},
    "subject": {"reference": f"Patient/{patient_id}"}
}
requests.post(f"{server_url}/MedicationStatement", data=json.dumps(medication), headers=headers)

# --- Female Cycle Tracking Observation ---
cycle_obs = {
    "resourceType": "Observation",
    "status": "final",
    "code": {"coding": [{"system": "http://loinc.org", "code": "8665-2", "display": "Menstrual cycle"}]},
    "subject": {"reference": f"Patient/{patient_id}"},
    "valueString": "Last period: 2025-08-01"
}
requests.post(f"{server_url}/Observation", data=json.dumps(cycle_obs), headers=headers)

print("All health info successfully posted for Patient", patient_id)
