# 📸 PixGram — Instagram-like Social Media App

![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)
![Django](https://img.shields.io/badge/Django-4.2-green?style=flat-square&logo=django)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple?style=flat-square&logo=bootstrap)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

> A full-featured Instagram-inspired social media web application built with Django & Python.

---

## 🌐 Live Demo

🔗 **[pixgram.onrender.com](https://pixgram.onrender.com)**

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 **Authentication** | Signup, Login, Logout with validation |
| 👤 **User Profiles** | Profile photo, bio, edit profile |
| 📸 **Posts** | Create, Read, Update, Delete posts |
| ❤️ **Likes** | Like / Unlike posts |
| 💬 **Comments** | Add comments on posts |
| 👥 **Follow System** | Follow / Unfollow users |
| 🔔 **Notifications** | Like, comment & follow notifications |
| 🔍 **Search** | Search users and posts |
| 🧭 **Explore** | Trending posts & suggested users |
| 🔖 **Save Posts** | Bookmark favorite posts |
| 📖 **Stories** | 24-hour expiring stories |
| 💌 **Direct Messages** | Private messaging between users |
| 🔗 **Share Posts** | Copy link or share via WhatsApp |
| 📱 **Mobile Responsive** | Instagram-like bottom navigation |

---

## 🛠️ Tech Stack

```
Backend    →  Python 3.12 + Django 4.2
Frontend   →  Bootstrap 5 + Bootstrap Icons
Database   →  SQLite (dev) / PostgreSQL (prod)
Storage    →  Cloudinary (media files)
Deploy     →  Render.com
```

---

## 📂 Project Structure

```
pixgram/
├── accounts/          # Auth + Profile + Follow
├── posts/             # Posts + Stories + DM + Notifications
├── templates/         # All HTML templates
│   ├── accounts/      # Login, Signup, Profile
│   ├── posts/         # Feed, Explore, Notifications
│   ├── stories/       # Create & View stories
│   └── dm/            # Direct messages
├── static/            # CSS, JS, Images
├── media/             # Uploaded files
├── manage.py
└── requirements.txt
```

---

## 🚀 Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/amitsgupta11/pixgram.git
cd pixgram
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create superuser (optional)
```bash
python manage.py createsuperuser
```

### 6. Run server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser 🎉

---

## 📸 Screenshots

| Feed | Profile | Explore |
|---|---|---|
| Instagram-style feed with stories | User profile with post grid | Trending posts & suggested users |

| Direct Messages | Notifications | Stories |
|---|---|---|
| Private chat inbox | Like/comment/follow alerts | 24-hour stories |

---

## 🔑 Environment Variables

Create a `.env` file or set these in your deployment platform:

```
SECRET_KEY     = your-secret-key
DEBUG          = False
DATABASE_URL   = your-database-url
CLOUD_NAME     = your-cloudinary-name
API_KEY        = your-cloudinary-api-key
API_SECRET     = your-cloudinary-api-secret
```

---

## 📱 Mobile Support

PixGram is fully responsive with:
- Instagram-style **bottom navigation** on mobile
- Optimized layouts for all screen sizes
- Touch-friendly UI components

---

## 🗄️ Database Models

```
User (Django built-in)
├── Profile      — avatar, bio
├── Follow       — follower/following
Post
├── Like         — user + post
├── Comment      — user + post + text
├── SavedPost    — bookmarks
├── Notification — like/comment/follow alerts
Story
├── StoryView    — view tracking
DirectMessage    — sender + receiver + message
```

---

## 👨‍💻 Developer

<div align="center">

**Amit Gupta**

Full-Stack Developer | Python & Django Enthusiast

[![GitHub](https://img.shields.io/badge/GitHub-amitsgupta11-black?style=flat-square&logo=github)](https://github.com/amitsgupta11)

*Built with ❤️ using Django & Python*

</div>

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">
  <strong>⭐ Star this repo if you like it!</strong>
</div>
