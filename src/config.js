const config = {
  apiUrl: process.env.NODE_ENV === 'production'
    ? 'YOUR_CLOUD_RUN_URL_HERE'  // Will be updated after Cloud Run deployment
    : 'http://localhost:8000'
}

export default config; 