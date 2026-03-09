"""
Zeal Code - Deployment Preparation (Phase 4)
Prepare for production deployment
"""

import os
import json
import shutil
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import time


@dataclass
class DeploymentConfig:
    """Deployment configuration"""
    environment: str  # development, staging, production
    version: str
    build_number: str
    deploy_date: float = field(default_factory=time.time)
    deployer: Optional[str] = None
    rollback_enabled: bool = False
    health_check_enabled: bool = True
    auto_scaling_enabled: bool = False


class DeploymentManager:
    """Manage deployment preparation and configuration"""

    def __init__(self, project_root: str):
        """
        Initialize deployment manager

        Args:
            project_root: Root directory of the project
        """
        self.project_root = project_root
        self.config_file = os.path.join(project_root, 'deployment', 'config.json')
        self.checklist_file = os.path.join(project_root, 'deployment', 'checklist.json')
        self.deployment_config: Optional[DeploymentConfig] = None
        self.checklist: Dict[str, bool] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load deployment configuration"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                data = json.load(f)
                self.deployment_config = DeploymentConfig(**data)

    def _save_config(self) -> None:
        """Save deployment configuration"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.deployment_config.__dict__, f, indent=2)

    def create_deployment_package(
        self,
        output_dir: str,
        environment: str = 'production'
    ) -> Tuple[bool, str, Optional[str]]:
        """
        Create deployment package

        Args:
            output_dir: Output directory for deployment package
            environment: Target environment

        Returns:
            (success, message, package_path)
        """
        try:
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)

            # Generate version and build number
            version = "1.0.0"
            build_number = f"build-{int(time.time())}"
            package_name = f"zeal-code-{version}-{build_number}.tar.gz"
            package_path = os.path.join(output_dir, package_name)

            # Create temporary directory for packaging
            import tempfile
            temp_dir = tempfile.mkdtemp()

            # Copy project files (excluding .git, __pycache__, etc.)
            exclude_dirs = {'.git', '__pycache__', '.pytest_cache', 'venv', 'env', '.venv', 'node_modules'}
            exclude_files = {'.DS_Store', '*.pyc', '*.pyo'}

            for item in os.listdir(self.project_root):
                item_path = os.path.join(self.project_root, item)
                temp_item_path = os.path.join(temp_dir, item)

                # Skip excluded directories
                if item in exclude_dirs or item.startswith('.'):
                    continue

                if os.path.isdir(item_path):
                    shutil.copytree(item_path, temp_item_path, ignore=shutil.ignore_patterns(*exclude_dirs))
                else:
                    shutil.copy2(item_path, temp_item_path)

            # Create package archive
            import tarfile
            package_name = f"zeal-code-{version}-{build_number}.tar.gz"
            package_path = os.path.join(output_dir, package_name)
                tar.add(temp_dir, arcname=os.path.basename(temp_dir))

            # Cleanup
            shutil.rmtree(temp_dir)

            # Update deployment config
            self.deployment_config = DeploymentConfig(
                environment=environment,
                version=version,
                build_number=build_number
            )
            self._save_config()

            return True, f"Deployment package created: {package_name}", package_path

        except Exception as e:
            return False, f"Failed to create deployment package: {str(e)}", None

    def generate_deployment_checklist(self) -> Dict[str, bool]:
        """Generate deployment checklist"""
        checklist = {
            # Code checks
            'code_quality_passed': False,
            'tests_passed': False,
            'code_coverage_adequate': False,
            'no_critical_bugs': False,
            'documentation_updated': False,

            # Configuration checks
            'environment_variables_configured': False,
            'database_migrations_run': False,
            'api_keys_configured': False,
            'secrets_managed': False,

            # Infrastructure checks
            'server_resources_adequate': False,
            'ssl_certificates_installed': False,
            'domain_dns_configured': False,
            'load_balancer_configured': False,
            'monitoring_setup': False,
            'logging_setup': False,
            'backup_system_configured': False,

            # Security checks
            'security_audit_passed': False,
            'vulnerability_scan_passed': False,
            'access_controls_configured': False,
            'rate_limiting_enabled': False,

            # Rollback checks
            'rollback_plan_in_place': False,
            'previous_version_backed_up': False,
            'database_backup_created': False
        }

        # Load existing checklist
        if os.path.exists(self.checklist_file):
            with open(self.checklist_file, 'r') as f:
                existing = json.load(f)
                for key, value in existing.items():
                    if key in checklist:
                        checklist[key] = value

        self.checklist = checklist
        self._save_checklist()
        return checklist

    def update_checklist_item(self, item: str, completed: bool = True) -> Tuple[bool, str]:
        """
        Update checklist item

        Args:
            item: Checklist item name
            completed: Completion status

        Returns:
            (success, message)
        """
        if item not in self.checklist:
            return False, f"Invalid checklist item: {item}"

        self.checklist[item] = completed
        self._save_checklist()
        return True, f"Checklist item '{item}' updated"

    def get_checklist_progress(self) -> Dict[str, Any]:
        """Get checklist progress"""
        total = len(self.checklist)
        completed = sum(1 for v in self.checklist.values() if v)
        incomplete = total - completed
        percentage = (completed / total * 100) if total > 0 else 0

        return {
            'total': total,
            'completed': completed,
            'incomplete': incomplete,
            'percentage': round(percentage, 2)
        }

    def generate_deployment_script(
        self,
        output_path: str,
        environment: str = 'production'
    ) -> Tuple[bool, str]:
        """
        Generate deployment script

        Args:
            output_path: Path for deployment script
            environment: Target environment

        Returns:
            (success, message)
        """
        try:
            script = f'''#!/bin/bash
# Zeal Code - Deployment Script
# Environment: {environment}
# Generated: {time.strftime("%Y-%m-%d %H:%M:%S")}

set -e  # Exit on error

echo "Starting deployment for environment: {environment}"

# Configuration
PROJECT_DIR="{self.project_root}"
DEPLOY_USER="deploy"
DEPLOY_HOST="zeal.example.com"
REMOTE_DIR="/var/www/zeal-code"
BACKUP_DIR="/var/backups/zeal-code"

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

log_info() {{
    echo -e "${{GREEN}}[INFO]${{NC}} $1"
}}

log_warn() {{
    echo -e "${{YELLOW}}[WARN]${{NC}} $1"
}}

log_error() {{
    echo -e "${{RED}}[ERROR]${{NC}} $1"
}}

# Pre-deployment checks
log_info "Running pre-deployment checks..."

if [ ! -f "deployment/checklist.json" ]; then
    log_error "Deployment checklist not found. Run: python3 -m deployment.prepare"
    exit 1
fi

# Check checklist status
CHECKLIST_STATUS=$(python3 -c "import json; f=open('deployment/checklist.json'); c=json.load(f); completed=sum(c.values()); total=len(c); print(f'{{completed}}/{{total}} ({completed/total*100:.0f}%)')")
log_info "Deployment checklist: $CHECKLIST_STATUS"

# Backup current deployment
log_info "Creating backup..."
ssh ${{DEPLOY_USER}}@${{DEPLOY_HOST}} "mkdir -p ${{BACKUP_DIR}} && tar -czf ${{BACKUP_DIR}}/backup-$(date +%Y%m%d-%H%M%S).tar.gz ${{REMOTE_DIR}}"

# Stop current deployment
log_info "Stopping current deployment..."
ssh ${{DEPLOY_USER}}@${{DEPLOY_HOST}} "cd ${{REMOTE_DIR}} && sudo systemctl stop zeal-code"

# Deploy new version
log_info "Deploying new version..."
scp deployment/*.tar.gz ${{DEPLOY_USER}}@${{DEPLOY_HOST}}:/tmp/
ssh ${{DEPLOY_USER}}@${{DEPLOY_HOST}} "mkdir -p /tmp/deploy && tar -xzf /tmp/*.tar.gz -C /tmp/deploy && rsync -av --delete /tmp/deploy/ ${{REMOTE_DIR}}/"

# Install dependencies
log_info "Installing dependencies..."
ssh ${{DEPLOY_USER}}@${{DEPLOY_HOST}} "cd ${{REMOTE_DIR}} && python3 -m pip install -r requirements.txt"

# Run database migrations
log_info "Running database migrations..."
ssh ${{DEPLOY_USER}}@${{DEPLOY_HOST}} "cd ${{REMOTE_DIR}} && python3 manage.py migrate"

# Restart service
log_info "Restarting service..."
ssh ${{DEPLOY_USER}}@${{DEPLOY_HOST}} "cd ${{REMOTE_DIR}} && sudo systemctl start zeal-code"

# Health check
log_info "Running health check..."
sleep 5
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    log_info "Health check passed!"
else
    log_error "Health check failed!"
    log_info "Rolling back..."
    ssh ${{DEPLOY_USER}}@${{DEPLOY_HOST}} "cd ${{REMOTE_DIR}} && sudo systemctl stop zeal-code && tar -xzf ${{BACKUP_DIR}}/backup-*.tar.gz -C ${{REMOTE_DIR}} && sudo systemctl start zeal-code"
    exit 1
fi

# Cleanup
log_info "Cleaning up..."
ssh ${{DEPLOY_USER}}@${{DEPLOY_HOST}} "rm -f /tmp/*.tar.gz && rm -rf /tmp/deploy"

log_info "Deployment completed successfully!"
'''

            with open(output_path, 'w') as f:
                f.write(script)

            # Make script executable
            os.chmod(output_path, 0o755)

            return True, f"Deployment script generated: {output_path}"

        except Exception as e:
            return False, f"Failed to generate deployment script: {str(e)}"

    def generate_docker_config(
        self,
        output_path: str
    ) -> Tuple[bool, str]:
        """
        Generate Docker configuration files

        Args:
            output_path: Path for Dockerfile

        Returns:
            (success, message)
        """
        try:
            dockerfile = '''FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["python3", "-m", "api", "run"]
'''

            docker_compose = '''version: '3.8'

services:
  zeal-code:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - LOG_LEVEL=info
      - WORKERS=4
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
'''

            # Write Dockerfile
            dockerfile_path = os.path.join(os.path.dirname(output_path), 'Dockerfile')
            with open(dockerfile_path, 'w') as f:
                f.write(dockerfile)

            # Write docker-compose.yml
            compose_path = os.path.join(os.path.dirname(output_path), 'docker-compose.yml')
            with open(compose_path, 'w') as f:
                f.write(docker_compose)

            return True, f"Docker configuration generated: Dockerfile, docker-compose.yml"

        except Exception as e:
            return False, f"Failed to generate Docker configuration: {str(e)}"

    def _save_checklist(self) -> None:
        """Save checklist to file"""
        os.makedirs(os.path.dirname(self.checklist_file), exist_ok=True)
        with open(self.checklist_file, 'w') as f:
            json.dump(self.checklist, f, indent=2)

    def get_deployment_config(self) -> Optional[DeploymentConfig]:
        """Get current deployment configuration"""
        return self.deployment_config

    def get_deployment_summary(self) -> Dict[str, Any]:
        """Get deployment summary"""
        checklist_progress = self.get_checklist_progress()

        return {
            'config': self.deployment_config.__dict__ if self.deployment_config else None,
            'checklist_progress': checklist_progress,
            'ready_for_deployment': checklist_progress['completed'] == checklist_progress['total']
        }


# Example usage
if __name__ == "__main__":
    manager = DeploymentManager('/home/ridzeal/.openclaw/workspace/projects/zeal-code')

    # Generate checklist
    checklist = manager.generate_deployment_checklist()
    print(f"Generated checklist with {len(checklist)} items")
    progress = manager.get_checklist_progress()
    print(f"Progress: {progress['completed']}/{progress['total']} ({progress['percentage']}%)")

    # Update checklist items
    success, message = manager.update_checklist_item('code_quality_passed', True)
    print(f"\nUpdate checklist: {success}, {message}")

    success, message = manager.update_checklist_item('tests_passed', True)
    print(f"Update checklist: {success}, {message}")

    # Check updated progress
    progress = manager.get_checklist_progress()
    print(f"Updated progress: {progress['completed']}/{progress['total']} ({progress['percentage']}%)")

    # Generate deployment script
    success, message = manager.generate_deployment_script('/tmp/deploy.sh')
    print(f"\nDeploy script: {success}, {message}")

    # Generate Docker config
    success, message = manager.generate_docker_config('/tmp/Dockerfile')
    print(f"Docker config: {success}, {message}")

    # Get deployment summary
    summary = manager.get_deployment_summary()
    print(f"\nDeployment summary:")
    print(json.dumps(summary, indent=2))
