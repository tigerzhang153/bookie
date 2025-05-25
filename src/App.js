"use client"

import { useState } from "react"
import HomePage from "./components/HomePage"
import PredictionPage from "./components/PredictionPage"
import AnalyticsPage from "./components/AnalyticsPage"
import "./App.css"

function App() {
  const [currentView, setCurrentView] = useState("home")
  const [prediction, setPrediction] = useState(null)

  const navigateTo = (view) => {
    setCurrentView(view)
  }

  const navigateBack = () => {
    setCurrentView("home")
    setPrediction(null)
  }

  return (
    <div className="App">
      {currentView === "home" && <HomePage onNavigate={navigateTo} />}
      {currentView === "prediction" && (
        <PredictionPage onNavigateBack={navigateBack} prediction={prediction} setPrediction={setPrediction} />
      )}
      {currentView === "analytics" && <AnalyticsPage onNavigateBack={navigateBack} />}
    </div>
  )
}

export default App
