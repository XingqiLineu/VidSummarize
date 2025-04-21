# Video Content Summarization: LLM Fine-Tuning Project

## Overview

This project fine-tunes a large language model (LLM) to perform high-quality summarization and analysis of YouTube video content. The goal is to enable the model to generate structured summaries, extract key points, suggest relevant tags, and provide insights for video transcripts with chapter segmentation.

---

## Dataset Preparation

- **Source**: 20 videos from YouTube creator Ali Abdaal, covering diverse topics.
- **Transcription**: Used AssemblyAI or Whisper to transcribe audio to high-quality text.
- **Chapters**: Extracted automatic chapter segmentation with time ranges and titles.
- **Annotation**: For each video, manually created structured summaries, including:
  - Overall summary
  - Chapter-wise detailed summaries
  - Key points
  - Suggested tags
  - Insight or outlook

---

## Model Selection

- **Base Model**: OpenAI `gpt-4o-mini` (64k context window)
- **Reason**: Cost-effective, strong performance on long and structured inputs.
- **Platform**: OpenAI official fine-tuning platform.

---

## Fine-Tuning Setup

- **Train/Validation Split**:
  - First run: 18 train, 2 validation
  - Second run: 16 train, 4 validation
- **Hyperparameters**:
  - Batch size: 2
  - Epochs: 3 (first), 5 (second)
  - Learning rate multiplier: 1.8 (first), 1.0 (second)
  - Method: Supervised fine-tuning

---

## Hyperparameter Optimization

- **Iteration 1**: Higher learning rate and fewer epochs for initial exploration.
- **Iteration 2**: Adjusted split, more epochs, and lower learning rate for stability.
- **Results**:
  - *First run*: Good overall improvement, but some instability (see loss/accuracy curves below).
    ![First run metrics][1]
  - *Second run*: Smoother training and validation curves, better validation accuracy.
    ![Second run metrics][2]

---

## Model Evaluation

- Evaluated using validation loss and mean token accuracy.
- Compared performance across different hyperparameter settings.
- Both training and validation accuracy improved, with reduced overfitting in the second run.

---

## Inference Pipeline

- Provided example scripts to compare outputs from the base and fine-tuned models.
- Inference can be performed via OpenAI Playground or API.

---

## Reproducibility

- All code, configuration, and data splits are included in this repository.
- See the technical report for setup and reproduction instructions.

---

*For more details, see the technical report and code in this repository.*
