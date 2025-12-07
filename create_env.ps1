# Script to create .env file
# This script creates a .env file with template values
# Replace 'your-api-key-here' with your actual OpenAI API key

$envContent = @"
OPENAI_API_KEY=your-api-key-here
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/docreview
REDIS_URL=redis://localhost:6379/0
LOG_LEVEL=INFO
"@

$envContent | Out-File -FilePath .env -Encoding utf8
Write-Host ".env file created successfully!"
Write-Host "IMPORTANT: Replace 'your-api-key-here' with your actual OpenAI API key in the .env file!"

