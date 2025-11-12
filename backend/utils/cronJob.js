const cron = require('node-cron');
const axios = require('axios');

// Simple scheduled job example: call backend update endpoint daily at 03:00 UTC
const startJobs = () => {
  cron.schedule('0 3 * * *', async () => {
    console.log('Running daily scraper + LLM update');
    try {
      // Example: trigger scraper (assuming scraper exposes a webhook or the backend triggers remote job)
      // await axios.post(process.env.SCRAPER_TRIGGER_URL || 'http://scraper-service/run');
      // Optionally trigger insight generation
      // await axios.post(`${process.env.BASE_URL}/api/insights/generate`, {...});
    } catch (err) {
      console.error('Cron job error', err.message);
    }
  }, { timezone: 'UTC' });
};

module.exports = { startJobs };
