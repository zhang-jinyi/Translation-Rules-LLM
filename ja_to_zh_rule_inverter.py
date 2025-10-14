import json
from openai import OpenAI

# 配置 DeepSeek API
client = OpenAI(
    api_key="your_api-key",
    base_url="your_base-url"
)

# 读取 JSON 文件
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 调用 DeepSeek 接口生成文本
def generate_text(prompt):
    try:
        response = client.chat.completions.create(
            model="deepseek-r1",
            messages=[
                {"role": "system", "content": "你是一个资深语言学家，擅长中日互译，擅长分析日文和汉语之间的翻译规则。"},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=1.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        error_details = {
            'error_type': type(e).__name__,
            'error_message': str(e),
            'http_status': getattr(e, 'status_code', None),
            'response_content': e.response.text if hasattr(e, 'response') and e.response else ''
        }
        print(f"API请求失败，详细信息: {error_details}")
        return None

# 带重试机制的调用包装
def attempt_generate_with_retry(prompt, max_retries=3):
    last_result = None
    for attempt in range(1, max_retries + 1):
        result = generate_text(prompt)
        if result:
            last_result = result.strip()
            try:
                return json.loads(last_result), last_result  # 成功解析就返回
            except json.JSONDecodeError:
                print(f"⚠️ 第 {attempt} 次尝试失败：返回的内容不是合法 JSON。")
        else:
            print(f"⚠️ 第 {attempt} 次尝试失败：无返回或 API 错误。")
    return None, last_result  # 所有尝试都失败，返回最后一次的原始结果


# 实时处理并写入 JSON
def process_translation_rules(input_file, output_file, error_file, error_text_file):
    data = load_json(input_file)
    results = []        # 保存成功的条目
    error_items = []    # 保存失败的原始条目
    error_text = []     # 保存失败的返回内容或信息

    for idx, item in enumerate(data, 1):
        prompt = f"""
你是一名资深语言学家，擅长日文和中文互译。
我将提供给你一条日语到中文的翻译规则、一个日文句子（input）和它对应的中文翻译（output）。

请你完成以下任务：
1. 根据日->中的翻译规则，生成一条对应的**中文到日文**的新翻译规则，格式保持一致。
2. 将原有的中文句子作为新的 input（即原来的 output）。
3. 将原有的日语句子作为新的 output（即原来的 input），但是请在日语句子后，附加一句说明，格式如下：
   ##在翻译这个句子的时候，我们使用了{{新生成的中->日翻译规则}}翻译规则，以得到更好的翻译结果。##

最后，请直接以 JSON 格式输出，结构如下所示（注意：只输出 JSON 内容本身，前后不要添加多余的文字、标签、标点符号或者格式说明（如 "json", "code block" 等））:
{{
    "instruction": "翻译规则：以下是一条汉语翻译为日语的相关规则，请根据具体情况来进行参考。\n{{新生成的中->日翻译规则}}\n*例句：中文例句*\n生成的##XXX##表示对此翻译规则的确认\n现在请翻译以下内容为日语：",
    "input": "中文句子（原来的 output）",
    "output": "日语句子（原来的 input）+ ##在翻译这个句子的时候，我们使用了{{新生成的中->日翻译规则}}翻译规则，以得到更好的翻译结果。##"
}}

以下是提供的数据：
翻译规则（原规则，日->中）：
{item['instruction'].strip()}

日语输入句子（原 input）：
{item['input'].strip()}

中文输出句子（原 output）：
{item['output'].strip()}

请严格按照要求返回，确保格式合法。如果无法生成符合要求的 JSON，请不要返回任何内容。注意：只输出 JSON 内容本身，前后不要添加多余的文字、标签、标点符号或者格式说明（如 "json", "code block" 等）
"""

        generated, last_raw_text = attempt_generate_with_retry(prompt)

        if generated:
            results.append(generated)
            print(f"✅ 成功处理第 {idx} 条，已累计 {len(results)} 条")
        else:
            error_items.append(item)
            error_text.append(last_raw_text)
            print(f"❌ 第 {idx} 条多次尝试仍失败，已保存到错误列表。")

        # 每次都保存中间进度
        with open(output_file, 'w', encoding='utf-8') as f_out:
            json.dump(results, f_out, ensure_ascii=False, indent=4)

        with open(error_file, 'w', encoding='utf-8') as f_err:
            json.dump(error_items, f_err, ensure_ascii=False, indent=4)

        with open(error_text_file, 'w', encoding='utf-8') as f_err:
            json.dump(error_text, f_err, ensure_ascii=False, indent=4)

    print(
        f"\n全部处理完毕！✅ 成功: {len(results)} 条，失败: {len(error_items)} 条。数据已保存到：\n- {output_file}\n- {error_file}")

# 运行
input_json_path = "your_path"          # 输入文件
output_json_path = "your_path"      # 输出成功文件
error_file = "your_path"               # 保存失败的条目
error_text_file = "your_path"          # 保存错误内容文本
process_translation_rules(input_json_path, output_json_path, error_file, error_text_file)
