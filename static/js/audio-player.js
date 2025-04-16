document.addEventListener('DOMContentLoaded', function() {
    // Register service worker for offline support
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(registration => {
                console.log('ServiceWorker registration successful');
            })
            .catch(err => {
                console.log('ServiceWorker registration failed: ', err);
            });
    }
    // Global audio player instance
    let globalAudioPlayer = null;
    let currentPlayingButton = null;
    
    // Function to play a song
    window.playSong = function(songId, button) {
        const url = `/play/${songId}`;
        
        // If we already have a player, stop it
        if (globalAudioPlayer) {
            globalAudioPlayer.pause();
            
            // Reset previous button icon if it exists
            if (currentPlayingButton) {
                currentPlayingButton.innerHTML = '<i class="fa fa-play"></i>';
            }
        }
        
        // If we're clicking the same button that's currently playing, just stop it
        if (currentPlayingButton === button) {
            globalAudioPlayer = null;
            currentPlayingButton = null;
            return;
        }
        
        // Create new audio player
        globalAudioPlayer = new Audio(url);
        currentPlayingButton = button;
        
        // Update button icon to show it's playing
        button.innerHTML = '<i class="fa fa-pause"></i>';
        
        // When audio ends, reset the button
        globalAudioPlayer.addEventListener('ended', function() {
            button.innerHTML = '<i class="fa fa-play"></i>';
            globalAudioPlayer = null;
            currentPlayingButton = null;
        });
        
        // Play the audio
        globalAudioPlayer.play().catch(error => {
            console.error('Error playing audio:', error);
            // Check if offline
            if (!navigator.onLine) {
                errorToast.innerHTML = `
                    <div class="d-flex">
                        <div class="toast-body">
                            You are offline. Only cached songs can be played.
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                `;
            
            // Show error message
            const errorToast = document.createElement('div');
            errorToast.className = 'toast align-items-center text-bg-danger border-0 position-fixed top-0 end-0 m-3';
            errorToast.setAttribute('role', 'alert');
            errorToast.setAttribute('aria-live', 'assertive');
            errorToast.setAttribute('aria-atomic', 'true');
            
            errorToast.innerHTML = `
                <div class="d-flex">
                    <div class="toast-body">
                        Error playing song. Please try again.
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            `;
            
            document.body.appendChild(errorToast);
            
            const toast = new bootstrap.Toast(errorToast);
            toast.show();
            
            // Reset button
            button.innerHTML = '<i class="fa fa-play"></i>';
            globalAudioPlayer = null;
            currentPlayingButton = null;
        });
    };
    
    // Function to download a song
    window.downloadSong = function(songId) {
        window.location.href = `/download/${songId}`;
    };
    
    // Function to search for songs
    window.searchSongs = function(artistId, artistName) {
        const query = document.getElementById('song-search').value;
        
        if (!query.trim()) {
            alert('Please enter a search term');
            return;
        }
        
        const resultsContainer = document.getElementById('search-results');
        resultsContainer.innerHTML = '<div class="spinner-border text-light" role="status"><span class="visually-hidden">Loading...</span></div>';
        
        // Show the modal
        const searchModal = new bootstrap.Modal(document.getElementById('searchSongsModal'));
        searchModal.show();
        
        // Make API request
        fetch(`/api/search_songs?query=${encodeURIComponent(query)}&artist=${encodeURIComponent(artistName)}`)
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = '';
                
                if (data.error) {
                    resultsContainer.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
                    return;
                }
                
                if (data.length === 0) {
                    resultsContainer.innerHTML = '<div class="alert alert-info">No songs found. Try a different search term.</div>';
                    return;
                }
                
                // Create a grid for song cards
                const songGrid = document.createElement('div');
                songGrid.className = 'row row-cols-1 row-cols-md-2 g-4';
                
                data.forEach(song => {
                    const songItem = document.createElement('div');
                    songItem.className = 'col';
                    
                    const thumbnailUrl = song.thumbnail || 'https://source.unsplash.com/100x100/?music,country';
                    const duration = song.duration || '';
                    
                    songItem.innerHTML = `
                        <div class="card h-100 shadow-sm">
                            <div class="card-body">
                                <div class="d-flex">
                                    <div class="flex-shrink-0 me-3">
                                        <img src="${thumbnailUrl}" alt="${song.name}" class="rounded" style="width: 60px; height: 60px; object-fit: cover;">
                                    </div>
                                    <div class="flex-grow-1">
                                        <h5 class="card-title mb-1">${song.name}</h5>
                                        <p class="card-text text-muted mb-0">
                                            <strong>${song.artist}</strong>
                                        </p>
                                        <div class="d-flex justify-content-between align-items-center mt-2">
                                            <span class="badge bg-dark">${song.source}</span>
                                            ${duration ? `<small class="text-muted"><i class="fas fa-clock me-1"></i>${duration}</small>` : ''}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="card-footer bg-transparent">
                                <button class="btn btn-primary w-100" onclick="addSongToArtist(${artistId}, '${song.name.replace(/'/g, "\\'")}', '${song.source_url}', '${song.source}')">
                                    <i class="fas fa-plus-circle me-2"></i> Add to Collection
                                </button>
                            </div>
                        </div>
                    `;
                    
                    songGrid.appendChild(songItem);
                });
                
                resultsContainer.appendChild(songGrid);
            })
            .catch(error => {
                console.error('Error searching songs:', error);
                resultsContainer.innerHTML = `<div class="alert alert-danger">Error searching for songs. Please try again.</div>`;
            });
    };
    
    // Function to add a song to an artist
    window.addSongToArtist = function(artistId, songName, sourceUrl, source) {
        const loadingToast = document.createElement('div');
        loadingToast.className = 'toast align-items-center text-bg-info border-0 position-fixed top-0 end-0 m-3';
        loadingToast.setAttribute('role', 'alert');
        loadingToast.setAttribute('aria-live', 'assertive');
        loadingToast.setAttribute('aria-atomic', 'true');
        
        loadingToast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                    Downloading song "${songName}"...
                </div>
            </div>
        `;
        
        document.body.appendChild(loadingToast);
        
        const toast = new bootstrap.Toast(loadingToast);
        toast.show();
        
        // Make API request to download the song
        fetch(`/api/download/${artistId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                song_name: songName,
                source_url: sourceUrl,
                source: source
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove the loading toast
            loadingToast.remove();
            
            const resultToast = document.createElement('div');
            
            if (data.success) {
                // Song was downloaded successfully
                resultToast.className = 'toast align-items-center text-bg-success border-0 position-fixed top-0 end-0 m-3';
                resultToast.innerHTML = `
                    <div class="d-flex">
                        <div class="toast-body">
                            Song "${songName}" was added successfully.
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                `;
                
                // Reload the page to show the new song
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                // There was an error
                resultToast.className = 'toast align-items-center text-bg-danger border-0 position-fixed top-0 end-0 m-3';
                resultToast.innerHTML = `
                    <div class="d-flex">
                        <div class="toast-body">
                            Error: ${data.error || 'Unknown error adding song'}
                        </div>
                        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                `;
            }
            
            document.body.appendChild(resultToast);
            const newToast = new bootstrap.Toast(resultToast);
            newToast.show();
            
            // Close the modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('searchSongsModal'));
            if (modal) {
                modal.hide();
            }
        })
        .catch(error => {
            console.error('Error downloading song:', error);
            
            // Remove the loading toast
            loadingToast.remove();
            
            // Show error toast
            const errorToast = document.createElement('div');
            errorToast.className = 'toast align-items-center text-bg-danger border-0 position-fixed top-0 end-0 m-3';
            errorToast.innerHTML = `
                <div class="d-flex">
                    <div class="toast-body">
                        Error downloading song. Please try again.
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            `;
            
            document.body.appendChild(errorToast);
            const newToast = new bootstrap.Toast(errorToast);
            newToast.show();
        });
    };
});
