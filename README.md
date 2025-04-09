# JuDGE: Benchmarking Judgment Document Generation for Chinese Legal System

📢 News: this work has been accepted at the SIGIR 2025!


## Overview

Welcome to the official GitHub repository for the **JuDGE** project!

In this repository, you'll find all resources related to the **JuDGE** dataset, including the following:

- The complete dataset and detailed documentation
- Implementations of multiple baseline methods and scripts to reproduce their results
- A one-click evaluation script for quickly assessing the quality of your generated legal documents






## Very Quick Start

1. **Environment Setup**  
   - First, follow the [environment setup instructions](https://github.com/oneal2000/JuDGE?tab=readme-ov-file#environment-setup) in this repository’s README.  

2. **Generate a Judgment Document**  
   - The file `data/text.json` is the test set. Each line is a dictionary with `text_id`, `text` (factual description section), and `fd` (full document).  
   - Your goal is to generate a complete legal document based on the `text` field (facts).  
   - For example, instruct an LLM:  
     > “Please generate a full legal document based on the following facts: [text].”

3. **Save Your Output**  
   - Store your generated document as a list of JSON objects, each with:  
     ```json
     {
       "id": "unique_case_identifier",
       "document": "full generated document text"
     }
     ```

4. **Evaluate**  
   - Assume your results are in `./your_results.json`. CD to the `evaluation` folder, then run:
     ```bash
     cd evaluation
     # Evaluate penalty accuracy, convicting accuracy, referencing accuracy
     python calc.py \
         --gen_file your_results.json \
         --exp_file ../expected.jsonl

     # Evaluate the reasoning and judgment sections
     python calc_rel.py \
         --gen_file your_results.json \
         --exp_file ../expected.jsonl
     ```
   - **Note:** Before running `calc_rel.py`, install NLTK’s WordNet:
     ```python
     import nltk
     nltk.download('wordnet')
     ```

5. **Check Your Environment**  
   - We provide a sample output file. Run the following script from the `evaluation` folder. If there are no errors, your environment is set up correctly:
     ```bash
     python calc.py \
         --gen_file ../Example_Output.jsonl \
         --exp_file ../expected.jsonl
     ```





### Repository Structure

- **data/**: Contains the dataset and relevant preprocessing scripts  
- **evaluation/**: Contains automated evaluation scripts and metrics for multi-dimensional assessment of generated legal documents 
- **prepare/**: Contains example preprocessing scripts and methods for splitting data  
- **retriever/**, **reranker/**: Code and examples for training retrieval and re-ranking models  
- **baseline_results/**,: This directory contains the generated judgments documents of all the baselines reported in our paper.
- **train/**,: This directory includes implementations of baseline approaches (e.g., in-context learning, fine-tuning, multi-source RAG) along with usage instructions.

### What You Can Do Here

1. **Access All Relevant Data**: Download and work with real-world case data, including external statutes and judgment documents.  
2. **Reproduce Baseline Results**: Easily replicate the performance of various baseline models on the JuDGE dataset using our provided scripts and instructions.  
3. **Evaluate Your Generated Legal Documents**: Prepare your generated texts, then use the scripts in the `evaluation/` directory for an automated, multi-dimensional assessment.

If you have any questions or want to contribute, feel free to open an issue or submit a pull request. We hope this repository proves helpful for your research and applications—happy exploring!

### Task Definition

Judgment Document Generation is formalized as a conditional text generation problem. Given an input fact description $$f \in \mathcal{F}$$, the goal is to generate a judgment document $$ \hat{j} \in \mathcal{J}$$ that is structurally coherent and legally sound:

$$ \mathcal{M} : \mathcal{F} \rightarrow \mathcal{J},$$

where $$\hat{j} = \mathcal{M}(f)$$ approximates the ground truth $j$ in terms of content, structure, and legal validity.

## Data Release

This section explains the dataset format, key fields, and where to find the data.

### **Dataset Files**

Our dataset consists of over **100,000** legal judgment documents. Due to the large file size (705.8MB), the full corpus is available at:
 [Google Drive: Full Corpus](https://drive.google.com/file/d/1x8HQ1l9yOjt5SFu-5n8kPuEXnqVca-LN/view?usp=sharing)



For ease of use, we provide a **high-quality subset** of judgment documents, which serves as both the training and test set:

- **High-Quality Subset:** [`data/all.json`](https://github.com/JuDGE/tree/main/data/all.json)



The dataset is split into separate **training** and **test** sets:

- **Training Set:** [`data/train.json`](https://github.com/JuDGE/tree/main/data/train.json)
- **Test Set:** [`data/test.json`](https://github.com/JuDGE/tree/main/data/test.json)



Additionally, we offer two **supplementary corpora** that provide external knowledge to enhance judgment document generation:

- **Legal Statutes Corpus:** [`data/law_corpus.jsonl`](https://github.com/JuDGE/tree/main/data/law_corpus.jsonl)

- **Case Corpus (Subset)**:

  `data/case_corpus.jsonl`

  - **Note:** `case_corpus.jsonl` is a subset; the full case corpus is available in the [Google Drive link above](https://drive.google.com/file/d/1x8HQ1l9yOjt5SFu-5n8kPuEXnqVca-LN/view?usp=sharing).




- **Data Structure:**
  Each judgment document is structured into a series of key-value pairs. The main fields include:

  - **CaseID:** Unique identifier for the case.
  - **Fact:** A section summarizing the key case facts (limited to 1,000 Chinese characters).
  - **Full Document:** Full Judgment Document.
  - **Reasoning:** Details of the legal reasoning process.
  - **Judgment:** The final decision and penalties (ranging from 1,000 to 3,000 Chinese characters).
  - **Sentence:** Duration of the prison sentence.
  - **Fine:** Monetary penalty imposed.
  - **Crime Type:** The type of crime involved.
  - **Law Articles:** Legal statutes’ indexes in penal codes cited in the judgment.

- **Example Entry:** 

  Below is a sample entry from `all.json`, showcasing the structure and data fields:

  ```json
  {
      "CaseId": "101305d2-00d3-443e-8f36-3843cbeb3379",
      "Fact": " 辉县市人民检察院指控，2018年5月21日1时许，被告人张新军醉酒后无证驾驶无号牌二轮摩托车，由西向东行驶至辉县市振新水泥厂门口时，与停在路南侧的豫G×××××、豫GCG＊＊挂号重型半挂牵引车尾部相撞，造成张新军受伤，车辆损坏的交通事故，被告人张新军负事故的主要责任... ",
      "Full Document": "河南省辉县市人民法院 刑事判决书 （2019）豫0782刑初325号 公诉机关河南省辉县市人民检察院。 被告人张新军，男，1984年3月12日出生于河南省，汉族，初中文化，农民，住新乡市。曾因犯抢劫罪，于2003年9月27日被新乡市北站区人民法院判处有期徒刑七年。因涉嫌犯危险驾驶罪，于2018年11月21日被辉县市公安局取保候审。经辉县市人民检察院决定，2019年6月25日被新乡市公安局耿黄分局执行取保候审。经本院决定，2019年6月29日被新乡市公安局耿黄分局执行取保候审...",
      "Reasoning": "本院认为，被告人张新军醉酒后无证驾驶机动车辆在道路上行驶，发生交通事故，负事故的主要责任，其行为已构成危险驾驶罪，应予惩处。被告人张新军到案后能如实供述自己的罪行，自愿认罪认罚，可从轻处罚。被告人张新军犯罪情节较轻，有悔罪表现，没有再犯罪的危险，可依法宣告缓刑。依照《中华人民共和国刑法》第一百三十三条之一第一款第（二）项，第六十七条第三款，第七十二条第一款、第三款，第七十三条第一款、第三款，第五十二条，第五十三条之规定，判决如下：",
      "Judgment": " 被告人张新军犯危险驾驶罪，判处拘役一个月，缓刑二个月，并处罚金人民币五千元。 （缓刑考验期限，从判决确定之日起计算。罚金限判决生效后五日内缴纳。） 如不服本判决，可在接到判决书的第二日起十日内，通过本院或直接向河南省新乡市中级人民法院提出上诉。书面上诉的，应当提交上诉状正本一份，副本两份。",
      "Sentence": [
          "拘役一个月"
      ],
      "Fine": [
          "罚金人民币五千元"
      ],
      "Crime Type": [
          "抢劫罪",
          "危险驾驶罪"
      ],
      "Law Articles": [
          67,
          133,
          72,
          73,
          52,
          53
      ]
  },
    
  Translated:
  {
      "CaseId": "101305d2-00d3-443e-8f36-3843cbeb3379",
      "Fact": "The Huixian City People's Procuratorate charged that on May 21, 2018, at around 1:00 AM, the defendant Zhang Xinjun, after being intoxicated, drove an unlicensed and unnumbered two-wheeled motorcycle from west to east. When reaching the entrance of Huixian City Zhenxin Cement Factory, he collided with the rear of a stationary heavy-duty semi-trailer truck (license plate: Yu G×××××, Yu GCG＊＊). This caused Zhang Xinjun to be injured and the vehicle to be damaged, with Zhang Xinjun bearing primary responsibility for the traffic accident...",
      "Full Document": "Henan Province Huixian City People's Court Criminal Judgment No. (2019) Yu 0782 Criminal Initial 325. Prosecuting authority: Huixian City People's Procuratorate. Defendant Zhang Xinjun, male, born March 12, 1984, in Henan Province, Han ethnicity, with a junior high school education, farmer, residing in Xinxiang City. He was previously convicted of robbery on September 27, 2003, by the Beizhan District People's Court in Xinxiang City, and sentenced to seven years in prison. He was granted bail pending trial by the Huixian City Public Security Bureau on November 21, 2018, on suspicion of committing the crime of dangerous driving. On June 25, 2019, he was released on bail by the Genghuang Branch of Xinxiang Public Security Bureau. On June 29, 2019, he was again granted bail by the same authority...",
      "Reasoning": "The court believes that the defendant Zhang Xinjun drove a motor vehicle without a license and while intoxicated on the road, causing a traffic accident for which he bears primary responsibility. His actions constitute the crime of dangerous driving and should be punished. After being apprehended, Zhang Xinjun confessed to his crime truthfully, voluntarily pleaded guilty, and can receive a reduced sentence. The defendant shows signs of remorse, has a low risk of reoffending, and may be sentenced to probation. Based on the provisions of Articles 133-1, 67-3, 72-1, 72-3, 73-1, 73-3, 52, and 53 of the Criminal Law of the People's Republic of China, the following judgment is made:",
      "Judgment": "The defendant Zhang Xinjun is found guilty of dangerous driving and sentenced to one month of detention with a two-month probation period, and fined RMB 5,000. (The probation period is calculated from the date the judgment is finalized. The fine must be paid within five days after the judgment becomes effective.) If dissatisfied with this judgment, the defendant may appeal within ten days after receiving the judgment, either through this court or directly to the Xinxiang City Intermediate People's Court in Henan Province. A written appeal must include one original and two copies of the appeal statement.",
      "Sentence": [
          "One month of detention"
      ],
      "Fine": [
          "RMB 5,000 fine"
      ],
      "Crime Type": [
          "Robbery",
          "Dangerous driving"
      ],
      "Law Articles": [
          67,
          133,
          72,
          73,
          52,
          53
      ]
  }
  ```

  Similarly, below is a sample entry from `law_corpus.jsonl`.

  ```json
  {
      "text_id": "1", 
      "text": "为了惩罚犯罪，保护人民，根据宪法，结合我国同犯罪作斗争的具体经验及实际情况，制定本法。",          
      "name": "中华人民共和国刑法第一条"
  }
    
  Translated:
  {
      "text_id": "1", 
      "text": "In order to punish crime and protect the people, based on the Constitution and in conjunction with the specific experiences and actual conditions of our country's fight against crime, this law is formulated.", 
      "name": "Article 1 of the Criminal Law of the People's Republic of China"
  }
  ```


## Automatic Evaluation

An automated evaluation framework is provided to assess the quality of generated judgment documents across multiple dimensions, including content accuracy, structural coherence, and legal soundness.

- **Evaluation Method:**
  The evaluation uses predefined metrics to compare the generated documents with the ground-truth texts, quantifying performance in terms of legal reasoning and text generation quality.
- **Implementation Details:**
  For more information on the evaluation process, refer to the evaluation Python codes and related documentation within this repository.

### Environment Setup

To get started, follow these steps to configure your environment:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/oneal2000/JuDGE.git
   cd JuDGE
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   Please note that installing these packages will only enable you to run the evaluation process successfully. If you want to run other parts, including *retriever*, *reranker*, and *baselines*, please refer to the relevant documentation in their respective folders.

### Running the Evaluation Script

To evaluate your generated judgment documents, follow these instructions:

1. **Prepare the Data:**
   Create two JSONL files where each line represents a case in the following format. One file contains ground truth documents, and the other consists of your generated judgment documents.

    ```json
   {
       "id": "unique_case_identifier",
       "document": "ground truth or generated document text"
   }
    ```

2. **Execute the Evaluation Python Code:**

   Before runing `calc_rel.py`, run the following code in your conda environment:
    ```python
    import nltk
    nltk.download('wordnet')
    ```

   ```bash
    cd evaluation
    # For Penalty Acc. Convicting Acc. Referencing Acc.
    python calc.py \
        --gen_file your_gen_file \
        --exp_file ground_truth_file


   # For Reasoning Section & Judgment Section
    python calc_rel.py \
        --gen_file your_gen_file \
        --exp_file ground_truth_file
   ```

   This requires you to specify the path to the input file and the location for the output results.
   
   **ground_truth_file** is released in `JuDGE/expected.jsonl`





## Necessary Preparations Before Reproduction

If you want to reproduce our baseline results, you need to transform the initial data into the appropriate format. This section is the first and necessary step.

To begin, simply execute:

```bash
cd prepare
./prep.sh
```

This script accomplishes the following:

1. Splits the initial data into two parts: **train** and **test** in a 4:1 ratio
2. Generates `case_corpus.json`, which will be encoded in the `retriever/sailer` section.
3. Generates `dense_train.json`, which is the training file for `retriever`
4. Generates `qrels_file` (test and train respectively), which will be used in the `retriever` and `reranker` sections to evaluate the quality of the retriever and reranker.

Please note that the execution order of the Python codes in this section cannot be reversed. This means that you should run the script `prep.sh` rather than running the codes separately unless you fully understand what the codes mean.

## Retriever & Reranker

This section is necessary if you want to reproduce the baseline results of the `multi-source rag` method. After successfully implementing this section, you will be able to retrieve the most relevant laws and case documents for any query. The main code for this section comes from:
- [Dense Retriever](https://github.com/luyug/Dense)
- [Reranker](https://github.com/luyug/Reranker)
    
Follow the instructions in their README respectively to configure the environments in this section.

- Demo code is provided in the `retriever` and `reranker` folders. You can follow these steps to get started quickly:

    ```bash
    cd retriever
    ./lr.sh
    ./sailer.sh
    cd ../reranker
    ./run.sh
    ```

- Once you have successfully completed the steps above, you can generate an M-RAG train file using the instructions below:

    ```bash
    cd src
    python gen_multi_train.py
    ```
    The generated train_file can be used to train your model and reproduce the `mrag` method baseline.

## Baselines Reproduction

- **LLM Training:**
  Guidelines for fine-tuning both general-purpose and legal-domain large language models, including specific parameter settings.

  - Qwen-series LLMs and Hanfei: The **qwen** template is sufficient to complete this section.
  - LexiLaw: You need to use the **chatglm** template to conduct training and deployment.

  You are supposed to use `data/train.json` to train LLMs.

- **Multi-source RAG:**
  A robust baseline that leverages multi-source retrieval-augmented generation by incorporating external knowledge from both statute and judgment document corpora.

  - You can still use the **qwen** template to train and deploy LLMs similar to methods in LLM training. The difference lies in the different training data.


## Baseline Results
If you have trouble reproducing our experiments step by step, you can simply use the result files we generated in our experiments. We have attached all the result files referenced in our paper. 
```bash
cd baseline_results
./run.sh
```
And you will get all the numbers.

## License

This project is licensed under [MIT License](https://github.com/oneal2000/JuDGE/blob/main/LICENSE). Please review the LICENSE file for more details.

## Citation

If you find the JuDGE dataset helpful for your research or are also working on document generation in the legal domain, we would sincerely appreciate it if you could cite our paper.

```
@misc{su2025judgebenchmarkingjudgmentdocument,
      title={JuDGE: Benchmarking Judgment Document Generation for Chinese Legal System}, 
      author={Weihang Su and Baoqing Yue and Qingyao Ai and Yiran Hu and Jiaqi Li and Changyue Wang and Kaiyuan Zhang and Yueyue Wu and Yiqun Liu},
      year={2025},
      eprint={2503.14258},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2503.14258}, 
}
```

## Contact

Document generation in the legal domain is still an evolving research area that requires further exploration. Our dataset represents an initial step in this direction, and we warmly welcome discussions with researchers interested in this field. 

If you have any questions, suggestions, or would like to discuss further, we would greatly appreciate it if you could open an issue on GitHub or reach out to us at oneal2000@126.com
