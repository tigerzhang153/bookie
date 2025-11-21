import config from '../config'
import { teamNameToId } from './teamMapping'

export const predictGame = async (team1, team2, bettingLine) => {
  try {
    // Convert team names to IDs
    const homeTeamId = teamNameToId[team1.trim()]
    const awayTeamId = teamNameToId[team2.trim()]

    if (!homeTeamId || !awayTeamId) {
      throw new Error("Invalid team name(s). Please enter valid NBA team names.")
    }

    const bettingLineNum = Number.parseFloat(bettingLine)
    if (isNaN(bettingLineNum)) {
      throw new Error("Please enter a valid betting line number.")
    }

    // Call the actual prediction API
    const response = await fetch(`${config.apiUrl}/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({
        home_team_id: homeTeamId,
        away_team_id: awayTeamId,
        betting_line: bettingLineNum
      })
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => null)
      throw new Error(errorData?.detail || 'Failed to get prediction from model')
    }

    const result = await response.json()
    return result
  } catch (error) {
    console.error("Prediction API error:", error)
    throw error
  }
}
