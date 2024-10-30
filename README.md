# JSON Extractor Using GPT

OpenAI API 在 2024/8 推出支援 [JSON 格式的輸出](https://openai.com/index/introducing-structured-outputs-in-the-api/)，所以此專案就是來實作 OpenAI GPT-4o (`gpt-4o-2024-08-06`) 模型，自動從使用者的輸入中提取姓名、電子郵件和電話號碼等資訊。使用了 `Streamlit` 作為前端框架，並提供了 `JSON Schema` 和 `Function Calling` 兩種提取資料的方法。

# 主要功能
- **資料提取模式**：支援 `JSON Schema` 和 `Function Calling` 兩種模式。
- **格式驗證**：自動驗證電子郵件格式，確保回傳資料的準確性。
- **歷史記錄**：儲存使用者輸入和 GPT 的回應，方便查看對話歷史。
- **資料保存**：成功提取的資料會以 JSON 格式保存至本地檔案。

# 前置步驟
## 複製專案
```
git clone https://github.com/estellacoding/gpt-json-extractor.git
cd gpt-json-extractor
```

## 安裝套件
```
pip install -r requirements.txt
```

## 設定環境變數
在專案目錄下建立 .env 檔案，並填寫以下內容。
```
OPENAI_API_KEY = <your OpenAI API key>
```

## 專案結構
```
gpt-json-extractor/
├── app.py                   # Streamlit 主應用程式
├── json_schema.py           # JSON Schema 模式下的資料提取邏輯
├── function_calling.py      # Function Calling 模式下的資料提取邏輯
├── models.py                # 使用者資料模型定義
├── validate_format.py       # 電子郵件格式驗證函數
├── requirements.txt         # 專案所需套件庫
└── README.md                # 專案說明文件
```

# 執行程式
## 啟動 Streamlit 應用程式
```
streamlit run app.py
```

## 開啟瀏覽器
開啟瀏覽器，進入 http://localhost:8501，即可使用專案介面。

## 輸入資料
選擇「JSON Schema」或「Function Calling」模式，並在輸入框中輸入訊息。點擊「Submit」按鈕，即可查看提取資料。
```
我的名字是Stella，請用 stelladai1028@gmail.com 聯絡我，電話是0988999999
```
