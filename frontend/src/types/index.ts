export type Message = {
  id: number;
  role: 'user' | 'ai';
  content: string;
  created_at: string;
};

export type Conversation = {
  messages: Message[];
};

export type WSMessage = {
  role?: 'user' | 'ai';
  content?: string;
  loading?: boolean;
  error?: string;
}; 