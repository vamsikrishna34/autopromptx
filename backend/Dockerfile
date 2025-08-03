# Use Python base image
FROM python:3.9

# Create user
RUN useradd -m -u 1000 user
USER user

# Set working directory
WORKDIR /app

# Set PATH
ENV PATH="/home/user/.local/bin:$PATH"

# Install dependencies
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy app code
COPY --chown=user . /app

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]