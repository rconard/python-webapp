import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter as Router } from 'react-router-dom';
import userEvent from '@testing-library/user-event';
import '@testing-library/jest-dom';
import App from './App';
import { API_BASE_URL } from './config';


// Increase the timeout for async operations
jest.setTimeout(10000);

describe('App component', () => {
  beforeEach(() => {
    render(
      <Router>
        <App />
      </Router>
    );
  });
  // Test 0: Verify that the navigation bar renders correctly
  test('renders navigation bar', async () => {

    const homeLink = await screen.findByText(/Home/i);
    const aboutLink = await screen.findByText(/About/i);

    expect(homeLink).toBeInTheDocument();
    expect(aboutLink).toBeInTheDocument();
  });
    const aboutLink = await screen.findByText(/About/i);

    expect(homeLink).toBeInTheDocument();
    expect(aboutLink).toBeInTheDocument();
  });
  test('renders main app components', () => {

    const titleElement = screen.getByText(/MVC Template App/i);
    expect(titleElement).toBeInTheDocument();

    const inputElement = screen.getAllByPlaceholderText(/Enter a message/i)[0];
    expect(inputElement).toBeInTheDocument();

    const buttonElement = screen.getAllByRole('button', { name: /Send/i })[0];
    expect(buttonElement).toBeInTheDocument();
  });
    expect(titleElement).toBeInTheDocument();

    const inputElement = screen.getAllByPlaceholderText(/Enter a message/i)[0];
    expect(inputElement).toBeInTheDocument();

    const buttonElement = screen.getAllByRole('button', { name: /Send/i })[0];
    expect(buttonElement).toBeInTheDocument();
  });

  // Test 2: Verify that user input is correctly handled
  test('handles user input correctly', async () => {
    const inputElement = screen.getAllByPlaceholderText(/Enter a message/i)[0];

    await userEvent.type(inputElement, 'Hello, World!');

    expect(inputElement).toHaveValue('Hello, World!');
  });

  // Test 3: Verify form submission and response display
  test('submits form and displays response', async () => {
    const inputElement = screen.getByPlaceholderText(/Enter a message/i);
    const buttonElement = screen.getAllByRole('button', { name: /Send/i })[0];

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

  // Test 6: Verify navigation to About page
  test('navigates to About page', async () => {
    render(<App />);

    const aboutLink = screen.getAllByText(/About/i)[0];
    fireEvent.click(aboutLink);

    await waitFor(() => {
      expect(screen.getByText(/This is the about page/i)).toBeInTheDocument();
    });
  });

  // Test 7: Verify API error handling
  test('handles API error correctly', async () => {
    global.fetch = jest.fn(() =>
      Promise.resolve({
        ok: false,
        status: 500,
      })
    );

    const inputElement = await screen.findByPlaceholderText(/Enter a message/i);
    const buttonElement = screen.getByRole('button', { name: /Send/i });

    await userEvent.type(inputElement, 'Test message');
    fireEvent.click(buttonElement);

    await waitFor(() => {
      expect(screen.getByText(/An error occurred/i)).toBeInTheDocument();
    });
  });

  // Test 8: Verify loading state during API call
  test('displays loading state during API call', async () => {
    global.fetch = jest.fn(() =>
      new Promise((resolve) => setTimeout(() => resolve({
        ok: true,
        json: () => Promise.resolve({ message: 'Test message' }),
      }), 1000))
    );

    const inputElement = await screen.findByPlaceholderText(/Enter a message/i);
    const buttonElement = screen.getByRole('button', { name: /Send/i });

    await userEvent.type(inputElement, 'Test message');
    fireEvent.click(buttonElement);

    expect(screen.getByText(/Loading.../i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(/"message": "Test message"/)).toBeInTheDocument();
    });
  });
});
