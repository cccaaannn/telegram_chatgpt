# Telegram ChatGPT

Message with ChatGPT on Telegram.

![GitHub top language](https://img.shields.io/github/languages/top/cccaaannn/telegram_chatgpt?color=blue) ![GitHub repo size](https://img.shields.io/github/repo-size/cccaaannn/telegram_chatgpt?color=orange) [![GitHub](https://img.shields.io/github/license/cccaaannn/telegram_chatgpt?color=green)](https://github.com/cccaaannn/telegram_chatgpt/blob/master/LICENSE) [![GitHub release](https://img.shields.io/github/v/release/cccaaannn/telegram_chatgpt?color=blueviolet)](https://github.com/cccaaannn/telegram_chatgpt/releases)

---

## Setup

### Preliminary steps
1. Get a [Telegram](https://core.telegram.org/bots) bot key.
2. Get a [OpenAI](https://platform.openai.com) api key.

### Running
#### Docker
1. Run the container.
```shell
docker run --name telegram_chatgpt -e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> -e OPENAI_API_KEY=<OPENAI_API_KEY> cccaaannn/telegram_chatgpt:latest
```
- You should map the db to outside, to keep the chat history after bot restarts.
```shell
docker run --name telegram_chatgpt -e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> -e OPENAI_API_KEY=<OPENAI_API_KEY> -v <YOUR_DB_PATH>:/telegram_chatgpt/db cccaaannn/telegram_chatgpt:latest
```
- Optionally you can map the logs to a directory.
```shell
docker run --name telegram_chatgpt -e TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY> -e OPENAI_API_KEY=<OPENAI_API_KEY> -v <YOUR_DB_PATH>:/telegram_chatgpt/db -v <YOUR_LOG_PATH>:/telegram_chatgpt/logs cccaaannn/telegram_chatgpt:latest
```

#### Without docker
1. Install dependencies.
```python
pip install -r requirements.txt
```
2 Run by passing keys
```shell
python telegram_chatgpt -t <TELEGRAM_BOT_KEY> -o <OPENAI_API_KEY>
```

2 You can also set api keys as env variables to run without parameters
```shell
export TELEGRAM_BOT_KEY=<TELEGRAM_BOT_KEY>
export OPENAI_API_KEY=<OPENAI_API_KEY>
```

```shell
python telegram_chatgpt
```
