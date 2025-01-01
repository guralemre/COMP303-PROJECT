import './App.css';
import React, { useState } from 'react';
import Header from './components/Header/Header';
import WhatWeDo from './components/WhatWeDo/WhatWeDo';
import Features from './components/Features/Features';
import Packages from './components/Packages/Packages';
import Projects from './components/Projects/Projects';
import Team from './components/Team/Team';
import Support from './components/Supports/Support';
import Footer from './components/Footer/Footer';
import IntroPage from './components/IntroPage/IntroPage';
import SignIn from './components/Auth/SignIn';

function App() {
  const [showIntro, setShowIntro] = useState(true);
  const [showSignIn, setShowSignIn] = useState(false);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const enterSite = () => {
    setShowIntro(false);
    setShowSignIn(true);
  };

  const handleAuthentication = () => {
    setShowSignIn(false);
    setIsAuthenticated(true);
  };

  return (
    <div className="App">
      {showIntro ? (
        <IntroPage onEnter={enterSite} />
      ) : showSignIn ? (
        <SignIn onEnter={handleAuthentication} />
      ) : (
        <>
          <Header />
          <WhatWeDo />
          <Features />
          <Packages />
          <Projects />
          <Team />
          <Support />
          <Footer />
        </>
      )}
    </div>
  );
}

export default App;
