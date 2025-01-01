import React, { useState } from 'react';
import './Auth.css';

const SignIn = ({ onEnter }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [isForgotPassword, setIsForgotPassword] = useState(false);
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [resetSuccess, setResetSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      if (isForgotPassword) {
        // Şifre sıfırlama isteği
        const response = await fetch('http://localhost:5000/api/reset', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || 'Şifre sıfırlama başarısız oldu');
        }

        setResetSuccess(true);
        setTimeout(() => {
          setIsForgotPassword(false);
          setResetSuccess(false);
        }, 3000);
      } else {
        // Normal giriş/kayıt isteği
        const endpoint = isLogin ? '/api/login' : '/api/signup';
        const response = await fetch(`http://localhost:5000${endpoint}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: formData.username,
            password: formData.password,
            ...(isLogin ? {} : { email: formData.email })
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.error || 'Bir hata oluştu');
        }

        if (data.access_token) {
          localStorage.setItem('token', data.access_token);
          localStorage.setItem('username', formData.username);
          onEnter();
        }
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const resetForm = () => {
    setFormData({
      username: '',
      email: '',
      password: ''
    });
    setError(null);
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2>
          {isForgotPassword 
            ? 'Forgot Password' 
            : (isLogin ? 'Login' : 'Register')}
        </h2>
        
        {error && <div className="auth-error">{error}</div>}
        {resetSuccess && (
          <div className="auth-success">Your password has been reset successfully!</div>
        )}
        
        <form onSubmit={handleSubmit}>
          {!isForgotPassword && (
            <div className="form-group">
              <input
                type="text"
                name="username"
                placeholder="Username"
                value={formData.username}
                onChange={handleChange}
                required
              />
            </div>
          )}
          
          {(isForgotPassword || !isLogin) && (
            <div className="form-group">
              <input
                type="email"
                name="email"
                placeholder="E-posta"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>
          )}
          
          <div className="form-group">
            <input
              type="password"
              name="password"
              placeholder={isForgotPassword ? "New Password" : "Password"}
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>
          
          <button type="submit" className="auth-button" disabled={loading}>
            {loading ? 'İşleniyor...' : (
              isForgotPassword ? 'Forgot Password' :
              (isLogin ? 'Login' : 'Register')
            )}
          </button>
        </form>
        
        <div className="auth-links">
          {!isForgotPassword && (
            <button 
              onClick={() => {
                setIsForgotPassword(true);
                resetForm();
              }}
              className="forgot-password-link"
            >
              Forgot password?
            </button>
          )}
          
          <div className="auth-switch">
            {!isForgotPassword && (
              <p>
                {isLogin ? 'Don\'t have an account?' : 'Already have an account?'}
                <button 
                  onClick={() => {
                    setIsLogin(!isLogin);
                    resetForm();
                  }}
                  className="switch-button"
                >
                  {isLogin ? 'Register' : 'Login'}
                </button>
              </p>
            )}
          </div>

          {isForgotPassword && (
            <button 
              onClick={() => {
                setIsForgotPassword(false);
                resetForm();
              }}
              className="back-to-login"
            >
              Back to Login
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default SignIn; 