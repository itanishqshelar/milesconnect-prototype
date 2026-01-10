import axios from 'axios';
import dotenv from 'dotenv';

dotenv.config();

const WHAPI_URL = 'https://gate.whapi.cloud';
const ACCESS_TOKEN = process.env.WHAPI_ACCESS_TOKEN;
const ADMIN_NUMBER = '+91 9702102445';

if (!ACCESS_TOKEN) {
  throw new Error('WHAPI_ACCESS_TOKEN is not defined in the environment variables');
}

export async function sendDocument(to: string, mediaUrl: string, filename: string, caption: string) {
  try {
    const response = await axios.post(
      `${WHAPI_URL}/messages`,
      {
        from: ADMIN_NUMBER, // Static admin number
        to,
        type: 'document',
        document: {
          url: mediaUrl,
          filename,
          caption,
        },
      },
      {
        headers: {
          Authorization: `Bearer ${ACCESS_TOKEN}`,
          'Content-Type': 'application/json',
        },
      }
    );

    console.log('Document sent successfully:', response.data);
    return response.data;
  } catch (error) {
    console.error('Error sending document:', error.response?.data || error.message);
    throw error;
  }
}