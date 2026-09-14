<div align="center">
  <h1>🌊 flow-cli</h1>
  <p><b>A beautiful, minimalist Pomodoro & focus timer for the terminal.</b></p>
  
  <p>
    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="Python version" />
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" />
    <img src="https://img.shields.io/badge/productivity-100%25-brightgreen.svg" alt="Productivity" />
  </p>
</div>

<br/>

I wanted a simple Pomodoro timer that runs entirely in the terminal, looks gorgeous, and keeps track of how much deep work I actually do during the day. All the other apps were either full of distractions, required accounts, or lived in the browser. 

So I built **flow-cli**. It's lightweight, uses `rich` for a stunning progress bar, and automatically logs your daily focus time in a local SQLite database.

## ✨ Features

- 🍅 **Pomodoro Timer**: Classic 25-minute focus blocks, or custom durations.
- ☕️ **Break Timer**: Easily start 5-minute (or custom) breaks.
- 📊 **Daily Stats**: See how many focus sessions and total minutes you've completed today.
- 🎨 **Beautiful UI**: Gorgeously rendered progress bars right in your terminal.
- 🔔 **Alerts**: Terminal bell notification when your session finishes.

## 📦 Installation

Clone the repo and install it locally using `pip`:

```bash
git clone https://github.com/muhammetefesahan/flow-cli.git
cd flow-cli
pip install .
```

*Tip: You can also use `pipx install .` if you want to install it globally without affecting your system Python environment.*

## 🛠️ Usage

### Start a Focus Session
Start a standard 25-minute Pomodoro session:
```bash
flow start
```

Want a longer deep-work session? Set custom minutes:
```bash
flow start -m 50
```

### Take a Break
Start a standard 5-minute break:
```bash
flow break
```
Or a longer 15-minute break:
```bash
flow break -m 15
```

### Check Your Stats
Wondering how productive you were today? Check your stats:
```bash
flow stats
```

## 🧠 Why I built this
As a developer, my terminal is my home. Switching to a browser or mobile app just to check a timer breaks my flow. **flow-cli** is designed to stay out of your way and just let you code. If you find it useful for your deep work sessions, leave a ⭐!

## 🤝 Contributing
Pull requests are always welcome! Whether it's adding new features like task tagging, or just fixing a typo. 

## 📄 License
[MIT](LICENSE) © Efe
