$ErrorActionPreference = "Stop"

Write-Host "Starting Automated Market Research Agent on the network..."
Write-Host "Other computers can connect using: http://<this-computer-ip>:8501"
streamlit run app.py --server.address=0.0.0.0 --server.port=8501
