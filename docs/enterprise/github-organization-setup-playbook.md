---
layout: default
title: "Enterprise GitHub Organization Setup Playbook"
description: "Comprehensive guide for transforming GitHub organizations into enterprise-ready environments"
nav_order: 1
parent: Enterprise Documentation
---

# Enterprise GitHub Organization Setup Playbook

> **Objective:** Transform your GitHub organization into an enterprise-ready environment ensuring security, compliance, scalability, and operational excellence for project deployments.

## Table of Contents

1. [Security Controls](#security-controls)
2. [Compliance Tasks](#compliance-tasks)
3. [Automation Setup](#automation-setup)
4. [Documentation Standards](#documentation-standards)
5. [Team and Role Management](#team-and-role-management)
6. [Release and Support Protocols](#release-and-support-protocols)
7. [Best Practices References](#best-practices-references)

---

## Security Controls

### 1. Organization-Level Security Settings

#### Two-Factor Authentication (2FA)
- **Action**: Enable 2FA requirement for all organization members
- **Implementation**:
  ```
  Settings → Organizations → [Your Org] → Security → Two-factor authentication
  ✓ Require two-factor authentication for everyone in the organization
  ```
- **Best Practice**: Provide guidance on setting up authenticator apps
- **Reference**: [GitHub 2FA Documentation](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa)

#### Single Sign-On (SSO) Integration
- **Action**: Configure SAML SSO for enterprise identity management
- **Implementation**:
  ```
  Settings → Organizations → [Your Org] → Security → SAML single sign-on
  ```
- **Supported Providers**: Azure AD, Okta, OneLogin, PingIdentity
- **Best Practice**: Test SSO with pilot group before full rollout

#### IP Allow Lists
- **Action**: Restrict access to approved IP ranges
- **Implementation**:
  ```
  Settings → Organizations → [Your Org] → Security → IP allow list
  ```
- **Best Practice**: Include office networks, VPN ranges, and CI/CD systems

### 2. Repository Security

#### Branch Protection Rules
**Implementation per repository**:
```yaml
# .github/branch-protection.yml
protection_rules:
  main:
    required_status_checks:
      strict: true
      contexts:
        - "ci/tests"
        - "security/codeql"
        - "security/dependency-check"
    enforce_admins: true
    required_pull_request_reviews:
      required_approving_review_count: 2
      dismiss_stale_reviews: true
      require_code_owner_reviews: true
      restrict_dismissals: true
    restrictions:
      users: []
      teams: ["security-team"]
    allow_force_pushes: false
    allow_deletions: false
```

#### CODEOWNERS Implementation
**Create `.github/CODEOWNERS`**:
```bash
# Global owners for all files
* @bakery-street-security-team

# Documentation
/docs/ @bakery-street-docs-team @bakery-street-security-team
/README.md @bakery-street-docs-team
/*.md @bakery-street-docs-team

# Infrastructure and CI/CD
/.github/ @bakery-street-devops-team @bakery-street-security-team
/docker/ @bakery-street-devops-team
/.gitlab-ci.yml @bakery-street-devops-team
/.github/workflows/ @bakery-street-devops-team @bakery-street-security-team

# Security-sensitive files
/SECURITY.md @bakery-street-security-team
/package.json @bakery-street-security-team @bakery-street-devops-team
/requirements.txt @bakery-street-security-team @bakery-street-devops-team
/Dockerfile @bakery-street-security-team @bakery-street-devops-team

# Source code by team
/src/api/ @bakery-street-backend-team
/src/frontend/ @bakery-street-frontend-team
/src/ml/ @bakery-street-ai-team
/tests/ @bakery-street-qa-team
```

#### Secret Scanning
- **Action**: Enable secret scanning for all repositories
- **Implementation**:
  ```
  Repository Settings → Security & analysis → Secret scanning
  ✓ Enable secret scanning
  ✓ Enable push protection
  ```
- **Custom Patterns**: Define organization-specific secret patterns
- **Alert Management**: Configure notification channels for security teams

#### Vulnerability Management
- **Dependabot Configuration** (`.github/dependabot.yml`):
```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
    reviewers:
      - "bakery-street-security-team"
    assignees:
      - "bakery-street-devops-team"
    commit-message:
      prefix: "security"
      include: "scope"
    
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "daily"
    reviewers:
      - "bakery-street-security-team"
    
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
```

#### Code Scanning with CodeQL
**GitHub Actions Workflow** (`.github/workflows/codeql.yml`):
```yaml
name: "CodeQL Security Analysis"

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 6 * * 1'  # Weekly Monday 6 AM

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    strategy:
      fail-fast: false
      matrix:
        language: [ 'javascript', 'python', 'java' ]

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v3
      with:
        languages: ${{ matrix.language }}
        queries: security-extended,security-and-quality

    - name: Autobuild
      uses: github/codeql-action/autobuild@v3

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
```

---

## Compliance Tasks

### 1. Audit Logging and Monitoring

#### Audit Log Streams
- **Action**: Configure audit log streaming to SIEM systems
- **Implementation**:
  ```
  Settings → Organizations → [Your Org] → Audit log → Streaming
  ```
- **Supported Destinations**: Splunk, Azure Monitor, Datadog, AWS CloudWatch
- **Retention**: Configure appropriate log retention policies

#### Activity Monitoring
**Monitoring Checklist**:
- [ ] Repository access and permissions changes
- [ ] Organization membership modifications
- [ ] Security setting changes
- [ ] Failed authentication attempts
- [ ] Unusual download patterns
- [ ] Administrative action tracking

### 2. Credential Rotation Policies

#### Personal Access Tokens (PATs)
- **Policy**: Mandatory rotation every 90 days
- **Implementation**: Use fine-grained personal access tokens
- **Monitoring**: Track token usage and expiration dates
- **Automation**: Alert system for expiring tokens

#### Deploy Keys and Secrets
- **Repository Secrets Rotation**:
  ```bash
  # Example rotation script
  gh secret set DATABASE_URL --repo org/repo --body "$NEW_DATABASE_URL"
  gh secret set API_KEY --repo org/repo --body "$NEW_API_KEY"
  ```
- **Schedule**: Quarterly rotation for production secrets
- **Documentation**: Maintain secret inventory and ownership

### 3. Data Protection and Privacy

#### Data Classification
- **Public Repositories**: No sensitive data
- **Private Repositories**: Internal business data
- **Internal Repositories**: Confidential information
- **Restricted**: Highly sensitive/regulated data

#### GDPR/Privacy Compliance
- **Data Retention**: Configure repository deletion policies
- **Right to be Forgotten**: Procedures for removing personal data
- **Data Processing**: Document data flows and processing activities

---

## Automation Setup

### 1. CI/CD Pipeline Standards

#### Required Workflow Elements
**Base CI Workflow** (`.github/workflows/ci.yml`):
```yaml
name: Continuous Integration

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  NODE_VERSION: '18'
  PYTHON_VERSION: '3.11'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Environment
      uses: actions/setup-node@v4
      with:
        node-version: ${{ env.NODE_VERSION }}
        cache: 'npm'
    
    - name: Install Dependencies
      run: npm ci
    
    - name: Run Linting
      run: npm run lint
    
    - name: Run Unit Tests
      run: npm run test:unit
    
    - name: Run Integration Tests
      run: npm run test:integration
    
    - name: Upload Coverage
      uses: codecov/codecov-action@v3
      with:
        token: ${{ secrets.CODECOV_TOKEN }}

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Run Security Audit
      run: npm audit --audit-level high
    
    - name: Dependency Check
      uses: dependency-check/Dependency-Check_Action@main
      with:
        project: 'bakery-street-project'
        path: '.'
        format: 'HTML,JSON'
    
    - name: Upload Results
      uses: actions/upload-artifact@v3
      with:
        name: dependency-check-report
        path: reports/

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Build Application
      run: npm run build
    
    - name: Build Docker Image
      run: docker build -t ${{ github.repository }}:${{ github.sha }} .
    
    - name: Push to Registry
      if: github.ref == 'refs/heads/main'
      run: |
        echo ${{ secrets.REGISTRY_PASSWORD }} | docker login -u ${{ secrets.REGISTRY_USERNAME }} --password-stdin
        docker push ${{ github.repository }}:${{ github.sha }}
```

### 2. Required Checks and Reviews

#### Pull Request Template
**Create `.github/pull_request_template.md`**:
```markdown
## Description
Brief description of changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Security Checklist
- [ ] No secrets or sensitive data exposed
- [ ] Dependencies reviewed for vulnerabilities
- [ ] Input validation implemented where applicable
- [ ] Authentication/authorization properly implemented

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Test coverage maintained/improved

## Documentation
- [ ] README updated (if applicable)
- [ ] API documentation updated (if applicable)
- [ ] Security documentation updated (if applicable)

## Deployment Notes
- [ ] Database migrations (if applicable)
- [ ] Environment variable changes (if applicable)
- [ ] Third-party service dependencies (if applicable)

## Reviewer Checklist
- [ ] Code follows project style guidelines
- [ ] Security review completed
- [ ] Performance impact assessed
- [ ] Documentation is adequate
```

### 3. Dependency Management

#### Automated Dependency Updates
- **Dependabot**: Configure for all package managers
- **Security Advisory**: Enable vulnerability alerts
- **Auto-merge**: Configure for patch updates only
- **Review Process**: Require manual review for major updates

#### License Compliance
```yaml
# .github/workflows/license-check.yml
name: License Compliance Check

on: [push, pull_request]

jobs:
  license-check:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    
    - name: Check Licenses
      uses: fossa-contrib/fossa-action@v2
      with:
        api-key: ${{ secrets.FOSSA_API_KEY }}
        
    - name: License Report
      run: |
        npx license-checker --onlyAllow 'MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause;ISC'
```

---

## Documentation Standards

### 1. Repository Documentation

#### Required Documentation Files
**Standard Repository Structure**:
```
├── README.md                 # Project overview and quick start
├── CONTRIBUTING.md           # Contribution guidelines
├── SECURITY.md              # Security policy and reporting
├── LICENSE                  # License information
├── CHANGELOG.md             # Version history
├── CODE_OF_CONDUCT.md       # Community guidelines
├── SUPPORT.md               # Support channels and resources
├── docs/
│   ├── architecture/        # System architecture
│   ├── api/                # API documentation
│   ├── deployment/         # Deployment guides
│   ├── development/        # Development setup
│   └── security/           # Security documentation
└── .github/
    ├── ISSUE_TEMPLATE/     # Issue templates
    ├── PULL_REQUEST_TEMPLATE.md
    ├── CODEOWNERS          # Code ownership
    └── workflows/          # CI/CD workflows
```

#### README.md Template
```markdown
# Project Name

Brief description of what this project does and who it's for.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker (optional)

### Installation
```bash
npm install
npm run build
npm start
```

## 📖 Documentation

- [API Documentation](docs/api/)
- [Architecture Guide](docs/architecture/)
- [Deployment Guide](docs/deployment/)
- [Contributing Guide](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)

## 🔒 Security

For security concerns, please review our [Security Policy](SECURITY.md) and report vulnerabilities privately.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- 📧 Email: security@organization.com
- 💬 Discussions: [GitHub Discussions](link)
- 🐛 Issues: [GitHub Issues](link)
```

### 2. Architecture Decision Records (ADRs)

#### ADR Template
**Create `docs/architecture/adr-template.md`**:
```markdown
# ADR-XXXX: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded]

## Context
What is the issue that we're seeing that is motivating this decision or change?

## Decision
What is the change that we're proposing or have agreed to implement?

## Consequences
What becomes easier or more difficult to do and any risks introduced by this change?

### Positive
- Benefit 1
- Benefit 2

### Negative  
- Risk 1
- Risk 2

### Neutral
- Change 1
- Change 2

## References
- [Link to relevant documentation]
- [Link to related ADRs]
```

### 3. API Documentation Standards

#### OpenAPI Specification
- **Standard**: Use OpenAPI 3.0+ for REST APIs
- **Tools**: Swagger/Redoc for documentation generation
- **Location**: Store in `docs/api/` directory
- **Validation**: Include API schema validation in CI

#### Code Documentation
- **Python**: Use Google-style docstrings
- **JavaScript**: Use JSDoc format
- **Java**: Use Javadoc format
- **Coverage**: Minimum 80% documentation coverage

---

## Team and Role Management

### 1. Organization-Level Roles

#### Role Hierarchy
```
Organization Owners (2-3 people maximum)
├── Security Team (Full security permissions)
├── DevOps Team (Actions, Pages, repository admin)
├── Engineering Teams
│   ├── Backend Team (Repository access)
│   ├── Frontend Team (Repository access)
│   └── QA Team (Repository access)
└── External Collaborators (Limited access)
```

#### Permission Matrix
| Role | Repository Admin | Security Settings | Member Management | Billing |
|------|------------------|-------------------|-------------------|---------|
| Owner | ✓ | ✓ | ✓ | ✓ |
| Security Team | ✓ | ✓ | - | - |
| DevOps Team | ✓ | Limited | - | - |
| Engineering Teams | Limited | - | - | - |
| External Collaborators | - | - | - | - |

### 2. Team Management Structure

#### Team Creation Strategy
```bash
# Create teams via GitHub API or CLI
gh api orgs/bakery-street-projct/teams -f name="security-team" -f description="Security and compliance team"
gh api orgs/bakery-street-projct/teams -f name="devops-team" -f description="DevOps and infrastructure team"
gh api orgs/bakery-street-projct/teams -f name="backend-team" -f description="Backend development team"
gh api orgs/bakery-street-projct/teams -f name="frontend-team" -f description="Frontend development team"
```

#### Team Synchronization
- **LDAP/AD Sync**: Configure team membership synchronization
- **SAML Group Mapping**: Map SAML groups to GitHub teams
- **Regular Audits**: Quarterly access reviews

### 3. Access Control Policies

#### Principle of Least Privilege
- **Repository Access**: Grant minimum necessary permissions
- **Time-limited Access**: Use temporary collaborators for contractors
- **Regular Reviews**: Monthly access audits
- **Automated Deprovisioning**: Remove access when employees leave

#### Guest Collaborator Management
```yaml
# Collaborator policy
guest_policy:
  max_duration: 90 days
  required_approvals: 2
  restricted_repos: 
    - production-systems
    - security-tools
  allowed_permissions:
    - read
    - triage
```

---

## Release and Support Protocols

### 1. Semantic Versioning

#### Version Format
```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILDMETADATA]

Examples:
- 1.0.0        # Initial release
- 1.1.0        # New features (backward compatible)
- 1.1.1        # Bug fixes
- 2.0.0        # Breaking changes
- 2.0.0-beta.1 # Pre-release
```

#### Automated Versioning
```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    branches: [ main ]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
        
    - name: Semantic Release
      uses: cycjimmy/semantic-release-action@v4
      with:
        semantic_version: 19
        extra_plugins: |
          @semantic-release/changelog
          @semantic-release/git
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### 2. Changelog Management

#### Automated Changelog Generation
**Configuration** (`.releaserc.json`):
```json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/changelog",
    "@semantic-release/npm",
    "@semantic-release/github",
    ["@semantic-release/git", {
      "assets": ["CHANGELOG.md", "package.json"],
      "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
    }]
  ]
}
```

#### Conventional Commits
```
feat: add new authentication method
fix: resolve memory leak in data processing
docs: update API documentation
style: fix code formatting
refactor: simplify user management logic
test: add integration tests for payment system
chore: update dependencies
```

### 3. Support and Incident Response

#### Support Channels
- **GitHub Issues**: Public bug reports and feature requests
- **GitHub Discussions**: Community questions and support
- **Security Email**: security@organization.com
- **Emergency Hotline**: For critical security issues

#### Incident Response Plan
```yaml
severity_levels:
  critical:
    description: "System down, security breach, data loss"
    response_time: "15 minutes"
    escalation: "Immediate"
    
  high:
    description: "Major feature broken, performance degraded"
    response_time: "2 hours"
    escalation: "4 hours"
    
  medium:
    description: "Minor feature issues, workaround available"
    response_time: "24 hours"
    escalation: "3 days"
    
  low:
    description: "Enhancement requests, documentation issues"
    response_time: "1 week"
    escalation: "2 weeks"
```

#### On-Call Procedures
- **Rotation Schedule**: Weekly rotations
- **Escalation Matrix**: Clear escalation paths
- **Runbooks**: Documented response procedures
- **Post-Incident Reviews**: Required for all critical incidents

---

## Best Practices References

### 1. GitHub Official Documentation
- [GitHub Enterprise Cloud Documentation](https://docs.github.com/en/enterprise-cloud@latest)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Managing Organizations](https://docs.github.com/en/organizations)
- [GitHub Actions Security](https://docs.github.com/en/actions/security-guides)

### 2. Security Frameworks
- **OWASP Top 10**: [Application Security Risks](https://owasp.org/www-project-top-ten/)
- **NIST Cybersecurity Framework**: [Framework Core](https://www.nist.gov/cyberframework)
- **CIS Controls**: [Critical Security Controls](https://www.cisecurity.org/controls)
- **SANS Security Policies**: [Policy Templates](https://www.sans.org/information-security-policy/)

### 3. Compliance Standards
- **SOC 2**: Service Organization Control 2
- **ISO 27001**: Information Security Management
- **GDPR**: General Data Protection Regulation
- **HIPAA**: Health Insurance Portability and Accountability Act
- **FedRAMP**: Federal Risk and Authorization Management Program

### 4. Industry Best Practices
- **SLSA Framework**: [Supply Chain Levels for Software Artifacts](https://slsa.dev/)
- **OpenSSF**: [Open Source Security Foundation](https://openssf.org/)
- **CNCF Security**: [Cloud Native Security](https://github.com/cncf/tag-security)
- **DevSecOps**: [OWASP DevSecOps Guideline](https://owasp.org/www-project-devsecops-guideline/)

### 5. Tools and Integrations
- **Security Tools**: Snyk, Veracode, Checkmarx, SonarQube
- **Monitoring**: Datadog, New Relic, Splunk, Elastic
- **Identity Management**: Okta, Azure AD, Auth0
- **Secrets Management**: HashiCorp Vault, AWS Secrets Manager, Azure Key Vault

---

## Implementation Checklist

Use the [Enterprise Readiness Checklist](enterprise-readiness-checklist.md) to track your organization's progress through these enterprise setup requirements.

---

*Last Updated: September 2024*
*Version: 1.0.0*
*Maintained by: Bakery Street Project Security Team*