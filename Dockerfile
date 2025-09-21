# 🐳 Containerization for DevOps
# Use the slim image for a smaller final image size
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# 1. INSTALL SYSTEM DEPENDENCIES & CA CERTIFICATES
# This is the crucial fix for the SSL error. It ensures the container can make secure HTTPS connections.
# 'apt-get update' and 'apt-get install' are commands for the Debian-based slim image.
# '--no-install-recommends' keeps the image small by avoiding unnecessary packages.
# 'curl' is needed for the HEALTHCHECK command later.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. UPGRADE PIP (Best Practice)
# Copy requirements file first to leverage Docker's cache.
# If requirements.txt doesn't change, Docker will skip the next steps until the COPY . command.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip

# 3. INSTALL PYTHON DEPENDENCIES
# Now we can install securely over HTTPS without the --trusted-host workaround.
RUN pip install --no-cache-dir -r requirements.txt

# 4. COPY APPLICATION CODE
# Copy the rest of the application. This is done after installing dependencies
# for better caching. If only code changes, dependencies don't need reinstalling.
COPY app/ ./app/
COPY assets/ ./assets/
COPY streamlit_app.py .
# Copy the .streamlit directory if you have configs, but secrets should come from runtime environment variables, not the build.
# COPY .streamlit/ .streamlit/

# 5. EXPOSE PORT AND HEALTH CHECK
# Expose the port Streamlit runs on
EXPOSE 8501

# Health check to ensure the application is running
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# 6. RUN THE APPLICATION
# Use the correct entry point based on your file structure.
# Since you have a 'streamlit_app.py' in the root, this is correct.
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]