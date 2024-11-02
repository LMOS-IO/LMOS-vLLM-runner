FROM vllm/vllm-openai

COPY requirements.txt lmos/requirements.txt

RUN pip install -r lmos/requirements.txt

COPY lmos-vllm lmos

ENTRYPOINT ["python3", "lmos/entrypoint.py"]