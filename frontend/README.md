# UTD Career Guidance AI - Frontend

A modern React frontend for the UTD Career Guidance AI System, built with Tailwind CSS and designed for AWS Amplify deployment.

## Features

- **Modern React UI** with Tailwind CSS
- **Responsive Design** for all devices
- **Real-time Career Guidance** powered by AI agents
- **Course Recommendations** tailored to your major
- **Market Analysis** with current job trends
- **Career Progression** from entry to senior level

## Tech Stack

- React 18
- Tailwind CSS
- React Router
- Axios for API calls
- Lucide React for icons
- Framer Motion for animations
- React Hot Toast for notifications

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

### Building for Production

```bash
npm run build
```

This builds the app for production to the `build` folder.

## Deployment

### AWS Amplify

1. Connect your GitHub repository to AWS Amplify
2. The `amplify.yml` file will automatically configure the build process
3. Deploy with a single click

### Manual Deployment

1. Build the project:
```bash
npm run build
```

2. Upload the `build` folder contents to your web server

## Configuration

Update the API endpoint in `src/context/CareerContext.js`:

```javascript
const response = await fetch('https://your-api-gateway-url.amazonaws.com/prod/career-guidance', {
  // ... rest of the configuration
});
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   └── Header.js       # Navigation header
├── context/            # React context for state management
│   └── CareerContext.js # Career guidance state
├── pages/              # Page components
│   ├── Home.js         # Landing page
│   ├── CareerGuidance.js # Main career guidance form
│   └── About.js        # About page
├── App.js              # Main app component
├── index.js            # App entry point
└── index.css           # Global styles with Tailwind
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from Create React App (one-way operation)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.
