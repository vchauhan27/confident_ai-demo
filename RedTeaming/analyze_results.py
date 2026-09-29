import json
import glob
import os

for file_path in glob.glob(r'd:\confident_ai-demo\RedTeaming\deepteam-results\*.json'):
    print(f"\n{'='*40}")
    print(f"File: {os.path.basename(file_path)}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    test_cases = data.get('test_cases', [])
    print(f"Total tests: {len(test_cases)}")

    passed = 0
    failed = 0
    aborted = 0

    for tc in test_cases:
        score = tc.get('score')
        if score == 1:
            passed += 1
        elif score == 0:
            failed += 1
        else:
            aborted += 1

    print(f"Passed (Mitigated): {passed}")
    print(f"Failed: {failed}")
    print(f"Aborted (Attacker Refused): {aborted}")
    if passed + failed > 0:
        print(f"Pass Rate: {passed/(passed+failed)*100:.2f}%")

    if failed > 0:
        print("\n--- FAILING TESTS ---")
        for tc in test_cases:
            score = tc.get('score')
            if score == 0:
                print(f"FAIL: {tc.get('vulnerability')} ({tc.get('vulnerability_type')}) via {tc.get('attack_method')}")
