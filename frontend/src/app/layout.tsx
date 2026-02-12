import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "Code Architect - Gemini 3 Hackathon",
  description: "Autonomous code analysis powered by Gemini 3 Pro",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
