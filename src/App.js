"use client"

import { useState } from "react"
import { db } from "./firebase"
import { collection, addDoc } from "firebase/firestore"
import "./App.css"

function App() {
  const [team1, setTeam1] = useState("")
  const [team2, setTeam2] = useState("")
  const [bettingLine, setBettingLine] = useState("")
  const [prediction, setPrediction] = useState(null)
  const [loading, setLoading] = useState(false)
  const [currentView, setCurrentView] = useState("home")

  const handlePrediction = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      // Call your prediction API
      const response = await fetch("/api/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          team1,
          team2,
          betting_line: Number.parseFloat(bettingLine),
        }),
      })

      const result = await response.json()
      setPrediction(result)

      // Save prediction to Firestore
      await addDoc(collection(db, "predictions"), {
        team1,
        team2,
        betting_line: Number.parseFloat(bettingLine),
        prediction: result,
        timestamp: new Date(),
      })
    } catch (error) {
      console.error("Prediction error:", error)
    } finally {
      setLoading(false)
    }
  }

  const HomePage = () => (
    <div className="home-container">
      <h1>🏀 Bookie AI</h1>
      <p>AI-Powered Sports Betting Predictions</p>

      <div className="options-grid">
        <div className="option-card" onClick={() => setCurrentView("prediction")}>
          <h3>📊 Game Prediction</h3>
          <p>Get ML-powered predictions for your games</p>
        </div>

        <div className="option-card" onClick={() => setCurrentView("analytics")}>
          <h3>📈 Analytics</h3>
          <p>View performance charts and insights</p>
        </div>
      </div>
    </div>
  )

  const PredictionPage = () => (
    <div className="prediction-container">
      <button onClick={() => setCurrentView("home")} className="back-btn">
        ← Back to Home
      </button>

      <h2>Game Prediction</h2>

      <form onSubmit={handlePrediction} className="prediction-form">
        <div className="form-group">
          <label>Home Team:</label>
          <input
            type="text"
            value={team1}
            onChange={(e) => setTeam1(e.target.value)}
            placeholder="e.g., Lakers"
            required
          />
        </div>

        <div className="vs-divider">VS</div>

        <div className="form-group">
          <label>Away Team:</label>
          <input
            type="text"
            value={team2}
            onChange={(e) => setTeam2(e.target.value)}
            placeholder="e.g., Warriors"
            required
          />
        </div>

        <div className="form-group">
          <label>Betting Line (O/U):</label>
          <input
            type="number"
            step="0.5"
            value={bettingLine}
            onChange={(e) => setBettingLine(e.target.value)}
            placeholder="e.g., 220.5"
            required
          />
        </div>

        <button type="submit" disabled={loading} className="predict-btn">
          {loading ? "Analyzing..." : "Get Prediction"}
        </button>
      </form>

      {prediction && (
        <div className="prediction-result">
          <h3>Prediction Results</h3>
          <div className="result-card">
            <p>
              <strong>Predicted Total:</strong> {prediction.predicted_total}
            </p>
            <p>
              <strong>Recommendation:</strong> {prediction.recommendation}
            </p>
            <p>
              <strong>Edge:</strong> {prediction.edge} points
            </p>
            <p>
              <strong>Confidence:</strong> {prediction.confidence}%
            </p>
          </div>
        </div>
      )}
    </div>
  )

  const AnalyticsPage = () => (
    <div className="analytics-container">
      <button onClick={() => setCurrentView("home")} className="back-btn">
        ← Back to Home
      </button>

      <h2>Analytics Dashboard</h2>
      <div className="analytics-placeholder">
        <p>📊 Charts and analytics coming soon!</p>
        <p>This will show your prediction accuracy, betting trends, and performance metrics.</p>
      </div>
    </div>
  )

  return (
    <div className="App">
      {currentView === "home" && <HomePage />}
      {currentView === "prediction" && <PredictionPage />}
      {currentView === "analytics" && <AnalyticsPage />}
    </div>
  )
}

export default App
