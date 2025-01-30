# AIDE-API
https://aide.dev/ used as Anthropic Claude-compatible endpoint. 
https://aide.dev/ 用作与 Claude 兼容的终端。

pip install flask

python3 main.py

The script will generate a link, go to this link to sign up for an account.
脚本将生成一个链接，请访问该链接注册账户。
When you sign up and sign in, the script will automatically work.
注册并登录后，脚本将自动运行。
Use localhost:5000 or localhost:5000/messages as your Anthropic Claude-compatible (messages API) endpoint.
使用 localhost:5000 或 localhost:5000/messages 作为 Anthropic Claude 兼容（消息 API）端点。

Anthropic Documentation: https://docs.anthropic.com/en/api/messages

Also supports other models such as Claude 3.5 Sonnet by changing the model:
通过更改型号，还可支持 Claude 3.5 Sonnet 等其他型号：
"model": "claude-3-5-sonnet-20241022",
