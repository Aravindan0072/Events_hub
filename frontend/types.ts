
export interface Event {
  id: string;
  title: string;
  description: string;
  date_text: string;
  location: string;
  image_url: string;
  category: string;
  city: string;
  is_free: boolean;
  source_type: 'internal' | 'external';
  external_url?: string;
  views: number;
  clicks: number;
}

export interface User {
  id: string;
  name: string;
  email: string;
}

export interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => void;
  signup: (name: string, email: string) => void;
  logout: () => void;
  isAuthenticated: boolean;
}
