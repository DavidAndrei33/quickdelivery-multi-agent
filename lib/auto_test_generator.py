#!/usr/bin/env python3
"""
AUTO-TEST-GENERATOR - Generează test cases automate din bug-uri
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

BUGS_DIR = '/workspace/shared/bugs'
TEST_CASES_DIR = '/workspace/shared/tests/auto'

def generate_test_case_from_bug(bug_file):
    """Generează test case specific din bug report"""
    
    with open(bug_file, 'r') as f:
        content = f.read()
    
    # Extrage informații din bug
    bug_id = Path(bug_file).stem
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Unknown Bug"
    
    # Determină tipul de test necesar
    test_type = determine_test_type(content)
    
    # Generează test case
    test_case = {
        'id': f"TC-AUTO-{bug_id}",
        'title': f"Test: {title}",
        'bug_id': bug_id,
        'type': test_type,
        'generated_at': datetime.now().isoformat(),
        'status': 'pending',
        'steps': generate_steps(content, test_type),
        'expected_result': generate_expected(content),
        'automation_script': generate_script(content, test_type)
    }
    
    # Salvează test case
    os.makedirs(TEST_CASES_DIR, exist_ok=True)
    test_file = os.path.join(TEST_CASES_DIR, f"{test_case['id']}.json")
    
    with open(test_file, 'w') as f:
        json.dump(test_case, f, indent=2)
    
    return test_case

def determine_test_type(bug_content):
    """Determină tipul de test necesar"""
    content = bug_content.lower()
    
    if 'button' in content or 'click' in content:
        return 'ui_click_test'
    elif 'api' in content or 'endpoint' in content:
        return 'api_test'
    elif 'display' in content or 'visible' in content:
        return 'ui_visibility_test'
    elif 'log' in content or 'duplicate' in content:
        return 'data_integrity_test'
    elif 'price' in content or 'calculation' in content:
        return 'calculation_test'
    else:
        return 'general_test'

def generate_steps(bug_content, test_type):
    """Generează pașii testului"""
    
    # Extrage pașii reproducere din bug
    steps_match = re.search(r'## Pași Reproducere\s+(.+?)(?=##|$)', bug_content, re.DOTALL)
    if steps_match:
        steps_text = steps_match.group(1).strip()
        steps = [s.strip() for s in steps_text.split('\n') if s.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.'))]
        return steps
    
    # Default steps bazat pe tip
    default_steps = {
        'ui_click_test': [
            'Navigate to dashboard',
            'Select affected component',
            'Perform click action',
            'Verify response'
        ],
        'api_test': [
            'Send request to endpoint',
            'Verify response status',
            'Validate response data'
        ],
        'ui_visibility_test': [
            'Load dashboard',
            'Check element visibility',
            'Verify correct rendering'
        ]
    }
    
    return default_steps.get(test_type, ['Step 1', 'Step 2', 'Step 3'])

def generate_expected(bug_content):
    """Generează rezultatul așteptat"""
    expected_match = re.search(r'## Expected Result\s+(.+?)(?=##|$)', bug_content, re.DOTALL)
    if expected_match:
        return expected_match.group(1).strip()
    return "System should function correctly without errors"

def generate_script(bug_content, test_type):
    """Generează script automat de test"""
    
    scripts = {
        'ui_click_test': '''
async function test() {
    const element = await findElement('{selector}');
    await element.click();
    const result = await waitForResponse();
    assert(result.success === true);
}
''',
        'api_test': '''
async function test() {
    const response = await fetch('{endpoint}', {
        method: '{method}'
    });
    assert(response.status === 200);
    const data = await response.json();
    assert(data.status === 'success');
}
''',
        'ui_visibility_test': '''
async function test() {
    const element = await findElement('{selector}');
    assert(element.visible === true);
    assert(element.textContent !== '');
}
'''
    }
    
    return scripts.get(test_type, '// Generic test script')

def scan_and_generate():
    """Scanează bug-uri și generează test cases"""
    
    print("🧪 AUTO-TEST-GENERATOR - Scanning for bugs...")
    
    if not os.path.exists(BUGS_DIR):
        print("   No bugs directory found")
        return
    
    generated = 0
    
    for bug_file in os.listdir(BUGS_DIR):
        if not bug_file.endswith('.md'):
            continue
        
        bug_path = os.path.join(BUGS_DIR, bug_file)
        bug_id = Path(bug_file).stem
        
        # Verifică dacă există deja test case
        test_file = os.path.join(TEST_CASES_DIR, f"TC-AUTO-{bug_id}.json")
        if os.path.exists(test_file):
            continue
        
        # Generează test case nou
        try:
            test_case = generate_test_case_from_bug(bug_path)
            print(f"   ✅ Generated: {test_case['id']} ({test_case['type']})")
            generated += 1
        except Exception as e:
            print(f"   ❌ Error generating for {bug_id}: {e}")
    
    print(f"\n📊 Generated {generated} new test cases")

if __name__ == '__main__':
    scan_and_generate()
