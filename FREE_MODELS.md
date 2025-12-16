# Free Model API Options for Testing

This document lists free model API options you can use for testing GaiaSage.

## Current Setup

Currently, the project uses **Google Gemini** models via Agno framework. The dependency is `agno[google]==2.3.13`.

## Free Model Options

### 1. Google Gemini (Current - Free Tier Available)

**Pros:**
- Already configured in the project
- Free tier with generous limits
- Good performance

**Cons:**
- Rate limits (429 errors) when quota exceeded
- Requires Google account

**Setup:**
- Get API key: https://makersuite.google.com/app/apikey
- Set `GOOGLE_API_KEY` in environment variables

**Free Tier Limits:**
- 60 requests per minute (RPM)
- 1,500 requests per day (RPD)

### 2. OpenAI (Free Credits for New Users)

**Pros:**
- $5 free credits for new users
- High quality models
- Good documentation

**Cons:**
- Credits expire after 3 months
- Requires credit card (but won't charge if you stay within free tier)

**Setup:**
1. Install OpenAI support:
   ```bash
   uv add "agno[openai]"
   ```

2. Update `src/gaiasage/agent.py`:
   ```python
   from agno.models.openai import OpenAI
   
   # Replace Gemini with OpenAI
   guard_agent = Agent(
       name="GuardAgent",
       model=OpenAI(id="gpt-3.5-turbo"),  # Free tier compatible
       # ... rest of config
   )
   ```

3. Set environment variable:
   ```bash
   export OPENAI_API_KEY=your_openai_api_key
   ```

**Get API Key:** https://platform.openai.com/api-keys

### 3. Local Models with Ollama (Completely Free)

**Pros:**
- 100% free, no API limits
- Runs locally, no internet required
- Privacy-friendly

**Cons:**
- Requires local installation
- May need GPU for good performance
- Setup more complex

**Setup:**
1. Install Ollama: https://ollama.ai
2. Download a model:
   ```bash
   ollama pull llama3.2
   # or
   ollama pull mistral
   ```

3. Install Agno Ollama support (if available) or use OpenAI-compatible API:
   ```bash
   # Ollama provides OpenAI-compatible API
   # Set base URL to local Ollama
   export OPENAI_API_BASE=http://localhost:11434/v1
   export OPENAI_API_KEY=ollama  # Dummy key
   ```

4. Use with OpenAI model configuration pointing to local Ollama

### 4. Anthropic Claude (Free Tier)

**Pros:**
- $5 free credits
- High quality responses

**Cons:**
- Credits expire
- Requires credit card

**Setup:**
1. Install Anthropic support:
   ```bash
   uv add "agno[anthropic]"
   ```

2. Update agent configuration:
   ```python
   from agno.models.anthropic import Anthropic
   
   guard_agent = Agent(
       name="GuardAgent",
       model=Anthropic(id="claude-3-haiku-20240307"),  # Cheapest option
       # ...
   )
   ```

3. Set environment variable:
   ```bash
   export ANTHROPIC_API_KEY=your_key
   ```

**Get API Key:** https://console.anthropic.com/

### 5. DeepSeek (Free Tier Available)

**Pros:**
- Free tier available
- Good performance
- OpenAI-compatible API

**Setup:**
1. Get API key: https://platform.deepseek.com/
2. Use with OpenAI-compatible configuration:
   ```python
   from agno.models.openai import OpenAI
   
   guard_agent = Agent(
       name="GuardAgent",
       model=OpenAI(
           id="deepseek-chat",
           base_url="https://api.deepseek.com/v1"
       ),
       # ...
   )
   ```

3. Set environment variable:
   ```bash
   export OPENAI_API_KEY=your_deepseek_key
   ```

## Recommended for Testing

### Quick Testing (No Setup)
- **Google Gemini**: Already configured, just need API key

### Best Free Option
- **Ollama (Local)**: Completely free, no limits, privacy-friendly
- **DeepSeek**: Good free tier, OpenAI-compatible

### For Production-like Testing
- **OpenAI GPT-3.5-turbo**: $5 free credits, reliable
- **Anthropic Claude Haiku**: $5 free credits, fast and cheap

## Switching Models

To switch models, you need to:

1. **Install the appropriate Agno extension:**
   ```bash
   uv add "agno[openai]"      # For OpenAI
   uv add "agno[anthropic]"   # For Anthropic
   # etc.
   ```

2. **Update `src/gaiasage/agent.py`:**
   - Change the import statement
   - Update model configuration in agent definitions
   - Update all three agents (guard, planner, coder) and root_team

3. **Update environment variables:**
   - Remove or change `GOOGLE_API_KEY`
   - Add the new API key (e.g., `OPENAI_API_KEY`)

4. **Update `requirements.txt`** if needed for Vercel deployment

## Example: Switching to OpenAI

Here's a complete example of switching to OpenAI:

```python
# In src/gaiasage/agent.py

# Change import
from agno.models.openai import OpenAI  # Instead of Gemini

# Update guard_agent
guard_agent = Agent(
    name="GuardAgent",
    model=OpenAI(id="gpt-3.5-turbo"),  # Free tier compatible
    # ... rest stays the same
)

# Update planner_agent
planner_agent = Agent(
    name="PlannerAgent",
    model=OpenAI(id="gpt-3.5-turbo"),
    # ...
)

# Update coder_agent
coder_agent = Agent(
    name="CoderAgent",
    model=OpenAI(id="gpt-3.5-turbo"),
    # ...
)

# Update root_team
root_team = Team(
    members=[guard_agent, planner_agent, coder_agent],
    name="GaiaSage_Coordinator",
    model=OpenAI(id="gpt-3.5-turbo"),
    # ...
)
```

## Notes

- **Rate Limits**: All free tiers have rate limits. If you hit 429 errors, wait a few minutes or switch to a different provider.
- **Cost Monitoring**: Even free tiers may have usage limits. Monitor your usage.
- **Local Models**: Ollama is the best option for unlimited free testing, but requires local setup.
- **Testing**: For quick testing, stick with Gemini (already configured) or try DeepSeek (easy setup).

