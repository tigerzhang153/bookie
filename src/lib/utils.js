import { clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs))
}

// Utility functions for your sports betting app
export function getConfidenceLevel(confidence) {
  if (confidence >= 80) return "high"
  if (confidence >= 60) return "medium"
  return "low"
}

export function formatCurrency(amount) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
  }).format(amount)
}

export function formatPercentage(value) {
  return `${value.toFixed(1)}%`
}

export function calculateEdge(predicted, line) {
  return Math.abs(predicted - line)
}

export function getBettingRecommendation(predicted, line) {
  return predicted > line ? "bet the OVER" : "bet the UNDER"
}
