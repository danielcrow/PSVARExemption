# DVSA PSVAR Exemption Application

A Next.js application for the DVSA PSVAR (Public Service Vehicle Accessibility Regulations) exemption application portal, integrated with watsonx Orchestrate AI agent.

## Features

- **DVSA Branding**: Official GOV.UK/DVSA styling and design patterns
- **watsonx Orchestrate Integration**: Embedded AI chat agent for guided application process
- **Responsive Design**: Mobile-friendly interface
- **Accessibility**: Built following GOV.UK accessibility standards

## Getting Started

### Prerequisites

- Node.js 18.x or higher
- npm or yarn

### Installation

1. Clone the repository or navigate to the project directory:

```bash
cd dvsa-psvar-app
```

2. Install dependencies:

```bash
npm install
```

3. Run the development server:

```bash
npm run dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## Deployment to Vercel

### Option 1: Deploy via Vercel CLI

1. Install Vercel CLI:

```bash
npm install -g vercel
```

2. Deploy:

```bash
vercel
```

3. Follow the prompts to link your project

### Option 2: Deploy via Vercel Dashboard

1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)

2. Go to [vercel.com](https://vercel.com) and sign in

3. Click "Add New Project"

4. Import your repository

5. Vercel will automatically detect Next.js and configure the build settings

6. Click "Deploy"

### Environment Variables

No environment variables are required as the watsonx Orchestrate configuration is embedded in the client-side code.

## Project Structure

```
dvsa-psvar-app/
├── app/
│   ├── layout.tsx          # Root layout with metadata
│   ├── page.tsx            # Main page with chat integration
│   ├── page.module.css     # Page-specific styles
│   └── globals.css         # Global styles
├── public/                 # Static assets
├── package.json            # Dependencies
├── tsconfig.json           # TypeScript configuration
├── next.config.js          # Next.js configuration
└── README.md              # This file
```

## watsonx Orchestrate Configuration

The application is configured to connect to:
- **Orchestration ID**: `20250430-1552-4383-00f2-8e9318aa2f1b_20250501-1821-5146-80d6-0ef0535f5342`
- **Host URL**: `https://eu-central-1.dl.watson-orchestrate.ibm.com`
- **Agent ID**: `a48c5531-927d-423b-b3d6-c20a291ac99a`

To update these values, edit the `wxOConfiguration` object in `app/page.tsx`.

## Customization

### Updating Agent Configuration

Edit `app/page.tsx` and modify the `wxOConfiguration` object:

```typescript
(window as any).wxOConfiguration = {
  orchestrationID: "your-orchestration-id",
  hostURL: "your-host-url",
  rootElementID: "chat-root",
  chatOptions: {
    agentId: "your-agent-id",
  }
};
```

### Styling

- Global styles: `app/globals.css`
- Page-specific styles: `app/page.module.css`
- DVSA colors are defined in the CSS files following GOV.UK design system

## Build for Production

```bash
npm run build
npm start
```

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [watsonx Orchestrate Documentation](https://developer.watson-orchestrate.ibm.com)
- [GOV.UK Design System](https://design-system.service.gov.uk/)
- [Vercel Deployment](https://vercel.com/docs)

## License

Crown Copyright