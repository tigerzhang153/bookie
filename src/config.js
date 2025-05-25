const config = {
  apiUrl: process.env.NODE_ENV === 'production'
    ? 'https://bookie-ai-api.onrender.com'  // We'll deploy the API to Render
    : 'http://localhost:8000'
}

export default config; 