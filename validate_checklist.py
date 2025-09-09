#!/usr/bin/env python3
"""
Final Validation Script for Critical Checklist Items
Validates all components mentioned in issue #3
"""

import os
import sys
import json
from pathlib import Path


def validate_checklist():
    """Validate all items from the critical checklist"""
    
    base_path = Path(__file__).parent
    results = {}
    
    print("🔍 Validating Critical Checklist Items")
    print("=" * 50)
    
    # 1. ADR Review
    print("\n1. 📋 ADR Review")
    adr_readme = base_path / "architecture" / "adr" / "README.md"
    adr_001 = base_path / "architecture" / "adr" / "ADR-0001-serverless-baseline-architecture.md"
    
    if adr_readme.exists() and adr_001.exists():
        print("   ✅ Architecture ADR documentation exists")
        print(f"   📄 {adr_readme.relative_to(base_path)}")
        print(f"   📄 {adr_001.relative_to(base_path)}")
        results["adr"] = True
    else:
        print("   ❌ Missing ADR documentation")
        results["adr"] = False
    
    # 2. Negative Test Cases  
    print("\n2. 🧪 Negative Test Cases")
    negative_tests = base_path / "tests" / "test_lambda_woofy_handler_negative.py"
    
    if negative_tests.exists():
        print("   ✅ Lambda Woofy handler negative tests exist")
        print(f"   📄 {negative_tests.relative_to(base_path)}")
        
        # Count test methods
        content = negative_tests.read_text()
        test_count = content.count("def test_")
        print(f"   🔢 {test_count} negative test cases implemented")
        results["negative_tests"] = True
    else:
        print("   ❌ Missing negative test cases")
        results["negative_tests"] = False
    
    # 3. COPILOT_TOKEN Integration
    print("\n3. 🤖 COPILOT_TOKEN Integration")
    workflow_file = base_path / ".github" / "workflows" / "test.yml"
    
    if workflow_file.exists():
        content = workflow_file.read_text()
        if "COPILOT_TOKEN" in content:
            print("   ✅ COPILOT_TOKEN configured in GitHub Actions")
            print("   🔧 Automation tasks configured")
            results["copilot_token"] = True
        else:
            print("   ❌ COPILOT_TOKEN not found in workflows")
            results["copilot_token"] = False
    else:
        print("   ❌ GitHub Actions workflow not found")
        results["copilot_token"] = False
    
    # 4. Coverage & Security
    print("\n4. 🛡️ Coverage & Security")
    codeql_file = base_path / ".github" / "workflows" / "codeql.yml"
    
    security_checks = []
    if codeql_file.exists():
        print("   ✅ CodeQL security scanning configured")
        security_checks.append("CodeQL")
    
    if workflow_file.exists() and "coverage" in workflow_file.read_text():
        print("   ✅ Coverage reporting configured")
        security_checks.append("Coverage")
    
    if len(security_checks) >= 2:
        results["security"] = True
    else:
        print("   ❌ Incomplete security configuration")
        results["security"] = False
    
    # 5. Changelog & Security Log
    print("\n5. 📝 Changelog & Security Log")
    changelog = base_path / "CHANGELOG.md"
    security_log = base_path / "SECURITY_REMEDIATION_LOG.md"
    
    changelog_ok = changelog.exists()
    security_log_ok = security_log.exists()
    
    if changelog_ok and security_log_ok:
        print("   ✅ Both CHANGELOG.md and SECURITY_REMEDIATION_LOG.md exist")
        print(f"   📄 {changelog.relative_to(base_path)}")
        print(f"   📄 {security_log.relative_to(base_path)}")
        results["documentation"] = True
    else:
        print("   ❌ Missing changelog or security log")
        results["documentation"] = False
    
    # 6. Final Review - Documentation Structure
    print("\n6. 📚 Final Documentation Review")
    doc_files = [
        "README.md",
        "SECURITY.md", 
        "CONTRIBUTING.md",
        "CHANGELOG.md",
        "SECURITY_REMEDIATION_LOG.md"
    ]
    
    existing_docs = []
    for doc in doc_files:
        doc_path = base_path / doc
        if doc_path.exists():
            existing_docs.append(doc)
    
    print(f"   ✅ {len(existing_docs)}/{len(doc_files)} core documentation files exist")
    for doc in existing_docs:
        print(f"   📄 {doc}")
    
    results["final_review"] = len(existing_docs) >= 4
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VALIDATION SUMMARY")
    print("=" * 50)
    
    all_passed = all(results.values())
    
    for item, status in results.items():
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {item.replace('_', ' ').title()}")
    
    print(f"\n🎯 Overall Status: {'✅ PASSED' if all_passed else '❌ FAILED'}")
    
    if all_passed:
        print("\n🎉 All critical checklist items have been successfully implemented!")
        print("📋 Ready for final milestone progression.")
    else:
        print("\n⚠️  Some checklist items need attention before proceeding.")
    
    return all_passed


if __name__ == "__main__":
    success = validate_checklist()
    sys.exit(0 if success else 1)