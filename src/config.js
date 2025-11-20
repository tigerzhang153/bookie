const config = {
  apiUrl: process.env.NODE_ENV === 'production'
    ? 'https://bookie-1075298251385.us-east5.run.app'  // Cloud Run URL
    : 'http://localhost:8000'
}

export default config; 