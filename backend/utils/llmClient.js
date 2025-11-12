const axios = require('axios');
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

if (!OPENAI_API_KEY) {
  console.warn('OPENAI_API_KEY not set; llmClient will fail until configured');
}

// Minimal wrapper for OpenAI completion (works with both v1 chat and older completion fields)
const complete = async (prompt, options = {}) => {
  const payload = {
    model: options.model || 'gpt-4',
    messages: [
      { role: 'system', content: 'You are a helpful travel analyst.' },
      { role: 'user', content: prompt }
    ],
    temperature: options.temperature ?? 0.4,
    max_tokens: options.max_tokens ?? 300
  };

  try {
    const res = await axios.post('https://api.openai.com/v1/chat/completions', payload, {
      headers: { Authorization: `Bearer ${OPENAI_API_KEY}` }
    });
    return res.data;
  } catch (err) {
    console.error('LLM client error', err?.response?.data || err.message);
    throw err;
  }
};

module.exports = { complete };
