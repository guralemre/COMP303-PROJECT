import React, { useEffect } from 'react';
import AOS from 'aos';
import 'aos/dist/aos.css';
import './IntroPage.css';

const IntroPage = ({ onEnter }) => {
  useEffect(() => {
    AOS.init({
      duration: 1000, // Animasyonun süresi (ms)
      once: true, // Animasyon bir kere çalışsın
    });
  }, []);

  return (
    <div className="intro-page">
      {/* YouTube Video */}
      <div className="youtube-background">
        <iframe
          src="https://www.youtube.com/embed/o-8DNL2wFLY?autoplay=1&mute=1&loop=1&playlist=o-8DNL2wFLY"
          title="YouTube Video Background"
          frameBorder="0"
          allow="autoplay; fullscreen"
          allowFullScreen
          className="youtube-video"
        ></iframe>
      </div>

      {/* Content */}
      <div className="intro-content">
        <h1 data-aos="fade-up">Welcome to GameTECH!</h1>
        <button onClick={onEnter} className="btn btn-red" data-aos="fade-up">
          Click to Enter
        </button>
      </div>
    </div>
  );
};

export default IntroPage;
