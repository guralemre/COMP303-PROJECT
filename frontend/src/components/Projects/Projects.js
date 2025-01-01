import React, { useState, useEffect } from 'react';
import './Projects.css';

const Projects = () => {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [platform, setPlatform] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  
  // sayfalama için state'ler
  const [currentPage, setCurrentPage] = useState(1);
  const [gamesPerPage] = useState(12); 
  const [addingToFavorites, setAddingToFavorites] = useState({});
  const [showFavorites, setShowFavorites] = useState(false);
  const [favorites, setFavorites] = useState([]);
  const [loadingFavorites, setLoadingFavorites] = useState(false);

  useEffect(() => {
    fetchGames();
  }, [platform, searchTerm]);

  const fetchGames = async () => {
    try {
      setLoading(true);
      let url = `http://localhost:5000/api/games?platform=${platform}`;
      if (searchTerm) {
        url += `&search=${searchTerm}`;
      }
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Oyunlar yüklenirken bir hata oluştu');
      }
      const data = await response.json();
      setGames(data.games);
      setCurrentPage(1); // Yeni arama yapıldığında ilk sayfaya dön
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Sayfalama 
  const indexOfLastGame = currentPage * gamesPerPage;
  const indexOfFirstGame = indexOfLastGame - gamesPerPage;
  const currentGames = games.slice(indexOfFirstGame, indexOfLastGame);
  const totalPages = Math.ceil(games.length / gamesPerPage);

  // sayfa değiştirme
  const paginate = (pageNumber) => {
    setCurrentPage(pageNumber);
    window.scrollTo(0, 0); 
  };

  // sayfalama komponenti
  const Pagination = () => {
    const pageNumbers = [];
    const maxVisiblePages = 5;
    
    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
    
    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }

    for (let i = startPage; i <= endPage; i++) {
      pageNumbers.push(i);
    }

    return (
      <div className="pagination">
        <button 
          onClick={() => paginate(1)} 
          disabled={currentPage === 1}
          className="pagination-button"
        >
          First
        </button>
        <button 
          onClick={() => paginate(currentPage - 1)} 
          disabled={currentPage === 1}
          className="pagination-button"
        >
          &#8249;
        </button>
        {pageNumbers.map(number => (
          <button
            key={number}
            onClick={() => paginate(number)}
            className={`pagination-button ${currentPage === number ? 'active' : ''}`}
          >
            {number}
          </button>
        ))}
        <button 
          onClick={() => paginate(currentPage + 1)} 
          disabled={currentPage === totalPages}
          className="pagination-button"
        >
          &#8250;
        </button>
        <button 
          onClick={() => paginate(totalPages)} 
          disabled={currentPage === totalPages}
          className="pagination-button"
        >
          Last
        </button>
      </div>
    );
  };

  // favorilere ekleme
  const addToFavorites = async (game) => {
    try {
      setAddingToFavorites(prev => ({ ...prev, [game.name]: true }));
      const token = localStorage.getItem('token');
      
      if (!token) {
        throw new Error('Please login');
      }

      const response = await fetch('http://localhost:5000/api/favorites', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          id: game.appid || game.name,
          name: game.name,
          platform: game.platform,
          price: game.price,
          price_formatted: game.price_formatted
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Favorilere eklenirken bir hata oluştu');
      }

      alert('Game has been added to favorites!');
    } catch (err) {
      alert(err.message);
    } finally {
      setAddingToFavorites(prev => ({ ...prev, [game.name]: false }));
    }
  };

  // favorileri getirme 
  const fetchFavorites = async () => {
    try {
      setLoadingFavorites(true);
      const token = localStorage.getItem('token');
      const username = localStorage.getItem('username'); // Username'i localStorage'dan al
      
      if (!token || !username) {
        throw new Error('Please login');
      }

      const response = await fetch(`http://localhost:5000/api/favorites?username=${username}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Error loading favorites');
      }

      setFavorites(data.favorites);
      setShowFavorites(true);
    } catch (err) {
      alert(err.message);
    } finally {
      setLoadingFavorites(false);
    }
  };

  // favorilerden çıkarma
  const removeFavorite = async (gameId) => {
    try {
      const token = localStorage.getItem('token');
      
      if (!token) {
        throw new Error('Please login');
      }

      const response = await fetch(`http://localhost:5000/api/favorites/${gameId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Error removing game from favorites');
      }

      // favorileri güncelle
      setFavorites(favorites.filter(game => game.id !== gameId));
      alert('Game has been removed from favorites!');

    } catch (err) {
      alert(err.message);
    }
  };

  return (
    <section className='projects section-padding' id='projects'>
      <div className='container'>
        <div className='section-header'>
          <div className='section-title'>
            <h3 className='text-brown'>Game List</h3>
          </div>
          <button 
            className={`favorites-toggle ${showFavorites ? 'active' : ''}`}
            onClick={() => {
              if (!showFavorites) {
                fetchFavorites();
              } else {
                setShowFavorites(false);
              }
            }}
          >
            {loadingFavorites ? 'Loading...' : (showFavorites ? 'Game Lists' : 'Favorites')}
          </button>
        </div>

        <div className='filters'>
          <select 
            value={platform} 
            onChange={(e) => setPlatform(e.target.value)}
            className='platform-select'
          >
            <option value="all">All Platforms</option>
            <option value="steam">Steam</option>
            <option value="epic">Epic</option>
            <option value="gog">GOG</option>
          </select>

          <input
            type="text"
            placeholder="Search game..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className='search-input'
          />
        </div>

        {loading && <div className="loading">Loading...</div>}
        {error && <div className="error">{error}</div>}

        <div className='projects-content'>
          {showFavorites ? (
            favorites.length > 0 ? (
              favorites.map((game, index) => (
                <div key={index} className='projects-item'>
                  <div className='projects-item-content'>
                    <h4>{game.name}</h4>
                    <p className='text'>Platform: {game.platform}</p>
                    <p className='text'>Fiyat: {game.price_formatted}</p>
                    {game.discount && (
                      <p className='text discount'>Discount: {game.discount}</p>
                    )}
                    <button
                      className='remove-favorite-button'
                      onClick={() => removeFavorite(game.id)}
                    >
                      Remove Favorite
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <div className="no-results">No favorites found</div>
            )
          ) : (
            currentGames.map((game, index) => (
              <div key={index} className='projects-item'>
                <div className='projects-item-content'>
                  <h4>{game.name}</h4>
                  <p className='text'>Platform: {game.platform}</p>
                  <p className='text'>Price: {game.price_formatted}</p>
                  {game.discount && (
                    <p className='text discount'>Discount: {game.discount}</p>
                  )}
                  <button
                    className='favorite-button'
                    onClick={() => addToFavorites(game)}
                    disabled={addingToFavorites[game.name]}
                  >
                    {addingToFavorites[game.name] ? 'Adding...' : 'Add to Favorites'}
                  </button>
                </div>
              </div>
            ))
          )}
        </div>

        {games.length === 0 && !loading && (
          <div className="no-results">Game not found</div>
        )}

        {games.length > 0 && <Pagination />}
      </div>
    </section>
  );
};

export default Projects; 