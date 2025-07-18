# cve2cli
**An open-source, vendor-agnostic database that translates CVE advisories into structured JSON mapping CVEs to both API endpoint and CLI configuration checks for network appliances.**

## Overview

`cve2cli` is an open-source project designed to bridge the gap between unstructured vulnerability advisories and automated network security validation workflows.

Many vendors publish CVE advisories without structured CLI or API configuration mappings, making it difficult to automate vulnerability checks and remediation across network estates. 

`cve2cli` parses these advisories and outputs **machine-readable JSON** that includes:
- CVE metadata (ID, description, affected platforms/versions)
- Potential CLI configuration commands to check for vulnerability exposure
- Recommended remediation commands
- References and links to official advisories

This enables NetDevOps teams to integrate vulnerability checks into CI/CD pipelines, automated remediation playbooks, and security dashboards.

---

## Feasability

The below table summarises the progress made to determine the feasiability of applying cve2cli for multiple Vendors. 

| Vendor    | Status | Description |
|-----------|--------|-------------|
| Cisco     |   🔴   | After Proof of Concept testing pulling data via Cisco's PSIRT OpenVuln API (both CVE and Advisory), it was realised that the information visible in the webpage is not matched 1:1 to the API, which leaves out critical information such as commands to run on the CLI. |
| Palo Alto | TBC    | TBC         |
| Juniper   | TBC    | TBC         |




## Getting Started
### Access
- **web portal**: (coming soon)
- **REST API Endpoint**: (coming soon)

--- 

### Interested in contributing?
Please see CONTRIBUTING.md
