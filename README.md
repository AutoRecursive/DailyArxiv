# ArXiv Browser

A modern ArXiv paper browser built with Tauri + Vue3 + Python, featuring a clean interface and convenient paper management functionality.

## Features

- 📱 Modern responsive interface
- 🔍 Paper category filtering
- 📖 Reading status tracking
- 🔗 Quick paper link opening
- 🌙 Light/Dark theme switching

## Tech Stack

- Frontend: Vue 3 + Vite + Pinia
- Backend: Python + FastAPI
- Desktop: Tauri
- Styling: SCSS

## Development Setup

### Prerequisites

- Node.js (>= 16)
- Python 3.8+
- Rust

### Installation Steps

1. Clone the repository
```bash
git clone https://github.com/yourusername/arxiv-paper-browser.git
cd arxiv-paper-browser
```

2. Setup backend
```bash
cd backend
python -m venv venv
source venv/bin/activate # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Setup frontend
```bash
cd daily-arxiv
npm install
```

### Running the Application

You can run the application in development mode:
```bash
npm run tauri dev
```

Or run frontend and backend separately:

Backend:
```bash
cd backend
python -m main
```

Frontend:
```bash
cd daily-arxiv
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Project Structure
```
.
├── backend/
│   ├── database/     # Database models and operations
│   ├── scraper/      # ArXiv API integration
│   ├── tests/        # Backend tests
│   └── main.py       # FastAPI application
├── daily-arxiv/      # Frontend application
│   ├── public/       # Static assets
│   └── src/
│       ├── assets/   # Styles and images
│       ├── components/# Vue components
│       ├── stores/   # Pinia stores
│       └── views/    # Page components
└── src-tauri/        # Tauri desktop application
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [ArXiv API](https://arxiv.org/help/api/index) for providing the paper data
- [Vue.js](https://vuejs.org/) for the excellent frontend framework
- [FastAPI](https://fastapi.tiangolo.com/) for the powerful backend framework
- [Tauri](https://tauri.app/) for the desktop application framework