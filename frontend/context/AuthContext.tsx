
import React, { createContext, useContext, useState, useEffect } from 'react';
import { User, AuthContextType } from '../types';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const login = (email: string, password: string) => {
    const mockUser = { id: 'u1', name: 'Arjun Reddy', email };
    localStorage.setItem('user', JSON.stringify(mockUser));
    setUser(mockUser);
  };

  const signup = (name: string, email: string) => {
    const mockUser = { id: 'u1', name, email };
    localStorage.setItem('user', JSON.stringify(mockUser));
    setUser(mockUser);
  };

  const logout = () => {
    localStorage.removeItem('user');
    setUser(null);
  };

  const isAuthenticated = !!user;

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
