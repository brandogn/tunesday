# About

A fun little tracker that displays and archives any playlist (default is `5VAWBjNvITrvEFSYwgq5iK`, ["As of Recent" on spotify](https://open.spotify.com/playlist/5VAWBjNvITrvEFSYwgq5iK))

## Setup

### 1. Environment Variables

Create a `.env` file with your Spotify API credentials:

```env
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

### 2. Install Dependencies

Install all python requirements:
```
pip install -r requirements.txt
```

Alternatively in a virtual python enviornment (recommendend):
```bash
VENV=.venv
python -m venv $VENV
source $VENV/bin/activate
pip install -r requirements.txt
```

### 3. Test the Setup

```bash
# Test playlist fetching
python spotify_fetcher.py

# Run the web app locally
python app.py
```

Visit `http://localhost:5000` to see the website.

### Changing which playlist you want to modify

Get the ID from spotify (format should be `https://open.spotify.com/playlist/{playlist_id}`) and change `DEFAULT_PLAYLIST_ID` in `spotify_fetcher.py`:

```
DEFAULT_PLAYLIST_ID = "5VAWBjNvITrvEFSYwgq5iK"
```

## Deployment Options

### Railway (Recommended - Simplest)

1. Push your code to GitHub
2. Go to [Railway.app](https://railway.app)
3. Connect your GitHub repository
4. Add environment variables in Railway dashboard
5. Deploy automatically

## GitHub Actions Setup

The automatic Tuesday updates require GitHub Secrets:

1. Go to your repository Settings → Secrets and variables → Actions
2. Add these secrets:
   - `SPOTIFY_CLIENT_ID`: Your Spotify client ID
   - `SPOTIFY_CLIENT_SECRET`: Your Spotify client secret

## Future Features

Feel free to request features. Some features I would like to add:
- I wish I could implement a button that could add all of these songs to a playlist tbh
- Letting people create their own "tunesday" archive - user/auth is something I might consider idk, this is a pet project atm
<!-- 
## Manual Updates

To manually update the playlist:

1. **Via Web**: Visit `https://your-domain.com/admin/update`
2. **Via Command**: Run `python spotify_fetcher.py`
3. **Via GitHub**: Go to Actions tab → "Update Playlist" → "Run workflow"

## Troubleshooting

- **No data showing**: Check that GitHub Actions ran successfully and committed data files
- **API errors**: Verify your Spotify credentials are correct
- **Deployment issues**: Check that all environment variables are set in your hosting platform -->