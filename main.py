from fastapi import FastAPI
import json
import os
import uvicorn
from auditor import audit_aws_resources
from remediator import execute_remediation

app = FastAPI(
    title="Autonomous Cloud Infrastructure Auditor & Remediator API",
    description="REST API wrapper for automated AWS infrastructure auditing and remediation.",
    version="1.2.0"
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Cloud Optimizer Engine API",
        "version": "1.2.0"
    }

@app.post("/api/v1/audit")
def trigger_audit():
    report = audit_aws_resources(region_name="af-south-1")
    return {
        "message": "Live AWS audit executed successfully.",
        "report": report
    }

@app.post("/api/v1/remediate")
def trigger_remediation(dry_run: bool = True):
    log = execute_remediation(region_name="af-south-1", dry_run=dry_run)
    return {
        "message": "Remediation engine executed successfully.",
        "log": log
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)