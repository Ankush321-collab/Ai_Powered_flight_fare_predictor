const mongoose = require('mongoose');

const SummarySchema = new mongoose.Schema({
  route: { type: String, required: true },
  summary_text: { type: String, required: true },
  data: { type: Object },
  created_at: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Summary', SummarySchema);
