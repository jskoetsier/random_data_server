FROM python:3.9-slim

WORKDIR /app

COPY server.py .

# Make the script executable
RUN chmod +x server.py

# Expose the ports
EXPOSE 80 443

# Run the server
CMD ["python", "server.py"]
