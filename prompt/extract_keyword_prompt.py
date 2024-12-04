EXTRACT_KEYWORD_PROMPT = (
    """
    # Instruction
    Read {user_message} and extract keywords that summarize the subject.
    
    # Constraints
    - If the original text is in Korean:
      - Extract keywords as they appear in the input, without translation.
      - Proper nouns should also remain unchanged.
    - If the original text is in foreign language:
      - Proper nouns (e.g., names of models, tools, libraries) must be output as they appear in the input, without translation.
      - Other general terms should be translated into Korean.
    - Ensure the number of keywords extracted is between 3 and 10.
    
    # Examples
    - For Korean input:
      User Message: 업무 효율화를 위한 카카오 사내봇 개발기...
      Output: 업무 효율화, 카카오 사내봇, 데이터, AI, LLM, RAG
    - For foreign language input:
      User Message: LoRA is a parameter-efficient method for fine-tuning large language models. LoRA fine-tunes RoBERTa models using PyTorch...
      Output: LoRA, 파라미터 효율적, 미세 조정, 대형 언어 모델, PyTorch, RoBERTa
    
    # Output Format
    - Output keywords as a comma-separated string, e.g., “keyword1, keyword2”. Do not use brackets or lists in the output.
    """
)
