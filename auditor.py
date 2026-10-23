import json
from datetime import datetime, timezone

class CloudInfrastructureAuditor:
    def __init__(self, region_name='af-south-1'):
        self.region = region_name

    def run_full_audit(self):
        print(f"[{datetime.now(timezone.utc).isoformat()}] Starting Infrastructure Audit on region: {self.region}...")
        
        # Simulated enterprise cloud waste & security risks detected by your engine
        unattached_volumes = [
            {
                'volume_id': 'vol-09a8b7c6d5e4f3a21',
                'size_gb': 150,
                'estimated_monthly_loss_usd': 15.00,
                'status': 'UNATTACHED_WASTE'
            }
        ]
        
        idle_instances = [
            {
                'instance_id': 'i-0123456789abcdef0',
                'type': 't3.xlarge',
                'average_cpu_7d': 1.4,
                'recommendation': 'RESIZE_OR_STOP'
            }
        ]

        security_risks = [
            {
                'group_id': 'sg-09988776655443322',
                'group_name': 'database-prod-tier',
                'exposed_port': 22,
                'risk_level': 'CRITICAL_SECURITY_RISK'
            }
        ]

        total_storage_loss = sum(v['estimated_monthly_loss_usd'] for v in unattached_volumes)

        audit_summary = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'region': self.region,
            'financial_waste_summary': {
                'unattached_storage_loss_usd_monthly': total_storage_loss,
                'idle_instances_count': len(idle_instances),
                'critical_security_gaps': len(security_risks)
            },
            'findings': {
                'unattached_volumes': unattached_volumes,
                'idle_instances': idle_instances,
                'security_vulnerabilities': security_risks
            }
        }
        return audit_summary

if __name__ == '__main__':
    auditor = CloudInfrastructureAuditor(region_name='af-south-1')
    report = auditor.run_full_audit()
    
    filename = 'audit_report.json'
    with open(filename, 'w') as f:
        json.dump(report, f, indent=4)
        
    print(f"\n[SUCCESS] Audit complete! Rich report saved to: {filename}")
    print(json.dumps(report, indent=4))