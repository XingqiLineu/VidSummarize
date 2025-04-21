import os
import asyncio
import assemblyai as aai
import csv

aai.settings.api_key = ""

AUDIO_DIR = 'audio/'
OUT_CSV = 'transcripts.csv'
FILE_COUNT = 20
MAX_CONCURRENT = 5

file_list = [f"audio_{i}.mp3" for i in range(1, FILE_COUNT + 1)]

async def transcribe_file(file_name, writer, lock):
    file_path = os.path.join(AUDIO_DIR, file_name)
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best, auto_chapters=True)
    try:
        transcript = transcriber.transcribe(file_path, config)
        while transcript.status not in [aai.TranscriptStatus.completed, aai.TranscriptStatus.error]:
            await asyncio.sleep(2)
            transcript = aai.Transcript.get_by_id(transcript.id)
        if transcript.status == aai.TranscriptStatus.error:
            print(f"转录失败 {file_name}: {transcript.error}")
            row = (file_name, "", "")
        else:
            chapters = []
            if transcript.chapters:
                for chapter in transcript.chapters:
                    chapters.append(f"{chapter.start}-{chapter.end}: {chapter.headline}")
            chapters_str = "\n".join(chapters)
            row = (file_name, transcript.text, chapters_str)
        # 写入CSV需加锁
        async with lock:
            writer.writerow(row)
    except Exception as e:
        print(f"处理 {file_name} 时出错: {e}")
        async with lock:
            writer.writerow((file_name, "", ""))

async def main():
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    lock = asyncio.Lock()
    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['file_name', 'full_text', 'auto_chapters'])
        tasks = [
            asyncio.create_task(
                sem_transcribe(f, writer, lock, semaphore)
            ) for f in file_list
        ]
        await asyncio.gather(*tasks)

async def sem_transcribe(file_name, writer, lock, semaphore):
    async with semaphore:
        await transcribe_file(file_name, writer, lock)

if __name__ == "__main__":
    asyncio.run(main())
    print(f"全部完成，结果已写入 {OUT_CSV}")
