import type { Metadata } from 'next'
import './globals.css'
import './wxo-override.css'

export const metadata: Metadata = {
  title: 'PSVAR Exemption Application - DVSA',
  description: 'Apply for an exemption from Public Service Vehicle Accessibility Regulations (PSVAR) for home-to-school transport services',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" style={{ margin: 0, padding: 0, height: '100%' }}>
      <body style={{ margin: 0, padding: 0, height: '100%' }}>{children}</body>
    </html>
  )
}

// Made with Bob
