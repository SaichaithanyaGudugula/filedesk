# FileDesk

A small web app for creating, reading, updating and deleting text files from the browser. It started as a command-line Python script and now has a Streamlit interface.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4B4B?logo=streamlit&logoColor=white)


[FileDesk screenshot](screenshots/home.png)


## Features

- **Create** a file with a name and content. If the file already exists, it is not overwritten.
- **Read** a file and see its character, word and line counts. You can also download it.
- **Update** a file in three ways: rename it, append text to the end, or overwrite the whole content.
- **Delete** a file after ticking a confirmation box.
- A live list of your files with their sizes, plus summary cards for file count, total size and last change.

## How it works

- Built with Python's `pathlib` for file handling and Streamlit for the interface.
- Every file lives inside a `workspace/` folder, and file names are reduced to their base name so paths like `../secret.txt` cannot escape it.
- If you enter a name without an extension, `.txt` is added.
- Errors (empty name, file exists, unreadable file) show a clear message instead of crashing.

## Run it locally

```bash
git clone https://github.com/SaichaithanyaGudugula/filedesk.git
cd filedesk

python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

Then open the address Streamlit prints, usually http://localhost:8501.

## Project structure

```
filedesk/
├── app.py            # the Streamlit app
├── requirements.txt
├── .gitignore
└── README.md
```

## Change the colors

All colors are variables at the top of `app.py` (`BG`, `INK`, `ACCENT`, `TAB` and so on). Change the hex values to restyle the whole app.

## What I learned

- Reading, writing, renaming and deleting files with `pathlib`
- Turning a command-line script into a web interface with Streamlit
- Validating input and handling errors so the app does not crash
- Keeping file access inside one folder for safety

## Ideas for next steps

- Search across files
- Upload files from your computer
- Support for folders
- Edit files in place with a larger editor

## License

MIT. Add a `LICENSE` file if you want others to reuse the code.
