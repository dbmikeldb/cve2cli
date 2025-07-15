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

## Features

- Parses Vendor's advisories through their API to extract relevant vulnerability data.
- Outputs structured JSON with CLI checks and remediation commands.
- Designed to be vendor-agnostic and extensible to other network platforms. 
---

## Getting Started
### Access
- **web portal**: (coming soon)
- **REST API Endpoint**: (coming soon)

--- 

### Interested in contributing?
Please see CONTRIBUTING.md
