import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
});

export async function postQuery({ text, pincode, situation_type, history }) {
  const body = { text };
  if (history) body.history = history;
  if (pincode) body.pincode = pincode;
  if (situation_type) body.situation_type = situation_type;
  const { data } = await api.post('/query', body);
  return data;
}

export async function generateLetter({ type, user_name, district, date, details }) {
  const { data } = await api.post('/generate-letter', {
    type,
    user_name,
    district,
    date,
    details,
  });
  return data;
}

export async function getDLSA(pincode, domain = 'general') {
  const { data } = await api.post('/locate-office', { pincode, domain });
  return data;
}
