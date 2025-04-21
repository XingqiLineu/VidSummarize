import csv
import json

input_csv = "transcripts_with_summary.csv"
train_jsonl = "train2.jsonl"
valid_jsonl = "valid2.jsonl"

system_prompt = "You are a professional video content analyst, skilled at summarizing, extracting key points, and providing constructive insights."

def build_user_prompt(full_text, auto_chapters):
    return (
        "Below is a video transcript and its chapters.\n"
        "Please summarize the video, extract key points, suggest tags, and provide a short insight according to the chapters.\n\n"
        "Chapters:\n"
        f"{auto_chapters}\n\n"
        "Transcript:\n"
        f"{full_text}"
    )

# 读取csv
with open(input_csv, 'r', encoding='utf-8') as infile:
    reader = list(csv.DictReader(infile))

# 分割训练和验证集
train_rows = reader[:16]
valid_rows = reader[16:]

def write_jsonl(rows, out_path):
    with open(out_path, 'w', encoding='utf-8') as f:
        for row in rows:
            item = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": build_user_prompt(row['full_text'], row['auto_chapters'])},
                    {"role": "assistant", "content": row['summary']}
                ]
            }
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

write_jsonl(train_rows, train_jsonl)
write_jsonl(valid_rows, valid_jsonl)

print(f"Train set saved to {train_jsonl}")
print(f"Validation set saved to {valid_jsonl}")
