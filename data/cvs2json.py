import json

input_file = "slang_dataset.jsonl"
output_file = "slang_dataset_fixed.jsonl"

# JSONL 읽고 수정
fixed_entries = []
with open(input_file, "r", encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        if line.strip():
            try:
                item = json.loads(line.strip())
                # ' output' → 'output' 수정
                if ' output' in item:
                    item['output'] = item.pop(' output')
                fixed_entries.append(item)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error at line {i}: {e}")
                continue

# 수정된 JSONL 저장
with open(output_file, "w", encoding="utf-8") as f:
    for item in fixed_entries:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Fixed {len(fixed_entries)} entries. Saved to {output_file}")