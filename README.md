This repository provides translation rule data and related resources for fine-tuning Large Language Models (LLMs). The dataset is in Alpaca format and covers multiple language pairs.

rule data: Contains example translation rule data for multiple language pairs. Chinese ↔ Japanese: 1,000 rules each. Chinese ↔ English: 500 rules each. The data samples can serve as references and training resources for model fine-tuning.

test data: The test set used in this experiment.

ja_to_zh_rule_inverter: Generates Chinese → Japanese translation rules by inverting existing Japanese → Chinese translation rules. This process is implemented using the DeepSeek API.

en-zh-prompt: Instruction templates for generating English ↔ Chinese translation rules.


--------------------------------------------------------------------------------------
本仓库提供用于 大语言模型（LLMs）微调 的 翻译规则数据 及相关资源。数据集采用Alpaca格式，涵盖多种语言对。

rule data：收录多语言对的翻译规则示例数据。中文 ↔ 日文：各1,000条规则。中文 ↔ 英文：各500条规则。数据样例可作为模型微调的参考与训练资源。

test data：本次实验所使用的测试集。

ja_to_zh_rule_inverter：通过对已有的 日文 → 中文 翻译规则进行反向转换，生成 中文 → 日文 的翻译规则。该过程基于DeepSeek API实现。

en-zh-prompt：生成 英文 ↔ 中文 翻译规则的指令模板。

