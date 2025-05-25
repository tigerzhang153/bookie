export const predictGame = async (team1, team2, bettingLine) => {
  try {
    // For now, return mock data that matches your model structure
    // Replace this with actual call to your Firebase Cloud Function

    const mockResponse = {
      predicted_total: 218.5,
      betting_line: bettingLine,
      edge: Math.abs(218.5 - bettingLine),
      recommendation: 218.5 > bettingLine ? "bet the OVER" : "bet the UNDER",
      confidence: 75,
      model_features: {
        avgpointtotal_home: 110.2,
        avgpointtotal_away: 108.3,
        meanpointtotal: 109.25,
      },
    }

    return mockResponse
  } catch (error) {
    console.error("Prediction API error:", error)
    throw error
  }
}
