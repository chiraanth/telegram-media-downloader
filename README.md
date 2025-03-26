# 📥 Telegram Media Downloader

A polished, efficient, and containerized tool to automatically download media from Telegram groups or channels using [Telethon](https://github.com/LonamiWebs/Telethon). Built with simplicity and power in mind.






---

## ✨ Features

- 📂 Automatically downloads media from Telegram groups/channels
- 🔧 Easy `.env`-based configuration
- 📉 Real-time progress bars with `tqdm`
- ♻️ Retry logic with exponential backoff using `retrying`
- 🧼 Filename sanitization to prevent OS conflicts
- 🧾 Logging with rotation using `loguru`
- 🐳 Containerized using Docker and Docker Compose
- 🔄 File permission fix support for Docker containers
- 🧪 Local and containerized run modes supported
- 💾 Persistent download directory

---

## 📁 Project Structure

```
telegram-media-downloader/
├── .env.sample            # Sample environment variables
├── .gitignore             # Git ignore rules
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker build instructions
├── movie_download.py      # Main Telegram downloader script
├── requirements.txt       # Python dependency list
└── downloads/             # Folder for downloaded media files
```

---

## ⚙️ Setup & Configuration

### 🔐 Step 1: Prepare `.env`

1. Copy the example `.env.sample` to a new `.env` file:

```bash
cp .env.sample .env
```

2. Fill in the required fields:

```dotenv
API_ID=your_api_id_here
API_HASH=your_api_hash_here
PHONE_NUMBER=your_phone_number_here
TARGET_GROUP=https://t.me/your-group-url
INSIDE_DOCKER=0
```

3. **Get your Telegram API credentials**:

   - Go to [my.telegram.org](https://my.telegram.org/auth)
   - Log in with your phone number
   - Click on "API Development Tools"
   - Enter a name, a short URL, and choose any platform (e.g., Desktop)
   - Copy your **API ID** and **API Hash**

4. Make sure the `TARGET_GROUP` is either:

   - A valid `@username` of a Telegram group/channel you belong to
   - Or a `https://t.me/your-group` public URL

5. Do **not** add quotes around any values in `.env`.

---

## 🧪 Running Locally (Python)

### 📦 Step 2: Install Python and Dependencies

1. Ensure Python 3.9 or higher is installed:

```bash
python --version
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install project dependencies:

```bash
pip install -r requirements.txt
```

### ▶️ Step 3: Run the Bot Locally

1. Execute the script:

```bash
python movie_download.py
```

2. On first run, you will:

   - Be prompted for OTP (Telegram verification)
   - Generate a session file `session_name.session`

3. Media files will be saved to:

```
downloads/telegram/
```

4. You can safely terminate and restart — the session is preserved.

---

## 🐳 Docker Deployment

### 🔨 Step 1: Build the Docker Image

Ensure Docker is installed, then:

```bash
docker build -t telegram-downloader .
```

### 🚀 Step 2: Run in a Container

```bash
docker run --env-file .env \
  -v $(pwd)/downloads:/app/downloads \
  telegram-downloader
```

- ✅ Your `.env` will inject credentials
- 💾 Downloads are saved to your host `downloads/` folder
- 🔐 Ensure `.env` is **excluded** from version control

---

## 🧱 Docker Compose (Recommended Method)

### 📄 Step 1: Validate Your `.env`

Ensure your `.env` file is populated and placed in the project root.

### ▶️ Step 2: Start with Docker Compose

```bash
docker-compose up --build
```

Benefits:

- ✅ Automatically loads environment variables
- 🔁 Restarts if the container crashes
- 💾 Mounts persistent download volume

To stop:

```bash
docker-compose down
```

---

## 🛑 Important Notes

### 🔒 Sensitive Files

- `session_name.session*` - Stores your Telegram session. Keep private.

### 📝 Logging

- Logs are saved to `telegram_bot.log`
- Log rotation: 10MB size / 10-day retention

To monitor logs:

```bash
tail -f telegram_bot.log
```

### 🛠 File Permission Fix (For Docker Linux Hosts)

Add this to `.env`:

```dotenv
INSIDE_DOCKER=1
```

This will run `chown -R 1000:1000 /app/downloads` in container after downloads.

---

## 📦 Python Dependencies

| Package         | Use Case                                    |
| --------------- | ------------------------------------------- |
| `telethon`      | Telegram API interaction                    |
| `tqdm`          | Download progress bars                      |
| `loguru`        | Logging with rotation and ease of use       |
| `retrying`      | Retry logic for network resilience          |
| `python-dotenv` | Load environment variables from `.env` file |

To pin versions:

```bash
pip freeze > requirements.txt
```

---

## 🛠️ Contributing

We welcome all kinds of contributions!

- 🐛 Found a bug? Open an [issue](https://github.com/achiraanth/telegram-media-downloader/issues)
- 💡 Suggest a feature? Submit a PR
- ⭐ Like the project? Star it!

To contribute:

```bash
git clone https://github.com/achiraanth/telegram-media-downloader.git
cd telegram-media-downloader
git checkout -b your-feature-branch
```

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
Use it freely with credit.

---

## 👤 Author

Built with ❤️ by [Chiraanth](https://github.com/achiraanth)

> Follow me on GitHub for updates, tools, and more projects 🚀

