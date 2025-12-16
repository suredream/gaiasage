# How to Get DeepSeek API Key

## Step-by-Step Guide

### 1. Visit DeepSeek Platform
Go to: **https://platform.deepseek.com/**

### 2. Sign Up or Log In
- If you don't have an account, click "Sign Up"
- You can sign up with:
  - Email
  - GitHub account
  - Other supported methods

### 3. Navigate to API Keys
- After logging in, go to the **API Keys** section
- This is usually in the dashboard or settings menu

### 4. Create a New API Key
- Click "Create API Key" or "New API Key"
- Give it a name (e.g., "GaiaSage Development")
- Click "Create"

### 5. Copy the API Key
- **IMPORTANT**: Copy the API key immediately
- You won't be able to see it again after closing the dialog
- The key should look like: `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 6. Add to Your Project

**For local development**, add to `.env` file:
```
OPENAI_API_KEY=sk-your-actual-deepseek-key-here
```

**For Vercel deployment**, add in Vercel dashboard:
- Settings → Environment Variables
- Add `OPENAI_API_KEY` with your DeepSeek key

## Important Notes

### API Key Format
- DeepSeek API keys typically start with `sk-`
- They are usually 40-50+ characters long
- **Do NOT** use OpenAI API keys (they start with `sk-proj-` or `sk-` but are for OpenAI, not DeepSeek)

### Free Tier
- DeepSeek offers free tier with generous limits
- Check your account balance in the dashboard
- Free tier may have rate limits

### Security
- Never commit API keys to Git
- Keep your `.env` file in `.gitignore`
- Rotate keys if they are exposed

## Troubleshooting

### "API key is invalid" Error
1. **Verify it's a DeepSeek key**: Make sure you got it from https://platform.deepseek.com/, not from OpenAI
2. **Check key format**: Should start with `sk-` (not `sk-proj-`)
3. **Verify key is active**: Check in DeepSeek dashboard
4. **Check account balance**: Ensure you have sufficient balance
5. **Try creating a new key**: Old keys may have been revoked

### Testing Your API Key
You can test your API key with curl:

```bash
curl https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer YOUR_DEEPSEEK_API_KEY"
```

If this returns a list of models, your key is valid.

## Alternative: Using OpenAI API Key

If you want to use OpenAI instead of DeepSeek:

1. Get OpenAI API key from https://platform.openai.com/api-keys
2. Update the model configuration in `src/gaiasage/agent.py`:
   - Change `base_url` to OpenAI's URL (or remove it)
   - Change `id` to `"gpt-3.5-turbo"` or another OpenAI model
3. Use the same `OPENAI_API_KEY` environment variable

