document.addEventListener('DOMContentLoaded', function() {
    // Set up artist edit modal
    const editArtistModal = document.getElementById('editArtistModal');
    if (editArtistModal) {
        editArtistModal.addEventListener('show.bs.modal', function(event) {
            const button = event.relatedTarget;
            const artistId = button.getAttribute('data-artist-id');
            const artistName = button.getAttribute('data-artist-name');
            const artistDescription = button.getAttribute('data-artist-description');
            
            const modal = this;
            modal.querySelector('#edit-artist-id').value = artistId;
            modal.querySelector('#edit-artist-name').value = artistName;
            modal.querySelector('#edit-artist-description').value = artistDescription;
        });
    }
    
    // Confirm delete artist
    window.confirmDeleteArtist = function(artistId, artistName) {
        if (confirm(`Are you sure you want to delete the artist "${artistName}" and ALL their songs? This cannot be undone.`)) {
            document.getElementById(`delete-artist-form-${artistId}`).submit();
        }
    };
    
    // Confirm delete song
    window.confirmDeleteSong = function(songId, songName) {
        if (confirm(`Are you sure you want to delete the song "${songName}"? This cannot be undone.`)) {
            document.getElementById(`delete-song-form-${songId}`).submit();
        }
    };
    
    // Validate song upload form
    const uploadForm = document.getElementById('upload-song-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(event) {
            const artistId = document.getElementById('artist-id').value;
            const songName = document.getElementById('song-name').value;
            const songFile = document.getElementById('song-file').files[0];
            
            if (!artistId) {
                alert('Please select an artist');
                event.preventDefault();
                return;
            }
            
            if (!songName) {
                alert('Please enter a song name');
                event.preventDefault();
                return;
            }
            
            if (!songFile) {
                alert('Please select a song file');
                event.preventDefault();
                return;
            }
            
            if (!songFile.type.includes('audio')) {
                alert('Please select an audio file');
                event.preventDefault();
                return;
            }
        });
    }
});
