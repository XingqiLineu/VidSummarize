import csv
from openai import OpenAI

client = OpenAI(
    api_key="",  # ← 替换为你的DeepSeek API Key
    base_url="https://api.deepseek.com"
)

input_csv = "transcripts.csv"
output_csv = "transcripts_with_summary.csv"

def build_prompt(full_text, auto_chapters):
    return (
        "Given the following video transcript and its chapters, please:\n"
        "1. Summarize the entire video content in a concise paragraph.\n"
        "2. For each chapter (with start and end time in milliseconds and title), convert the time to mm:ss format and use it as the heading, then write a detailed summary for that chapter based on the transcript. The chapter summaries should be more detailed than the overall summary.\n"
        "3. Extract 3-5 key points from the whole video as bullet points.\n"
        "4. Suggest 3-5 suitable tags for the video (comma separated).\n"
        "5. Provide a short insight or outlook related to the video content.\n\n"
        "Chapters (format: start_ms-end_ms: title):\n"
        f"{auto_chapters}\n\n"
        "Video transcript:\n"
        f"{full_text}\n"
        "Please strictly follow this format in your response:\n"
        "Summary:\n"
        "(your summary here)\n"
        "Chapter Summaries:\n"
        "[mm:ss-mm:ss] Chapter title\n"
        "(detailed summary for this chapter)\n"
        "...\n"
        "Key Points:\n- point 1\n- point 2\n...\n"
        "Tags: tag1, tag2, tag3\n"
        "Insight/Outlook: (one sentence)"
    )

with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
     open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['summary']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for idx, row in enumerate(reader, 1):
        text = row['full_text']
        chapters_str = row['auto_chapters']
        prompt = build_prompt(text, chapters_str)
        print(f"Processing row {idx}...")

        try:
            response = client.chat.completions.create(
                model="deepseek-reasoner",
                messages=[
                    {"role": "system", "content": "You are a professional video content analyst, skilled at summarizing, extracting key points, and providing constructive insights."},
                    {"role": "user", "content": prompt}
                ],
                stream=False
            )
            summary = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error on row {idx}: {e}")
            summary = ""

        row['summary'] = summary
        writer.writerow(row)

print(f"All done! Results saved to {output_csv}")
