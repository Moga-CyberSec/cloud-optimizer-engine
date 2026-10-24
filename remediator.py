import boto3
import json
import os
from datetime import datetime

def execute_remediation(region_name="af-south-1", dry_run=True):
    """
    Reads audit findings and safely remediates waste:
    - Deletes unattached EBS volumes (if dry_run=False)
    - Logs all actions to remediation_log.json
    """
    ec2 = boto3.client('ec2', region_name=region_name)
    
    log = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "region": region_name,
        "mode": "DRY_RUN (Simulation)" if dry_run else "LIVE_EXECUTION",
        "actions_taken": [],
        "total_savings_usd_monthly": 0
    }

    audit_file = "audit_report.json"
    if not os.path.exists(audit_file):
        log["status"] = "ERROR"
        log["message"] = "No audit_report.json found. Run audit first."
        return log

    with open(audit_file, "r") as f:
        audit_data = json.load(f)

    unattached_volumes = audit_data.get("findings", {}).get("unattached_volumes", [])

    for vol in unattached_volumes:
        vol_id = vol.get("volume_id")
        est_loss = vol.get("estimated_monthly_loss_usd", 0)

        action_entry = {
            "resource_id": vol_id,
            "action": "DELETE_UNATTACHED_VOLUME",
            "monthly_savings_usd": est_loss,
            "status": "SIMULATED" if dry_run else "EXECUTED"
        }

        if not dry_run:
            try:
                ec2.delete_volume(VolumeId=vol_id)
                action_entry["status"] = "SUCCESS"
            except Exception as e:
                action_entry["status"] = "FAILED"
                action_entry["error"] = str(e)

        log["actions_taken"].append(action_entry)
        log["total_savings_usd_monthly"] += est_loss

    # Save log locally
    with open("remediation_log.json", "w") as f:
        json.dump(log, f, indent=4)

    return log

if __name__ == "__main__":
    result = execute_remediation(dry_run=True)
    print("Remediation execution complete:")
    print(json.dumps(result, indent=2))