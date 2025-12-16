# Troubleshooting Guide

## API Key Authentication Errors

### Error: "Authentication Fails, Your api key: **** is invalid"

This error indicates that the API key is not being recognized by DeepSeek API. Follow these steps:

#### 1. Verify API Key is Set

Check if the environment variable is correctly set:

```bash
# Check if the variable is set
echo $OPENAI_API_KEY

# Or check in Python
python -c "import os; print('API Key set:', bool(os.getenv('OPENAI_API_KEY')))"
```

#### 2. Verify API Key Format

- **No spaces**: Make sure there are no leading or trailing spaces
- **No quotes**: Don't include quotes in the `.env` file
- **Complete key**: Ensure you copied the entire key

**Correct format in `.env`:**
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Incorrect formats:**
```
OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Don't use quotes
OPENAI_API_KEY= sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx    # No space after =
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx     # No trailing space
```

#### 3. Verify API Key is Valid

1. **Check DeepSeek Platform:**
   - Visit https://platform.deepseek.com/
   - Log in to your account
   - Go to API Keys section
   - Verify the key exists and is active
   - Check if the key has expired or been revoked

2. **Test API Key Directly:**
   ```bash
   curl https://api.deepseek.com/v1/models \
     -H "Authorization: Bearer YOUR_API_KEY"
   ```
   Replace `YOUR_API_KEY` with your actual key. This should return a list of available models.

#### 4. Check Account Status

- **Balance**: Ensure your DeepSeek account has sufficient balance
- **Service Status**: Check if DeepSeek API service is operational
- **Rate Limits**: Verify you haven't exceeded rate limits

#### 5. Restart Server After Setting Environment Variable

If you set the environment variable after starting the server, you need to restart:

```bash
# Stop the server (Ctrl+C)
# Then restart
uvicorn api.main:app --reload --port 8000
```

#### 6. Verify .env File Location

The `.env` file must be in the **root directory** (same level as `pyproject.toml`):

```
gaiasage/
├── .env              ← Must be here
├── pyproject.toml
├── api/
└── src/
```

#### 7. Check for Multiple .env Files

Make sure you're not accidentally using a different `.env` file. The API loads from the root directory.

#### 8. Common Issues

**Issue: Key works in terminal but not in application**
- Solution: Make sure the `.env` file is in the correct location and the server is restarted

**Issue: Key was working but suddenly stopped**
- Solution: Check if the key was revoked or expired in DeepSeek platform
- Solution: Verify account balance

**Issue: Getting 401/403 errors**
- Solution: Verify the API key is correct
- Solution: Check account status and balance

## Getting a New API Key

If your current key is invalid:

1. Visit https://platform.deepseek.com/
2. Log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key immediately (you won't be able to see it again)
6. Update your `.env` file with the new key
7. Restart your server

## Testing API Key

You can test your API key using curl:

```bash
curl https://api.deepseek.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

If this works, the API key is valid and the issue is in the application configuration.

## Still Having Issues?

1. **Check server logs**: Look for detailed error messages
2. **Verify environment variable loading**: Check the startup logs for "OPENAI_API_KEY is configured"
3. **Test with a simple script**:
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   print("API Key:", os.getenv("OPENAI_API_KEY")[:10] + "..." if os.getenv("OPENAI_API_KEY") else "NOT SET")
   ```

