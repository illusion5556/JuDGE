
# JuDGE: Benchmarking Judgment Document Generation for Chinese Law System

## Overview

Judgment Document Generation is formalized as a conditional text generation problem. Given an input fact description f∈Ff \in \mathcal{F}, the goal is to generate a judgment document j^∈J\hat{j} \in \mathcal{J} that is structurally coherent and legally sound:

$M:F→J,\mathcal{M} : \mathcal{F} \rightarrow \mathcal{J},$

where $$j^=M(f)\hat{j} = \mathcal{M}(f)$$approximates the ground truth jj in terms of content, structure, and legal validity.

## Data Release

This section explains the dataset format, key fields, and where to find the data.

-   **Data Structure:**
    Each judgment document is structured into a series of key-value pairs. The main fields include:
    -   **CaseID:** Unique identifier for the case.
    -   **Fact:** A section summarizing the key case facts (limited to 1,000 Chinese characters).
	-   **Full Document:** Full Judgment Document.
    -   **Reasoning:** Details of the legal reasoning process.
    -   **Judgment:** The final decision and penalties (ranging from 1,000 to 3,000 Chinese characters).
    -   **Sentence:** Duration of the prison sentence.
    -   **Fine:** Monetary penalty imposed.
    -   **Crime Type:** The type of crime involved.
    -   **Law Articles:** Legal statutes' indexes in penalcodes cited in the judgment.

**Example Entry:** Below is a sample entry from `all.json`, showcasing the structure and data fields:

```
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

这里再展示几条真实的 json 格式的数据，可以参考 stard，同时放中文和英文

Corpus 同理（我后续会再给你一些文书）

-   **Data Availability:**
    Detailed information on file formats and data locations can be found in the [Data Release](https://chatgpt.com/c/DATA_RELEASE.md) document.

## Automatic Evaluation

An automated evaluation framework is provided to assess the quality of generated judgment documents across multiple dimensions including content accuracy, structural coherence, and legal soundness.

-   **Evaluation Method:**
    The evaluation uses predefined metrics to compare the generated documents with the ground-truth texts, quantifying the performance in terms of legal reasoning and text generation quality.
-   **Implementation Details:**
    For more information on the evaluation process, refer to the evaluation scripts and related documentation within this repository.

## Environment Setup

To get started, follow these steps to configure your environment:

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/your_username/JuDGE.git
    cd JuDGE
    ```

2. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **System Requirements:**
   Ensure that your system meets the required Python version and, if applicable, CUDA requirements for GPU acceleration. For further details, see [CONFIG.md](https://chatgpt.com/c/CONFIG.md).

这里是一个例子，我们在这里教他们怎么配置环境就行了

## Running the Evaluation Script

To evaluate your generated judgment documents, follow these instructions:

1. **Prepare the Data:**
   Create a JSONL file where each line represents a case in the following format:

    ```json
    {
        "id": "unique_case_identifier",
        "document": "generated judgment document text"
    }
    ```

2. **Execute the Evaluation Script:**

    ```bash
    sh eval.sh
    ```

    The script requires you to specify the path to the input file and the location for the output results. Detailed instructions are provided within the script.

这里写一下，eval.sh 的各个超参

## Baselines Reproduction

This section details the process for reproducing the baseline methods, which include:

-   **Retriever Training:**
    Instructions for preparing the training data, configuring the model, and executing training commands for the retrieval module.
-   **LLM Training:**
    Guidelines for fine-tuning both general-purpose and legal-domain large language models, including specific parameter settings.
-   **Multi-source RAG:**
    A robust baseline that leverages multi-source retrieval-augmented generation by incorporating external knowledge from both statute and judgment document corpora.

For a comprehensive guide on reproducing the baselines, please refer to the [Baselines Documentation](https://chatgpt.com/c/docs/baselines.md).

## License

This project is licensed under [LICENSE_NAME](https://chatgpt.com/c/LICENSE). Please review the LICENSE file for more details.

## Citation

If you use the JuDGE dataset in your research, please cite our paper:

```
[Add your citation details here]
```

## Contact

For questions or suggestions, please open an issue on GitHub or contact us at [your_email@example.com](mailto:your_email@example.com).
