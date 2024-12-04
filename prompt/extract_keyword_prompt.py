EXTRACT_KEYWORD_PROMPT = (
    """
    # Instruction
    Read {user_message} and extract keywords that summarize the subject.
    
    # Constraints
    - If the original text is in Korean:
      - Extract keywords as they appear in the original text, without translation.
      - Proper nouns should also remain unchanged.
    - If the original text is in English:
      - Proper nouns (e.g., names of models, tools, libraries) must be in English as they appear in the text.
      - Other general terms should be translated into Korean.
    - The number of keywords must be between 3 to 10.
    
    # Examples
    - For Korean input:
      User input: 업무 효율화를 위한 카카오 사내봇 개발기...
      Keywords: 업무 효율화, 카카오 사내봇, 데이터, AI
    - For English input:
      User input: LoRA is a parameter-efficient method for fine-tuning large language models...
      Keywords: LoRA, 파라미터 효율적, 미세 조정, 대형 언어 모델
    - Mixed output:
      User input: LoRA fine-tunes RoBERTa models using PyTorch...
      Keywords: LoRA, 미세 조정, RoBERTa, PyTorch
    
    # Output Format
    - Provide the keywords as a string separated by commas, similar to the examples above.
    """
)