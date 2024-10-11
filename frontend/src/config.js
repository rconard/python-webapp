const getBaseUrl = () => {
  if (process.env.NODE_ENV === 'test') {
    return 'http://localhost:5000';
  }
  return '';
};

export const API_BASE_URL = getBaseUrl();
