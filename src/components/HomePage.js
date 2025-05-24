"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { Button } from "./ui/button"
import { TrendingUp, BarChart3, Zap } from "lucide-react"

export default function HomePage({ onNavigate }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Zap className="w-8 h-8 text-blue-600 mr-2" />
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Sports Prediction AI
            </h1>
          </div>
          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Advanced machine learning predictions powered by Firebase and Python analytics
          </p>
        </div>

        {/* Main Options */}
        <div className="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          {/* Prediction Option */}
          <Card
            className="group hover:shadow-xl transition-all duration-300 border-2 hover:border-blue-300 hover:-translate-y-1 cursor-pointer"
            onClick={() => onNavigate("prediction")}
          >
            <CardHeader className="text-center pb-6">
              <div className="mx-auto w-20 h-20 bg-gradient-to-br from-blue-100 to-blue-200 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <TrendingUp className="w-10 h-10 text-blue-600" />
              </div>
              <CardTitle className="text-2xl text-slate-900 mb-2">AI Game Prediction</CardTitle>
              <CardDescription className="text-slate-600 text-base">
                Enter team matchup details and betting lines to get sophisticated ML-powered predictions
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <div className="space-y-4">
                <div className="text-sm text-slate-500 space-y-1">
                  <p>✓ Real-time ML analysis</p>
                  <p>✓ Confidence scoring</p>
                  <p>✓ Betting recommendations</p>
                </div>
                <Button
                  size="lg"
                  className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white shadow-lg"
                  onClick={(e) => {
                    e.stopPropagation()
                    onNavigate("prediction")
                  }}
                >
                  Start Prediction
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Analytics Option */}
          <Card
            className="group hover:shadow-xl transition-all duration-300 border-2 hover:border-purple-300 hover:-translate-y-1 cursor-pointer"
            onClick={() => onNavigate("analytics")}
          >
            <CardHeader className="text-center pb-6">
              <div className="mx-auto w-20 h-20 bg-gradient-to-br from-purple-100 to-purple-200 rounded-full flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300">
                <BarChart3 className="w-10 h-10 text-purple-600" />
              </div>
              <CardTitle className="text-2xl text-slate-900 mb-2">Analytics Dashboard</CardTitle>
              <CardDescription className="text-slate-600 text-base">
                Explore comprehensive data visualizations and performance metrics
              </CardDescription>
            </CardHeader>
            <CardContent className="text-center">
              <div className="space-y-4">
                <div className="text-sm text-slate-500 space-y-1">
                  <p>✓ Interactive charts</p>
                  <p>✓ Historical trends</p>
                  <p>✓ Performance insights</p>
                </div>
                <Button
                  size="lg"
                  variant="outline"
                  className="w-full border-2 border-purple-600 text-purple-600 hover:bg-purple-50 hover:border-purple-700 shadow-lg"
                  onClick={(e) => {
                    e.stopPropagation()
                    onNavigate("analytics")
                  }}
                >
                  View Analytics
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Footer Info */}
        <div className="text-center mt-16">
          <div className="inline-flex items-center px-4 py-2 bg-slate-100 rounded-full">
            <div className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></div>
            <span className="text-sm text-slate-600">Connected to Firebase • Python ML Models Active</span>
          </div>
        </div>
      </div>
    </div>
  )
}
