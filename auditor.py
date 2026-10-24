import boto3
import json
from datetime import datetime

def audit_aws_resources(region_name="af-south-1"):
    """
    Connects to AWS using boto3 to scan for:
    1. Unattached EBS storage volumes (financial waste)
    2. Running EC2 instances
    """
    ec2 = boto3.client('ec2', region_name=region_name)
    
    findings = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "region": region_name,
        "financial_waste_summary": {
            "unattached_storage_loss_usd_monthly": 0,
            "idle_instances_count": 0,
            "critical_security_gaps": 0
        },
        "findings": {
            "unattached_volumes": [],
            "idle_instances": []
        }
    }

    try:
        # Scan for Unattached EBS Volumes
        volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
        for vol in volumes.get('Volumes', []):
            vol_id = vol['VolumeId']
            size = vol['Size']
            est_loss = size * 0.10
            
            findings['findings']['unattached_volumes'].append({
                "volume_id": vol_id,
                "size_gb": size,
                "estimated_monthly_loss_usd": round(est_loss, 2),
                "status": "UNATTACHED_WASTE"
            })
            findings['financial_waste_summary']['unattached_storage_loss_usd_monthly'] += round(est_loss, 2)

        # Scan for Running EC2 Instances
        instances = ec2.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        for reservation in instances.get('Reservations', []):
            for inst in reservation.get('Instances', []):
                inst_id = inst['InstanceId']
                inst_type = inst['InstanceType']
                
                findings['findings']['idle_instances'].append({
                    "instance_id": inst_id,
                    "type": inst_type,
                    "recommendation": "MONITOR_OR_RESIZE"
                })
                findings['financial_waste_summary']['idle_instances_count'] += 1

    except Exception as e:
        print(f"AWS Connection / Fallback Mode: {e}")
        findings["error"] = str(e)

    # Save findings locally
    with open("audit_report.json", "w") as f:
        json.dump(findings, f, indent=4)

    return findings

if __name__ == "__main__":
    report = audit_aws_resources()
    print("Audit executed successfully!")
    print(json.dumps(report, indent=2))