#!/usr/bin/env python3
"""
Verify Graph RAG setup is complete and working.
Run this before starting the main server.
"""

import json
from pathlib import Path
import sys

def check_files():
    """Verify all required files exist."""
    print("📁 Checking files...")
    required = {
        "statutes/dv_act_section_3.txt": "Statute file",
        "statutes/payment_of_wages_section_5.txt": "Statute file",
        "data/statute_graph.json": "Statute relationship graph",
        "rag.py": "RAG system",
        "llm.py": "LLM integration",
        "config.py": "Configuration",
        "GRAPH_RAG_ARCHITECTURE.md": "Documentation",
    }
    
    all_good = True
    for file, description in required.items():
        if Path(file).exists():
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - {description}")
            all_good = False
    
    return all_good

def check_graph_structure():
    """Verify statute_graph.json has correct structure."""
    print("\n📊 Checking graph structure...")
    
    with open("data/statute_graph.json", "r") as f:
        graph = json.load(f)
    
    # Check main keys
    required_keys = ["statute_relationships", "domain_statute_map", "process_flows"]
    for key in required_keys:
        if key in graph:
            print(f"  ✅ {key}")
        else:
            print(f"  ❌ {key} - missing from graph")
            return False
    
    # Check statute nodes
    statutes = graph["statute_relationships"]
    print(f"\n  📝 Total statute nodes: {len(statutes)}")
    
    # Check relationships
    total_edges = sum(len(s.get("related", [])) for s in statutes.values())
    print(f"  🔗 Total relationships: {total_edges}")
    avg_degree = total_edges / len(statutes) if statutes else 0
    print(f"  📈 Average edges per node: {avg_degree:.1f}")
    
    # Verify all referenced statutes exist
    print("\n  Verifying referential integrity...")
    all_ids = set(statutes.keys())
    broken_refs = set()
    
    for stat_id, stat in statutes.items():
        for related_id in stat.get("related", []):
            if related_id not in all_ids:
                broken_refs.add(f"{stat_id} → {related_id}")
    
    if broken_refs:
        print(f"  ❌ Found broken references:")
        for ref in broken_refs:
            print(f"     {ref}")
        return False
    else:
        print(f"  ✅ All relationships are valid")
    
    # Check process flows
    print(f"\n  🛣️  Process flows: {len(graph.get('process_flows', {}))}")
    
    return True

def check_domains():
    """Verify domain coverage."""
    print("\n🎯 Checking domain coverage...")
    
    with open("data/statute_graph.json", "r") as f:
        graph = json.load(f)
    
    domains = graph.get("domain_statute_map", {})
    statutes = graph["statute_relationships"]
    
    for domain, statute_ids in domains.items():
        statutes_count = len(statute_ids)
        print(f"  ✅ {domain}: {statutes_count} statute(s)")
        
        # Verify all listed statutes exist
        for stat_id in statute_ids:
            if stat_id not in statutes:
                print(f"     ⚠️  Statute '{stat_id}' not found in relationships")
    
    return True

def check_graph_expansion():
    """Test graph expansion logic."""
    print("\n⚙️  Testing graph expansion logic...")
    
    with open("data/statute_graph.json", "r") as f:
        graph = json.load(f)
    
    statutes = graph["statute_relationships"]
    
    # Test 1: Simple expansion
    seed = "dv_act_section_3"
    if seed in statutes:
        related = statutes[seed].get("related", [])
        print(f"  ✅ Seed '{seed}' expands to {len(related)} related statutes")
    
    # Test 2: Multi-seed expansion
    seeds = ["dv_act_section_3", "ipc_section_498a"]
    expanded = set(seeds)
    for seed_id in seeds:
        if seed_id in statutes:
            expanded.update(statutes[seed_id].get("related", []))
    print(f"  ✅ Multi-seed expansion: {len(seeds)} seeds → {len(expanded)} total")
    
    # Test 3: Expansion ratio
    all_expansion_ratios = []
    for stat_id, stat in statutes.items():
        relations = len(stat.get("related", []))
        all_expansion_ratios.append(1 + relations)  # seed + related
    
    avg_ratio = sum(all_expansion_ratios) / len(all_expansion_ratios) if all_expansion_ratios else 1
    print(f"  ✅ Average expansion ratio: {avg_ratio:.1f}x")
    
    return True

def check_env():
    """Verify environment setup."""
    print("\n🔑 Checking environment setup...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("  ⚠️  .env file not found (copy from .env.example)")
        return False
    
    with open(".env", "r") as f:
        content = f.read()
    
    if "GEMINI_API_KEY" not in content:
        print("  ❌ GEMINI_API_KEY not in .env")
        return False
    
    # Check if it's the placeholder
    if "your_gemini_api_key_here" in content:
        print("  ⚠️  GEMINI_API_KEY is still placeholder (add your real key)")
        return False
    else:
        print("  ✅ GEMINI_API_KEY is set")
    
    return True

def main():
    """Run all checks."""
    print("=" * 60)
    print("🚀 LegalSaathi Graph RAG - Verification Checklist")
    print("=" * 60)
    
    checks = [
        ("Files", check_files),
        ("Graph Structure", check_graph_structure),
        ("Domain Coverage", check_domains),
        ("Graph Expansion", check_graph_expansion),
        ("Environment", check_env),
    ]
    
    all_passed = True
    for name, check_func in checks:
        try:
            result = check_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"  ❌ Error: {e}")
            all_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL CHECKS PASSED - System is ready!")
        print("\nYou can now run:")
        print("  python main.py")
        print("\nThen test with:")
        print("  python test_endpoints.py")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Copy .env.example to .env")
        print("  - Add your GEMINI_API_KEY to .env")
        print("  - Verify data/statute_graph.json exists")
        return 1

if __name__ == "__main__":
    sys.exit(main())
