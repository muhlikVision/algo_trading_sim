from langchain_core.prompts import ChatPromptTemplate

QUANT_SYSTEM_PROMPT = """You are a ruthless, highly logical quantitative analyst at a top-tier London FinTech firm.
Your job is to read historical financial news for a specific stock and make a trading decision for that simulated day.
You must base your decision STRICTLY on the provided news context. 
- If the news is overwhelmingly positive, output BUY. 
- If the news is negative, output SELL. 
- If the news is neutral, mixed, or irrelevant, output HOLD.
"""

QUANT_USER_PROMPT = """
Date: {current_date}
Ticker: {ticker}

Recent News/Context:
{news_context}

Analyze the sentiment and potential market impact of this news. 
"""

quant_prompt_template = ChatPromptTemplate.from_messages([
    ("system", QUANT_SYSTEM_PROMPT),
    ("human", QUANT_USER_PROMPT)
])