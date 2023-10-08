import wikipediaapi
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

# Initialize Wikipedia API for each language, including Catalan
LANGUAGES = ['en', 'es', 'fr', 'de', 'it', 'pt', 'el', 'la', 'ca']
LANGUAGE_NAMES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'el': 'Greek',
    'la': 'Latin',
    'ca': 'Catalan'
}
wiki_objects = {lang: wikipediaapi.Wikipedia('MyApp (example@example.com)', lang) for lang in LANGUAGES}

def open_url(url):
    webbrowser.open(url)
    entry.focus_set()  # Refocus on the search box

def create_language_buttons(available_translations):
    # Destroy old buttons and labels
    for widget in lang_button_frame.winfo_children():
        widget.destroy()
    
    for lang, translation in available_translations.items():
        sub_frame = ttk.Frame(lang_button_frame)
        sub_frame.pack(side=tk.LEFT, anchor='n', padx=5, pady=5)

        btn = ttk.Button(sub_frame, text=LANGUAGE_NAMES[lang], command=lambda link=translation.fullurl: open_url(link))
        btn.grid(row=0, column=0, sticky="n")
        
        label = ttk.Label(sub_frame, text=translation.title, wraplength=100, justify='center')
        label.grid(row=1, column=0, sticky="n")

def search_term(event=None):
    status_indicator.config(bg="red")
    root.update_idletasks()

    term = entry.get()
    if not term:
        messagebox.showinfo("Info", "Please enter a search term.")
        return

    # Attempt to retrieve the page for various capitalizations of the term
    variations = [term, term.title(), term.capitalize()]
    
    for variant in variations:
        summaries = {lang: wiki_objects[lang].page(variant).summary for lang in LANGUAGES}
        detected_lang = max(summaries, key=lambda k: len(summaries[k]))
        if summaries[detected_lang]:
            break

    text_widget.delete(1.0, tk.END)
    if summaries[detected_lang]:
        text_widget.insert(tk.END, summaries[detected_lang])
        displayed_language_label.config(text=f"Text shown in: {LANGUAGE_NAMES[detected_lang]}", foreground="dodger blue")
    else:
        displayed_language_label.config(text="No results found.", foreground="red")

    page = wiki_objects[detected_lang].page(variant)
    available_translations = {lang: page.langlinks[lang] for lang in LANGUAGES if lang in page.langlinks}
    
    create_language_buttons(available_translations)

    if 'el' in available_translations:
        root.clipboard_clear()
        root.clipboard_append(available_translations['el'].title)
        root.update()
        lang_count_label.config(text=f"Languages found: {len(available_translations)}. Greek text copied.")
    else:
        lang_count_label.config(text=f"Languages found: {len(available_translations)}. No Greek versions found.")

    status_indicator.config(bg="green")

# GUI setup
root = tk.Tk()
root.title("Wikipedia Search")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.columnconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)
frame.rowconfigure(3, weight=1)

entry = ttk.Entry(frame)
entry.grid(row=0, column=0, sticky=tk.W + tk.E, padx=5, pady=5)
entry.focus_set()

search_btn = ttk.Button(frame, text="Search", command=search_term)
search_btn.grid(row=0, column=1, padx=5, pady=5)

text_widget = tk.Text(frame, wrap=tk.WORD)
text_widget.grid(row=1, column=0, columnspan=3, sticky=tk.W + tk.E + tk.N + tk.S, padx=5, pady=5)

displayed_language_label = ttk.Label(frame, text="", foreground="blue")
displayed_language_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)

lang_button_frame = ttk.Frame(frame)
lang_button_frame.grid(row=3, column=0, columnspan=3, sticky=tk.W, padx=5, pady=5)

lang_count_label = ttk.Label(frame, text="Languages found: 0", foreground="green")
lang_count_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)

status_indicator = tk.Canvas(frame, width=20, height=20, bg="green", bd=0, highlightthickness=0)
status_indicator.grid(row=0, column=2, padx=5, pady=5)

root.bind('<Return>', search_term)

root.mainloop()
