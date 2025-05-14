import json

jsonl_file = "slang_dataset_fixed.jsonl"
entries = []

try:
    with open(jsonl_file, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if line.strip():  # 빈 줄 무시
                item = json.loads(line.strip())
                if "input" not in item or "output" not in item:
                    raise ValueError(f"Invalid entry at line {i}: {item}")
                entries.append(item)
    print(f"Total entries: {len(entries)}")
    print("First 5 entries:")
    for i, item in enumerate(entries[:5], 1):
        print(f"Entry {i}: {item}")
    print("JSONL is valid!")
except json.JSONDecodeError as e:
    print(f"JSON parsing error at line {i}: {e}")
except Exception as e:
    print(f"Error: {e}")