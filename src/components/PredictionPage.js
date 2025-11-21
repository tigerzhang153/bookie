"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card"
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Label } from "./ui/label"
import { ArrowLeft, Loader2, TrendingUp, Target, Brain, AlertCircle } from "lucide-react"
import { Alert, AlertDescription } from "./ui/alert"
import { Badge } from "./ui/badge"
import { db } from "../firebase"
import { collection, addDoc } from "firebase/firestore"
import { teamNameToId } from "../api/teamMapping"
import config from '../config'

export default function PredictionPage({ onNavigateBack, prediction, setPrediction }) {
  const [team1, setTeam1] = useState("")
  const [team2, setTeam2] = useState("")
  const [bettingLine, setBettingLine] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError("")
    setPrediction(null)

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

      console.log("Sending prediction request:", {
        home_team_id: homeTeamId,
        away_team_id: awayTeamId,
        betting_line: bettingLineNum
      })

      // Call prediction API
      console.log("API URL:", config.apiUrl)
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
        }),
        signal: AbortSignal.timeout(60000) // 60 second timeout
      }).catch((fetchError) => {
        console.error("Fetch error:", fetchError)
        if (fetchError.name === 'AbortError') {
          throw new Error('Request timed out. Please try again.')
        } else if (fetchError.name === 'TypeError' && fetchError.message.includes('Failed to fetch')) {
          throw new Error(`Network error: Unable to reach API at ${config.apiUrl}. Check if the API is running and CORS is configured correctly.`)
        }
        throw fetchError
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => null)
        throw new Error(errorData?.detail || `API error: ${response.status} ${response.statusText}`)
      }

      const result = await response.json()
      console.log("Received prediction:", result)
      setPrediction(result)

      // Save to Firestore
      await addDoc(collection(db, "predictions"), {
        team1: team1.trim(),
        team2: team2.trim(),
        betting_line: bettingLineNum,
        prediction: result,
        timestamp: new Date(),
      })
    } catch (err) {
      console.error("Prediction error:", err)
      setError(err instanceof Error ? err.message : "Failed to get prediction. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 80) return "text-green-600 bg-green-50 border-green-200"
    if (confidence >= 60) return "text-yellow-600 bg-yellow-50 border-yellow-200"
    return "text-red-600 bg-red-50 border-red-200"
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <button
            onClick={onNavigateBack}
            className="inline-flex items-center text-slate-600 hover:text-slate-900 transition-colors"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Dashboard
          </button>
        </div>

        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
              AI Game Prediction
            </h1>
            <p className="text-slate-600">Enter matchup details for ML-powered analysis</p>
          </div>

          <div className="grid lg:grid-cols-2 gap-8">
            {/* Input Form */}
            <Card className="shadow-lg">
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Brain className="w-5 h-5 mr-2 text-blue-600" />
                  Prediction Input
                </CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="team1" className="text-sm font-medium">
                        Home Team
                      </Label>
                      <Input
                        id="team1"
                        placeholder="e.g., Los Angeles Lakers"
                        value={team1}
                        onChange={(e) => setTeam1(e.target.value)}
                        className="h-12"
                        required
                      />
                    </div>

                    <div className="text-center">
                      <span className="text-2xl font-bold text-slate-400">VS</span>
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="team2" className="text-sm font-medium">
                        Away Team
                      </Label>
                      <Input
                        id="team2"
                        placeholder="e.g., Golden State Warriors"
                        value={team2}
                        onChange={(e) => setTeam2(e.target.value)}
                        className="h-12"
                        required
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="bettingLine" className="text-sm font-medium">
                        Over/Under Line
                      </Label>
                      <Input
                        id="bettingLine"
                        type="number"
                        step="0.5"
                        placeholder="e.g., 220.5"
                        value={bettingLine}
                        onChange={(e) => setBettingLine(e.target.value)}
                        className="h-12"
                        required
                      />
                      <p className="text-xs text-slate-500">Enter the total points over/under line</p>
                    </div>
                  </div>

                  <Button
                    type="submit"
                    className="w-full h-12 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Analyzing with AI...
                      </>
                    ) : (
                      <>
                        <Target className="w-4 h-4 mr-2" />
                        Get Prediction
                      </>
                    )}
                  </Button>
                </form>
              </CardContent>
            </Card>

            {/* Results */}
            <div className="space-y-6">
              {error && (
                <Alert className="border-red-200 bg-red-50">
                  <AlertCircle className="h-4 w-4 text-red-600" />
                  <AlertDescription className="text-red-700">{error}</AlertDescription>
                </Alert>
              )}

              {prediction && (
                <Card className="shadow-lg border-green-200 bg-gradient-to-br from-green-50 to-blue-50">
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span className="text-green-800">ML Prediction Results</span>
                      <Badge variant="outline" className="text-xs">
                        {prediction.model_version || "Stacked Ensemble"}
                      </Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Main Prediction */}
                    <div className="text-center p-4 bg-white rounded-lg border">
                      <p className="text-sm text-slate-600 mb-1">Predicted Total Points</p>
                      <p className="text-3xl font-bold text-green-700">{prediction.predicted_total}</p>
                    </div>

                    {/* Betting Recommendation */}
                    <div className="text-center p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border">
                      <p className="text-sm text-slate-600 mb-2">Recommendation</p>
                      <Badge
                        variant={prediction.recommendation.includes("OVER") ? "default" : "secondary"}
                        className="text-lg px-4 py-2"
                      >
                        {prediction.recommendation}
                      </Badge>
                    </div>

                    {/* Key Metrics */}
                    <div className="grid grid-cols-2 gap-4">
                      <div className={`p-3 rounded-lg border ${getConfidenceColor(prediction.confidence)}`}>
                        <p className="text-xs font-medium mb-1">Confidence</p>
                        <p className="text-xl font-bold">{prediction.confidence}%</p>
                      </div>
                      <div className="p-3 rounded-lg border bg-orange-50 border-orange-200">
                        <p className="text-xs font-medium text-orange-600 mb-1">Edge</p>
                        <p className="text-xl font-bold text-orange-700">{prediction.edge} pts</p>
                      </div>
                    </div>

                    {/* Model Features */}
                    {prediction.model_features && (
                      <div className="p-3 bg-white rounded border">
                        <p className="text-sm font-medium mb-3">Model Features Used</p>
                        <div className="grid grid-cols-1 gap-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-slate-600">Home Team Avg:</span>
                            <span className="font-medium">{prediction.model_features.avgpointtotal_home}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-600">Away Team Avg:</span>
                            <span className="font-medium">{prediction.model_features.avgpointtotal_away}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-600">Combined Avg:</span>
                            <span className="font-medium">{prediction.model_features.meanpointtotal}</span>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Additional Info */}
                    <div className="space-y-3">
                      <div className="flex justify-between items-center p-3 bg-white rounded border">
                        <span className="text-sm font-medium">Betting Line</span>
                        <span className="font-bold">{prediction.betting_line}</span>
                      </div>

                      {prediction.factors && prediction.factors.length > 0 && (
                        <div className="p-3 bg-white rounded border">
                          <p className="text-sm font-medium mb-2">Model Components</p>
                          <div className="flex flex-wrap gap-1">
                            {prediction.factors.map((factor, index) => (
                              <Badge key={index} variant="outline" className="text-xs">
                                {factor}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              )}

              {!prediction && !error && !isLoading && (
                <Card className="border-dashed border-2 border-slate-300">
                  <CardContent className="text-center py-12">
                    <TrendingUp className="w-12 h-12 mx-auto text-slate-400 mb-4" />
                    <p className="text-slate-500">Enter team details to get your AI prediction</p>
                  </CardContent>
                </Card>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
