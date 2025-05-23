
# LegalAI - AI-Powered Legal Document Analyzer

![LegalAI](https://via.placeholder.com/1200x630/3b82f6/ffffff?text=LegalAI)

LegalAI is a modern web application designed for analyzing legal documents using artificial intelligence. The platform helps legal professionals identify risks, review clauses, and get AI-powered suggestions to improve their legal documents.

## Features

- **Document Upload**: Upload legal documents for analysis
- **Document Review**: Examine the content with AI assistance
- **Risk Analysis**: Identify potential legal risks in your documents
- **AI Suggestions**: Get AI-powered recommendations for improvements
- **Document Summary**: Review comprehensive document insights

## Tech Stack

- **Frontend**: React, TypeScript, Tailwind CSS, Framer Motion
- **UI Components**: shadcn/ui
- **Charts**: Recharts
- **Animations**: Framer Motion
- **Icons**: Lucide React

## Getting Started

### Prerequisites

- Node.js (v18 or later)
- npm or yarn

### Installation

1. Clone the repository:

```bash
git clone [repository-url]
cd legal-ai
```

2. Install dependencies:

```bash
npm install
# or
yarn install
```

3. Start the development server:

```bash
npm run dev
# or
yarn dev
```

4. Open your browser and visit `http://localhost:5173`

## Project Structure

```
legal-ai/
├── public/              # Static files
├── src/                 # Source code
│   ├── components/      # Reusable components
│   │   ├── dashboard/   # Dashboard-specific components
│   │   ├── layout/      # Layout components (sidebar, navbar)
│   │   ├── theme/       # Theme components
│   │   └── ui/          # UI components (shadcn/ui)
│   ├── hooks/           # Custom hooks
│   ├── lib/             # Utility functions
│   ├── pages/           # Page components
│   └── ...
└── ...
```

## Usage

1. **Document Upload**: Click on "Upload" in the sidebar and upload your legal document
2. **Document Review**: Navigate to the "Review" tab to examine the document's content
3. **Risk Analysis**: Check the "Risks" section for potential legal issues
4. **AI Suggestions**: Review the "Suggestions" tab for AI-powered recommendations
5. **Document Summary**: See a comprehensive overview in the "Summary" section

## Customization

### Theme

The application supports both light and dark modes. Use the theme toggle in the top navigation bar to switch between modes.

### Sidebar

The sidebar can be collapsed for a more focused view. Click the toggle button in the sidebar header.

## License

[MIT License](LICENSE)

## Acknowledgments

- [shadcn/ui](https://ui.shadcn.com/) for beautiful UI components
- [Recharts](https://recharts.org/) for data visualization
- [Framer Motion](https://www.framer.com/motion/) for animations
- [Lucide Icons](https://lucide.dev/) for the icon set
