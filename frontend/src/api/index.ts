import axios from 'axios';
import type { Conversation } from '../types';
import { config } from '../config';

export async function fetchConversation(): Promise<Conversation> {
  const res = await axios.get(`${config.API_BASE}/history`);
  return res.data;
} 