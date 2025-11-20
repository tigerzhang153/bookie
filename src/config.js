const config = {
  apiUrl: process.env.NODE_ENV === 'production'
    ? 'https://us-central1-bookie-ai-dc1f8.cloudfunctions.net/api'  // Firebase Functions URL
    : 'http://localhost:8000'
}

export default config; 