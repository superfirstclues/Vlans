                 
VLAN Network Automation Project

Repository: https://gitlab.com/firstclues-group/vlans.git

Platform: GitLab
Lab Environment: Cisco DevNet Sandbox (IOS-XE)

1. Executive Summary

This project delivers a complete end-to-end VLAN automation solution using Python and Ansible against a live Cisco DevNet Sandbox IOS-XE device.

2. Project Goals (All Achieved)

✔ Automate VLAN creation
✔ Perform pre-deployment validation checks
✔ Configure trunk interfaces programmatically
✔ Verify VLAN state before and after deployment

3. Technical Architecture

Environment Components:

WSL Ubuntu 22.04

Python 3 (virtual environment)

Netmiko (SSH automation)

Ansible

Cisco DevNet Sandbox IOS-XE switch

Git-based repository hosted on GitLab

Automation Flow:

Inventory → SSH Connection → Validation → Deployment → Verification → User Automation → Documentation

4. File Structure & Purpose
Python Automation Scripts
File	Purpose
check_vlans.py	Baseline VLAN verification
auto_checks.py	Pre-deployment validation
auto.py	Core automation logic
auto_dynamic.py	Dynamic VLAN automation
auto_dynamic2.py	Extended dynamic logic
vlan_deploy.py	VLAN deployment execution
trunk.py	Trunk interface configuration
check_v.py	VLAN verification helper
Ansible Automation
File	Purpose
switch_users.yml	Switch user provisioning
windows_users.yml	Windows user automation (if required)
Inventory & Configuration
File	Purpose
inventory.ini	DevNet Sandbox device definition
test.ini	Testing inventory
inventory_access_closet1.txt	Device reference
requirements.txt	Python dependencies
5. Installation & Setup
sudo apt update
sudo apt install python3 python3-venv python3-pip -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt install ansible -y

6. Execution Order (Strict Demonstration Flow)

Follow this exact order in both testing and Panopto presentation.

STEP 1 – Baseline VLAN Check
python3 check_vlans.py

📸 Screenshot Required:

Terminal output showing existing VLAN list before changes.

Purpose:
Establish initial network state.

STEP 2 – Pre-Deployment Validation
python3 auto_checks.py

📸 Screenshot Required:

Successful SSH connection

Validation results

Purpose:
Confirms connectivity and configuration readiness.

STEP 3 – VLAN Deployment
python3 vlan_deploy.py

📸 Screenshot Required:

VLAN creation commands

Success confirmation output

Purpose:
Implements required VLAN configuration.

STEP 4 – Dynamic Automation
python3 auto_dynamic.py
python3 auto_dynamic2.py

📸 Screenshot Required:

Dynamic logic execution

Confirmation output

Purpose:
Demonstrates scalability and reusable automation logic.

STEP 5 – Trunk Configuration
python3 trunk.py

📸 Screenshot Required:

Trunk configuration commands

Interface trunk confirmation

Purpose:
Ensures VLAN traffic transport across interfaces.

STEP 6 – Post-Deployment Verification
python3 check_vlans.py

📸 Screenshot Required:

VLAN list showing newly created VLANs

Purpose:
Validates successful implementation.

STEP 7 – Ansible User Deployment
ansible-playbook -i inventory.ini switch_users.yml

📸 Screenshot Required:

Playbook execution summary

“changed” status confirmation

Purpose:
Automates switch user provisioning.

7. Required Screenshots Checklist

✔ Initial VLAN state
✔ Pre-check validation output
✔ VLAN deployment output
✔ Dynamic automation execution
✔ Trunk configuration confirmation
✔ Post-deployment VLAN verification
✔ Ansible playbook summary
✔ GitLab repository showing committed files
✔ inventory.ini file
✔ requirements.txt file
✔ Successful SSH connection to DevNet

Every execution stage must have visual proof in Panopto.

8. Panopto Presentation Structure

Slide 1 – Problem Statement
Manual VLAN configuration is inefficient and error-prone.

Slide 2 – Project Objective
Explain automation goals and Infrastructure-as-Code.

Slide 3 – Architecture Diagram
Show WSL → Python → Ansible → Cisco DevNet Sandbox → GitLab.

Slide 4 – Live Execution Demo
Run scripts in required order.
Explain each output clearly.

Slide 5 – Validation & Results
Show before/after VLAN state.

Slide 6 – Version Control
Show GitLab repository structure.

Slide 7 – Business Impact

Reduced configuration time

Increased consistency

Reduced human error

Scalable deployment model

Slide 8 – Conclusion
Project objectives met successfully.

9. Troubleshooting Guide
Problem	Resolution
SSH authentication failure	Verify DevNet credentials
Module import error	pip install -r requirements.txt
ansible-playbook not found	Install Ansible
Permission denied	Use sudo
Script fails	Check inventory.ini configuration
10. Final Outcome

This project successfully demonstrates:

✔ Real-world automation against Cisco DevNet Sandbox
✔ Full VLAN lifecycle management
✔ Dynamic configuration scripting
✔ Infrastructure-as-Code principles
✔ Hybrid Python + Ansible automation
✔ Proper validation before and after deployment
=======
# Vlans
Virtual network automation
>>>>>>> 2680d1e787d57fb3eab4a98c37c70c15b9729c70
