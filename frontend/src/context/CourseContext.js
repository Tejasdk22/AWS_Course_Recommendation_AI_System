import React, { createContext, useContext, useReducer } from 'react';
import toast from 'react-hot-toast';

const CourseContext = createContext();

const initialState = {
  loading: false,
  results: null,
  error: null,
  query: '',
  major: '',
  studentType: '',
  careerGoal: ''
};

function courseReducer(state, action) {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_RESULTS':
      return { ...state, results: action.payload, loading: false, error: null };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    case 'SET_QUERY':
      return { ...state, query: action.payload };
    case 'SET_FORM_DATA':
      return { 
        ...state, 
        major: action.payload.major,
        studentType: action.payload.studentType,
        careerGoal: action.payload.careerGoal
      };
    case 'CLEAR_RESULTS':
      return { ...state, results: null, error: null };
    default:
      return state;
  }
}

export function CourseProvider({ children }) {
  const [state, dispatch] = useReducer(courseReducer, initialState);

  const submitCourseQuery = async (formData) => {
    try {
      dispatch({ type: 'SET_LOADING', payload: true });
      dispatch({ type: 'SET_FORM_DATA', payload: formData });
      
      // Construct the query
      const query = `I am a ${formData.major} ${formData.studentType} student at UTD. I want to become a ${formData.careerGoal}. What courses should I take?`;
      dispatch({ type: 'SET_QUERY', payload: query });

      // Call local backend API (fallback to AWS if needed)
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/career-guidance`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          major: formData.major,
          studentType: formData.studentType,
          careerGoal: formData.careerGoal
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      dispatch({ type: 'SET_RESULTS', payload: data });
      toast.success('Course recommendations generated successfully!');
      
    } catch (error) {
      console.error('Error submitting course query:', error);
      dispatch({ type: 'SET_ERROR', payload: error.message });
      toast.error('Failed to generate course recommendations. Please try again.');
    }
  };

  const clearResults = () => {
    dispatch({ type: 'CLEAR_RESULTS' });
  };

  const value = {
    ...state,
    submitCourseQuery,
    clearResults
  };

  return (
    <CourseContext.Provider value={value}>
      {children}
    </CourseContext.Provider>
  );
}

export function useCourse() {
  const context = useContext(CourseContext);
  if (context === undefined) {
    throw new Error('useCourse must be used within a CourseProvider');
  }
  return context;
}
