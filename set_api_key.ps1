# PowerShell script to set OpenRouter API key
$env:OPENROUTER_API_KEY = "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"
Write-Host "OpenRouter API key set for this session."
Write-Host "To make it permanent, add to your PowerShell profile or use:"
Write-Host '[System.Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "sk-or-v1-...", "User")'
