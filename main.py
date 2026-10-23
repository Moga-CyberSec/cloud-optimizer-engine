from fastapi import FastAPI
import json
import os
import uvicorn

app = FastAPI(
    title="Autonomous Cloud Infrastructure Auditor & Remediator API",
    description="REST API wrapper for automated AWS infrastructure auditing and remediation.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Cloud Optimizer Engine API",
        "version": "1.0.0"
    }

@app.post("/api/v1/audit")
def trigger_audit():
    audit_results = {}
    if os.path.exists("audit_report.json"):
        with open("audit_report.json", "r") as f:
            audit_results = json.load(f)
    return {
        "message": "Audit report loaded successfully.",
        "report": audit_results
    }

@app.post("/api/v1/remediate")
def trigger_remediation():
    remediation_results = {}
    if os.path.exists("remediation_log.json"):
        with open("remediation_log.json", "r") as f:
            remediation_results = json.load(f)
    return {
        "message": "Remediation log loaded successfully.",
        "log": remediation_results
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)