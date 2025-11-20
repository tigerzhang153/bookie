const functions = require('firebase-functions');
const admin = require('firebase-admin');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

admin.initializeApp();

// CORS helper
const cors = require('cors')({ origin: true });

// Health check endpoint
exports.health = functions.https.onRequest((req, res) => {
  cors(req, res, () => {
    res.json({ status: 'healthy' });
  });
});

// Predict endpoint
exports.predict = functions
  .runWith({
    memory: '2GB',
    timeoutSeconds: 300,
  })
  .https.onRequest((req, res) => {
    cors(req, res, async () => {
      if (req.method !== 'POST') {
        return res.status(405).json({ detail: 'Method not allowed' });
      }

      try {
        const { home_team_id, away_team_id, betting_line } = req.body;

        if (!home_team_id || !away_team_id || !betting_line) {
          return res.status(400).json({ detail: 'Missing required fields' });
        }

        // Call Python script for prediction
        const pythonScript = path.join(__dirname, 'predict.py');
        const pythonProcess = spawn('python3', [pythonScript], {
          env: {
            ...process.env,
            HOME_TEAM_ID: home_team_id.toString(),
            AWAY_TEAM_ID: away_team_id.toString(),
            BETTING_LINE: betting_line.toString(),
          },
        });

        let stdout = '';
        let stderr = '';

        pythonProcess.stdout.on('data', (data) => {
          stdout += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
          stderr += data.toString();
        });

        pythonProcess.on('close', (code) => {
          if (code !== 0) {
            console.error('Python script error:', stderr);
            return res.status(500).json({ detail: stderr || 'Prediction failed' });
          }

          try {
            const result = JSON.parse(stdout);
            res.json(result);
          } catch (error) {
            console.error('JSON parse error:', error);
            res.status(500).json({ detail: 'Invalid response from prediction service' });
          }
        });

        pythonProcess.on('error', (error) => {
          console.error('Python process error:', error);
          res.status(500).json({ detail: 'Failed to start prediction service' });
        });
      } catch (error) {
        console.error('Request error:', error);
        res.status(500).json({ detail: error.message });
      }
    });
  });

// Combined API endpoint (routes to health or predict)
exports.api = functions
  .runWith({
    memory: '2GB',
    timeoutSeconds: 300,
  })
  .https.onRequest((req, res) => {
    cors(req, res, () => {
      const path = req.path;

      if (path === '/health' || path === '/api/health') {
        return res.json({ status: 'healthy' });
      }

      if (req.method === 'POST' && (path === '/predict' || path === '/api/predict')) {
        // Handle predict - same logic as above
        const { home_team_id, away_team_id, betting_line } = req.body;

        if (!home_team_id || !away_team_id || !betting_line) {
          return res.status(400).json({ detail: 'Missing required fields' });
        }

        const { spawn } = require('child_process');
        const path = require('path');
        const pythonScript = path.join(__dirname, 'predict.py');
        const pythonProcess = spawn('python3', [pythonScript], {
          env: {
            ...process.env,
            HOME_TEAM_ID: home_team_id.toString(),
            AWAY_TEAM_ID: away_team_id.toString(),
            BETTING_LINE: betting_line.toString(),
          },
        });

        let stdout = '';
        let stderr = '';

        pythonProcess.stdout.on('data', (data) => {
          stdout += data.toString();
        });

        pythonProcess.stderr.on('data', (data) => {
          stderr += data.toString();
        });

        pythonProcess.on('close', (code) => {
          if (code !== 0) {
            console.error('Python script error:', stderr);
            return res.status(500).json({ detail: stderr || 'Prediction failed' });
          }

          try {
            const result = JSON.parse(stdout);
            res.json(result);
          } catch (error) {
            console.error('JSON parse error:', error);
            res.status(500).json({ detail: 'Invalid response from prediction service' });
          }
        });

        pythonProcess.on('error', (error) => {
          console.error('Python process error:', error);
          res.status(500).json({ detail: 'Failed to start prediction service' });
        });
      } else {
        res.status(404).json({ detail: 'Not found' });
      }
    });
  });

