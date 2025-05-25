"use client"

import { Card, CardContent, CardHeader, CardTitle } from "./ui/card"
import { Button } from "./ui/button"
import { ArrowLeft, BarChart3, TrendingUp, PieChart, Activity, Database, Brain } from "lucide-react"
import { Badge } from "./ui/badge"

export default function AnalyticsPage({ onNavigateBack }) {
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

        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-2">
              Analytics Dashboard
            </h1>
            <p className="text-slate-600">Comprehensive insights powered by Firebase and Python analytics</p>
          </div>

          {/* Status Bar */}
          <div className="mb-8">
            <Card className="bg-gradient-to-r from-green-50 to-blue-50 border-green-200">
              <CardContent className="py-4">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-green-500 rounded-full mr-2 animate-pulse"></div>
                      <span className="text-sm font-medium">Firebase Connected</span>
                    </div>
                    <div className="flex items-center">
                      <Database className="w-4 h-4 text-blue-600 mr-2" />
                      <span className="text-sm">Real-time Data</span>
                    </div>
                    <div className="flex items-center">
                      <Brain className="w-4 h-4 text-purple-600 mr-2" />
                      <span className="text-sm">ML Models Active</span>
                    </div>
                  </div>
                  <Badge variant="outline" className="text-xs">
                    Last Updated: Live
                  </Badge>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Chart Placeholders */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            <Card className="group hover:shadow-lg transition-all duration-300 border-2 hover:border-blue-200">
              <CardHeader className="text-center">
                <BarChart3 className="w-12 h-12 mx-auto text-blue-600 mb-2 group-hover:scale-110 transition-transform" />
                <CardTitle className="text-slate-700">Team Performance</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-slate-500 text-sm mb-4">Win/Loss ratios and performance trends across seasons</p>
                <div className="space-y-2 text-xs text-slate-400">
                  <p>• Historical win rates</p>
                  <p>• Home vs Away performance</p>
                  <p>• Against the spread stats</p>
                </div>
                <Button variant="outline" className="mt-4 w-full" disabled>
                  Chart Coming Soon
                </Button>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-lg transition-all duration-300 border-2 hover:border-green-200">
              <CardHeader className="text-center">
                <TrendingUp className="w-12 h-12 mx-auto text-green-600 mb-2 group-hover:scale-110 transition-transform" />
                <CardTitle className="text-slate-700">Model Accuracy</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-slate-500 text-sm mb-4">ML prediction accuracy and confidence metrics</p>
                <div className="space-y-2 text-xs text-slate-400">
                  <p>• Prediction success rate</p>
                  <p>• Confidence calibration</p>
                  <p>• Model performance trends</p>
                </div>
                <Button variant="outline" className="mt-4 w-full" disabled>
                  Chart Coming Soon
                </Button>
              </CardContent>
            </Card>

            <Card className="group hover:shadow-lg transition-all duration-300 border-2 hover:border-purple-200">
              <CardHeader className="text-center">
                <PieChart className="w-12 h-12 mx-auto text-purple-600 mb-2 group-hover:scale-110 transition-transform" />
                <CardTitle className="text-slate-700">Betting Analytics</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-slate-500 text-sm mb-4">Betting patterns and market analysis</p>
                <div className="space-y-2 text-xs text-slate-400">
                  <p>• Line movement tracking</p>
                  <p>• Popular betting trends</p>
                  <p>• ROI calculations</p>
                </div>
                <Button variant="outline" className="mt-4 w-full" disabled>
                  Chart Coming Soon
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Main Analytics Area */}
          <div className="grid lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <Card className="h-96 border-2 border-dashed border-slate-300">
                <CardHeader className="text-center">
                  <Activity className="w-16 h-16 mx-auto text-slate-400 mb-4" />
                  <CardTitle className="text-xl text-slate-600">Interactive Dashboard</CardTitle>
                </CardHeader>
                <CardContent className="text-center py-8">
                  <p className="text-slate-500 mb-6 max-w-md mx-auto">
                    This area will display interactive charts and real-time analytics from your Firebase data and Python
                    models.
                  </p>
                  <div className="grid grid-cols-2 gap-4 text-sm text-slate-400 max-w-sm mx-auto">
                    <div className="text-left">
                      <p className="font-medium mb-2">Planned Features:</p>
                      <ul className="space-y-1">
                        <li>• Real-time data feeds</li>
                        <li>• Interactive filters</li>
                        <li>• Custom date ranges</li>
                      </ul>
                    </div>
                    <div className="text-left">
                      <p className="font-medium mb-2">Data Sources:</p>
                      <ul className="space-y-1">
                        <li>• Firebase Firestore</li>
                        <li>• Python ML models</li>
                        <li>• Historical game data</li>
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Quick Stats</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between items-center p-3 bg-blue-50 rounded">
                    <span className="text-sm font-medium">Total Predictions</span>
                    <Badge variant="secondary">Coming Soon</Badge>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-green-50 rounded">
                    <span className="text-sm font-medium">Accuracy Rate</span>
                    <Badge variant="secondary">Coming Soon</Badge>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-purple-50 rounded">
                    <span className="text-sm font-medium">Active Models</span>
                    <Badge variant="secondary">Coming Soon</Badge>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Recent Activity</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-slate-500 text-center py-8">
                    Recent predictions and model updates will appear here
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
