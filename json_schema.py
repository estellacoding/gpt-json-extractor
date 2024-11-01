# json_schema.py

from openai import OpenAI, OpenAIError
from pydantic import ValidationError
from models import UserData
from typing import Optional, Union
import os
from dotenv import load_dotenv
import json
from validate_format import validate_email_format

# 加載 .env 文件，以便讀取環境變數中的 API 金鑰
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# 初始化 OpenAI 客戶端
client = OpenAI(api_key=OPENAI_API_KEY)

def json_schema_response(user_input: str, memory: list) -> Union[Optional[UserData], str]:
    """
    使用 OpenAI 的 Json_Schema 方法提取使用者資料。

    參數:
        user_input (str): 使用者輸入的文字。
        memory (list): 對話記憶，用於存儲對話歷史。

    返回:
        Optional[UserData]: 如果成功提取資料，返回 UserData 實例；若電子郵件格式無效，返回特定錯誤訊息。
    """
    try:
        # 建立 OpenAI API 的請求，設置模型和調用參數
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0,
            # 定義json schema
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "extract_user_data",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string", "description": "使用者的姓名"},
                            "email": {"type": "string", "description": "使用者的電子郵件"},
                            "phone": {"type": "string", "description": "使用者的電話號碼"}
                        },
                        "required": ["name", "email", "phone"],
                        "additionalProperties": False
                    }
                }
            }
        )

        # 獲取 API 回應中的訊息
        message = response.choices[0].message
        print("Response Message:", message)

        if message.content:
            # 將 JSON 格式的回應內容解析為字典
            response_data = json.loads(message.content)

            # 驗證電子郵件格式，若無效則返回錯誤訊息
            if not validate_email_format(response_data):
                return "Email format validation failed."  # 返回特定的錯誤訊息
            
            try:
                # 將結果轉換為 UserData 實例
                user_data = UserData(**response_data)
                # 將LLM回應添加到對話歷史
                memory.append({"role": "assistant", "content": response_data})
                return user_data
            except ValidationError as ve:
                print(f"JSON 解析錯誤: {ve}")
                print(f"Content received: {response_data}")
                return "Unable to extract valid data. Please check the input format."
        else:
            print("No content in the response message.")
            return "No content in the response message."

    except OpenAIError as e:
        print(f"OpenAI API 錯誤: {e}")
        return "OpenAI API error occurred. Please try again later."
