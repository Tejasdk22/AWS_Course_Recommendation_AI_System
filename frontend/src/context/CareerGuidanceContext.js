import React, { createContext, useContext, useReducer, useEffect } from 'react';
import axios from 'axios';

const CareerGuidanceContext = createContext();

const initialState = {
  query: '',
  response: null,
  loading: false,
  error: null,
  sessionId: null,
  history: [],
  systemStatus: null
};

const actionTypes = {
  SET_QUERY: 'SET_QUERY',
  SET_LOADING: 'SET_LOADING',
  SET_RESPONSE: 'SET_RESPONSE',
  SET_ERROR: 'SET_ERROR',
  SET_SESSION_ID: 'SET_SESSION_ID',
  ADD_TO_HISTORY: 'ADD_TO_HISTORY',
  CLEAR_HISTORY: 'CLEAR_HISTORY',
  SET_SYSTEM_STATUS: 'SET_SYSTEM_STATUS'
};

function careerGuidanceReducer(state, action) {
  switch (action.type) {
    case actionTypes.SET_QUERY:
      return { ...state, query: action.payload };
    
    case actionTypes.SET_LOADING:
      return { ...state, loading: action.payload };
    
    case actionTypes.SET_RESPONSE:
      return { 
        ...state, 
        response: action.payload, 
        loading: false, 
        error: null 
      };
    
    case actionTypes.SET_ERROR:
      return { 
        ...state, 
        error: action.payload, 
        loading: false 
      };
    
    case actionTypes.SET_SESSION_ID:
      return { ...state, sessionId: action.payload };
    
    case actionTypes.ADD_TO_HISTORY:
      return { 
        ...state, 
        history: [action.payload, ...state.history].slice(0, 10) // Keep last 10
      };
    
    case actionTypes.CLEAR_HISTORY:
      return { ...state, history: [] };
    
    case actionTypes.SET_SYSTEM_STATUS:
      return { ...state, systemStatus: action.payload };
    
    default:
      return state;
  }
}

export function CareerGuidanceProvider({ children }) {
  const [state, dispatch] = useReducer(careerGuidanceReducer, initialState);

  // API base URL - in production, this would be your deployed backend
  const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const setQuery = (query) => {
    dispatch({ type: actionTypes.SET_QUERY, payload: query });
  };

  const setLoading = (loading) => {
    dispatch({ type: actionTypes.SET_LOADING, payload: loading });
  };

  const setResponse = (response) => {
    dispatch({ type: actionTypes.SET_RESPONSE, payload: response });
  };

  const setError = (error) => {
    dispatch({ type: actionTypes.SET_ERROR, payload: error });
  };

  const setSessionId = (sessionId) => {
    dispatch({ type: actionTypes.SET_SESSION_ID, payload: sessionId });
  };

  const addToHistory = (query, response) => {
    const historyItem = {
      id: Date.now(),
      query,
      response,
      timestamp: new Date().toISOString()
    };
    dispatch({ type: actionTypes.ADD_TO_HISTORY, payload: historyItem });
  };

  const clearHistory = () => {
    dispatch({ type: actionTypes.CLEAR_HISTORY });
  };

  const setSystemStatus = (status) => {
    dispatch({ type: actionTypes.SET_SYSTEM_STATUS, payload: status });
  };

  const submitQuery = async (query) => {
    if (!query.trim()) {
      setError('Please enter a question');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/api/career-guidance`, {
        query: query.trim(),
        sessionId: state.sessionId || generateSessionId()
      });

      const data = response.data;
      
      setResponse(data);
      setSessionId(data.session_id);
      addToHistory(query, data);
      
    } catch (error) {
      console.error('Error submitting query:', error);
      
      if (error.response) {
        setError(`Server error: ${error.response.data.message || error.response.statusText}`);
      } else if (error.request) {
        setError('Network error: Unable to connect to the server');
      } else {
        setError('An unexpected error occurred');
      }
    }
  };

  const generateSessionId = () => {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  };

  const checkSystemStatus = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/health`);
      setSystemStatus(response.data);
    } catch (error) {
      console.error('Error checking system status:', error);
      setSystemStatus({ status: 'offline', error: error.message });
    }
  };

  // Check system status on mount
  useEffect(() => {
    checkSystemStatus();
  }, []);

  const value = {
    ...state,
    setQuery,
    setLoading,
    setResponse,
    setError,
    setSessionId,
    addToHistory,
    clearHistory,
    setSystemStatus,
    submitQuery,
    checkSystemStatus
  };

  return (
    <CareerGuidanceContext.Provider value={value}>
      {children}
    </CareerGuidanceContext.Provider>
  );
}

export function useCareerGuidance() {
  const context = useContext(CareerGuidanceContext);
  if (!context) {
    throw new Error('useCareerGuidance must be used within a CareerGuidanceProvider');
  }
  return context;
}
