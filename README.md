📱 Social Media Web Application

A full-featured social media web application that allows users to connect, share, and interact online. Built using Django, the platform supports user authentication, posting, commenting, likes, friend requests, real-time notifications, and more — all within a modern and responsive UI.

📄 Description

This project is a full-featured social media web application that enables users to connect, share, and engage with others online. Users can register, log in, create and manage posts, comment, like, send and accept friend requests, and receive real-time notifications.

Each user has a customizable profile that includes a profile photo and bio. The platform also features a search function to find users or posts easily. The application uses Django on the backend, ensuring robust authentication, media handling, and clean project structuring for scalability and maintenance.

The frontend is built with Django templates for dynamic content rendering, and static files for styling and interaction.
✨ Features

- ✅ User registration and login
- 🧑‍💼 User profiles with bios and profile photos
- 📝 Create, edit, and delete posts
- 💬 Comment and like functionality
- 🤝 Friend request system (send, accept)
- 🔔 Real-time notifications
- 🔍 Search functionality for users and posts
- 📱 Fully responsive and modern UI

---
 🧰 Technologies Used

- **Backend:** Django (Python Web Framework)
- **Database:** SQLite (default Django database)
- **Frontend:** HTML, CSS, JavaScript (for interactivity)
- **Templating Engine:** Django Templates
- **Media Handling:** Uploaded media files (profile pictures, post images)
- **Static Files:** CSS, JS, and images
- **OS:** Windows (development environment)

🗂 Project Structure

.
├── accounts/      # Django app for user accounts and social features
├── backend/       # Django project settings and configuration
├── users/         # Django app for user management
├── templates/     # HTML templates for rendering pages
├── static/        # Static files (images, CSS, JS)
├── media/         # Uploaded media files (profile photos, post images)
├── db.sqlite3     # SQLite database file
└── manage.py      # Django management script
<img width="1767" height="902" alt="image" src="https://github.com/user-attachments/assets/6f21fb1a-3711-48e1-bc41-d741bfd1b973" />
<img width="1748" height="898" alt="image" src="https://github.com/user-attachments/assets/33a5bbae-bebf-4210-9511-1a6d97862684" />
## ⚙️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <project-directory>

2. **Set up a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install django
   ```

4. **Apply migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (admin):**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## ▶️ Usage

* Register a new account or log in with existing credentials
* Create and manage posts from your profile or home page
* Like or comment on posts and send friend requests to others
* Receive real-time notifications for interactions
* Search users or posts via the search bar
🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.
## 📜 License

This project is created for **educational purposes** only and is not intended for production use.


Let me know if you want a downloadable `.md` file, project logo suggestion, or deployment instructions (like how to host this on **Render**, **Heroku**, or **PythonAnywhere**).

