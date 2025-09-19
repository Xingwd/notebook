FROM python:3.10

WORKDIR /app

COPY ai_data_analyst.py /app

COPY requirements.txt /app

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD ["streamlit", "run", "--theme.base=light", "ai_data_analyst.py"]
