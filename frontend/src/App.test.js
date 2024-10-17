import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import App from './App';
import { BrowserRouter as Router } from 'react-router-dom';
import { BrowserRouter as Router } from 'react-router-dom';
import { API_BASE_URL } from './config';

// Increase the timeout for async operations
jest.setTimeout(10000);

describe('App component', () => {
  // Test 1: Verify that the main components of the app are rendered
  test('renders main app components', () => {
    render(
      <Router>
        <App />
      </Router>
    );
    
    const titleElement = screen.getByText(/MVC Template App/i);
    expect(titleElement).toBeInTheDocument();
    
    const inputElement = screen.getByPlaceholderText(/Enter a message/i);
    expect(inputElement).toBeInTheDocument();
    
    const buttonElement = screen.getByRole('button', { name: /Send/i });
    expect(buttonElement).toBeInTheDocument();
  });

  // Test 2: Verify that user input is correctly handled
  test('handles user input correctly', async () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter a message/i);
    
    await userEvent.type(inputElement, 'Hello, World!');
    
    expect(inputElement).toHaveValue('Hello, World!');
  });

  // Test 3: Verify form submission and response display
  test('submits form and displays response', async () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter a message/i);
    const buttonElement = screen.getByRole('button', { name: /Send/i });

    await userEvent.type(inputElement, 'Test message');
    fireEvent.click(buttonElement);

    await waitFor(() => {
      expect(screen.getByText(/Response from server:/i)).toBeInTheDocument();
    }, { timeout: 5000 });

    const responseElement = await screen.findByText(/"message": "Test message"/);
    expect(responseElement).toBeInTheDocument();
  });

  // Test 4: Verify handling of empty input
  test('handles empty input submission', async () => {
    render(<App />);
    const buttonElement = screen.getByRole('button', { name: /Send/i });

    fireEvent.click(buttonElement);

    await waitFor(() => {
      expect(screen.getByText(/Response from server:/i)).toBeInTheDocument();
    }, { timeout: 5000 });

    const responseElement = await screen.findByText(/"message": ""/);
    expect(responseElement).toBeInTheDocument();
  });

  // Test 5: Verify that multiple submissions update the displayed response
  test('updates displayed response on multiple submissions', async () => {
    render(<App />);
    const inputElement = screen.getByPlaceholderText(/Enter a message/i);
    const buttonElement = screen.getByRole('button', { name: /Send/i });

    // First submission
    await userEvent.type(inputElement, 'First message');
    fireEvent.click(buttonElement);

    await waitFor(() => {
      expect(screen.getByText(/Response from server:/i)).toBeInTheDocument();
    }, { timeout: 5000 });

    let responseElement = await screen.findByText(/"message": "First message"/);
    expect(responseElement).toBeInTheDocument();

    // Second submission
    await userEvent.clear(inputElement);
    await userEvent.type(inputElement, 'Second message');
    fireEvent.click(buttonElement);

    // Check if the response is updated
    responseElement = await screen.findByText(/"message": "Second message"/);
    expect(responseElement).toBeInTheDocument();
  });
});
