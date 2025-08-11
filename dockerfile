FROM python:3.12-slim
ENV TOKEN='token from @BotFather'
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "bot.py" ]

