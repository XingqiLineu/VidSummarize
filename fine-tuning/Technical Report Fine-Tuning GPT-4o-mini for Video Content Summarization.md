# Technical Report: Fine-Tuning GPT-4o-mini for Video Content Summarization

## 1. Background & Motivation

With the rapid growth of online video content, there is a pressing need for automated, high-quality summarization tools that can help users quickly understand and navigate long-form videos. This project aims to fine-tune a large language model (LLM) to generate structured summaries, extract key points, suggest relevant tags, and provide insights for YouTube videos, using both full transcripts and chapter segmentation.

---

## 2. Dataset Preparation

- **Source**: 20 videos from YouTube creator Ali Abdaal, covering a variety of topics in productivity, career, and personal development.
- **Transcription**: Used AssemblyAI or Whisper to obtain accurate, high-quality full-text transcripts from video audio.
- **Chapter Segmentation**: Leveraged automatic chaptering to extract time-stamped sections with descriptive titles.
- **Annotation**: For each video, manually created high-quality summaries, including:
  - Overall summary
  - Chapter-wise detailed summaries
  - Key points
  - Suggested tags
  - Insight or outlook

**Data Structure**:
- `full_text`: The complete transcript of the video.
- `auto_chapters`: Chapter breakdowns with time ranges and titles.
- `summary`: Structured summary as the target output.

---

## 3. Model Selection

- **Base Model**: OpenAI `gpt-4o-mini` (64k context window)
- **Rationale**:
  - Supports long and structured inputs, ideal for combining transcripts and chapters.
  - Cost-effective for experimentation.
  - Strong performance on summarization and reasoning tasks.
- **Platform**: OpenAI fine-tuning platform.

---

## 4. Fine-Tuning Setup

- **Data Split**:
  - First run: 18 training samples, 2 validation samples.
  - Second run: 16 training samples, 4 validation samples.
- **Hyperparameters**:
  - Batch size: 2
  - Epochs: 3 (first), 5 (second)
  - Learning rate multiplier: 1.8 (first), 1.0 (second)
  - Method: Supervised fine-tuning
  - Seed: Default

---

## 5. Hyperparameter Optimization & Iteration

### First Run
- **Settings**: 18:2 split, batch size 2, epochs 3, LR multiplier 1.8
- **Observation**:  
  - Training and validation loss decreased rapidly.
  - Token accuracy improved, but validation loss plateaued early.
  - Some instability in validation accuracy.

![fine_tuning_metrics_visualization](https://s2.loli.net/2025/04/19/bMHfEtXw4JQLqTW.png)

### Second Run
- **Settings**: 16:4 split, batch size 2, epochs 5, LR multiplier 1.0
- **Observation**:  
  - Smoother and more stable decrease in both training and validation loss.
  - Validation mean token accuracy improved and stabilized.
  - Reduced gap between training and validation metrics, indicating less overfitting and improved generalization.

![fine_tuning_metrics_visualization2](https://s2.loli.net/2025/04/19/xyKpY4ANjMriEho.png)

**Analysis**:  
The first run, with a higher learning rate and fewer epochs, led to a rapid decrease in loss but also to more fluctuation and less stable validation accuracy. The second run, with a lower learning rate and more epochs, resulted in smoother curves, higher and more stable validation accuracy, and better generalization. These results highlight the importance of careful hyperparameter tuning, especially with small datasets.

---

## 6. Model Evaluation

- **Metrics**: Validation loss and mean token accuracy were tracked during training.
- **Findings**:
  - The second run achieved better and more stable validation performance.
  - Both runs showed clear improvement over the initial baseline.
  - Validation accuracy and loss curves demonstrate effective learning and generalization.

---

## 7. Error Analysis

- **Qualitative Review**: Compared outputs from the base model and the fine-tuned model on held-out examples.
- **Findings**:
  - The fine-tuned model produced more structured, relevant, and insightful summaries.
  - Outputs better matched the desired format (chapter-wise summaries, key points, tags, insights).
  - Occasional minor hallucinations or missed details, especially on ambiguous or very long chapters.
- **Example**:  
  See attached files [`my_model.md`](my_model.md) and [`4o_mini.md`](4o_mini.md) for side-by-side output comparisons and detailed breakdowns.

---

## 8. Inference Pipeline

- **Interface**: Provided example scripts for API-based inference and comparison.
- **Usage**: The model can be accessed via the OpenAI Playground or API by specifying the fine-tuned model name.
- **Demonstration**: Included sample prompts and outputs in the repository for reproducibility.

---

## 9. Documentation & Reproducibility

- **Code and Data**: All scripts, configuration files, and data splits are included in the repository.
- **Environment**: See below for a list of required libraries.
- **Instructions**: The `README.md` provides setup and usage guidance.
- **Reproducibility**: All random seeds and hyperparameters are documented for experiment replication.

**Key Libraries Used** (see also [audio_extraction repo](https://github.com/XingqiLineu/audio_extraction)):

| Library       | Purpose                      |
| ------------- | ---------------------------- |
| openai        | LLM fine-tuning & inference  |
| assemblyai    | Audio transcription          |
| pandas        | Data processing              |
| csv           | Data processing              |
| tqdm          | Progress bars                |
| python-dotenv | Environment variable loading |

---

## 10. Limitations & Future Work

- **Small dataset**: Only 20 examples; increasing the dataset size would likely improve generalization and robustness.
- **Domain specificity**: The model is tuned to Ali Abdaal’s content style; broader testing is needed for other creators, topics, and video formats.
- **Potential for hallucination**: Occasional minor inaccuracies or hallucinations, especially in chapter summaries for ambiguous content.
- **Limited evaluation**: Current evaluation is based on loss and token accuracy; future work could include human evaluation and more granular metrics (e.g., ROUGE, BLEU).
- **Scalability and deployment**: Future work can explore larger models, more advanced fine-tuning techniques (e.g., DPO), and deployment as a public API or web tool.
- **Ethical considerations**: As with all LLM applications, care must be taken to avoid bias, respect creator rights, and ensure transparency in automated summarization.

---

## 11. References

- Ali Abdaal YouTube Channel
- OpenAI API Documentation
- AssemblyAI API Documentation

