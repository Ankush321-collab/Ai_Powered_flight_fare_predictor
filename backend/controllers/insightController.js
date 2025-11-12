const axios = require('axios');
const Summary = require('../models/Summary');
const llmClient = require('../utils/llmClient');

// POST /api/insights/generate
const generateInsight = async (req, res) => {
  const { route, data } = req.body; // data: prices, sentiment stats etc
  try {
    const prompt = `You are a flight fare analyst. Given the data: ${JSON.stringify(data)} produce a concise 3-sentence insight for route ${route}.`;
    const llmResponse = await llmClient.complete(prompt);
    const summaryText = llmResponse?.choices?.[0]?.text?.trim() || llmResponse?.data?.choices?.[0]?.message?.content || llmResponse;
    const summary = new Summary({ route, summary_text: summaryText, data });
    await summary.save();
    res.json({ success: true, summary });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

// GET /api/insights/latest?route=DEL-DXB
const getLatest = async (req, res) => {
  const { route } = req.query;
  try {
    const query = {};
    if (route) query.route = route;
    const latest = await Summary.find(query).sort({ created_at: -1 }).limit(10);
    res.json({ success: true, data: latest });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};

module.exports = { generateInsight, getLatest };
