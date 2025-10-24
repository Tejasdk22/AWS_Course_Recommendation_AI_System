import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Header from './components/Header';
import Home from './pages/Home';
import CourseRecommendations from './pages/CourseRecommendations';
import About from './pages/About';
import { CourseProvider } from './context/CourseContext';

function App() {
  return (
    <CourseProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Header />
          <main>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/course-recommendations" element={<CourseRecommendations />} />
              <Route path="/about" element={<About />} />
            </Routes>
          </main>
          <Toaster 
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
            }}
          />
        </div>
      </Router>
    </CourseProvider>
  );
}

export default App;