import tkinter as tk
from tkinter import messagebox
from string import ascii_uppercase
import random

VIGENERE = {
    (letter1, letter2): ascii_uppercase[(ascii_uppercase.index(letter1) + ascii_uppercase.index(letter2)) % 26]
    for letter1 in ascii_uppercase
    for letter2 in ascii_uppercase
}

def encrypt(message, key):
    message = message.upper().replace(" ", "")
    key = key.upper()
    encrypted_message = ""
    key_repeated = (key * (len(message) // len(key) + 1))[:len(message)]

    for m_char, k_char in zip(message, key_repeated):
        if m_char in ascii_uppercase:
            encrypted_message += VIGENERE[(m_char, k_char)]
        else:
            encrypted_message += m_char

    return encrypted_message

def decrypt(message, key):
    message = message.upper().replace(" ", "")
    key = key.upper()
    decrypted_message = ""
    key_repeated = (key * (len(message) // len(key) + 1))[:len(message)]

    for m_char, k_char in zip(message, key_repeated):
        if m_char in ascii_uppercase:
            decrypted_message += ascii_uppercase[(ascii_uppercase.index(m_char) - ascii_uppercase.index(k_char)) % 26]
        else:
            decrypted_message += m_char

    return decrypted_message


def generate_key(length):
    return ''.join(random.choice(ascii_uppercase) for _ in range(length))

def hack(message, max_key_length=10):
    possible_messages = []
    for key_length in range(1, max_key_length + 1):
        for i in range(26 ** key_length):
            key = ''.join(ascii_uppercase[i // (26 ** j) % 26] for j in range(key_length))
            decrypted = decrypt(message, key)
            possible_messages.append((key, decrypted))
    return possible_messages


def encrypt_button_handler():
    message = entry_message.get()
    key = entry_key.get()
    if not key:
        messagebox.showerror("Ошибка", "Ключ не может быть пустым!")
        return
    encrypted = encrypt(message, key)
    result_label.config(text=f"Зашифрованное сообщение: {encrypted}")

def decrypt_button_handler():
    message = entry_message.get()
    key = entry_key.get()
    if not key:
        messagebox.showerror("Ошибка", "Ключ не может быть пустым!")
        return
    decrypted = decrypt(message, key)
    result_label.config(text=f"Расшифрованное сообщение: {decrypted}")

def generate_key_button_handler():
    key_length = int(entry_key_length.get())
    if key_length <= 0:
        messagebox.showerror("Ошибка", "Длина ключа должна быть положительным числом!")
        return
    key = generate_key(key_length)
    entry_key.delete(0, tk.END)
    entry_key.insert(0, key)

def hack_button_handler():
    message = entry_message.get()
    possible_messages = hack(message)
    result_label.config(text="Возможные варианты:")
    for key, msg in possible_messages[:10]: 
        result_label.config(text=result_label.cget("text") + f"\nКлюч: {key}, Сообщение: {msg}")

root = tk.Tk()
root.title("Шифр Виженера")


label_message = tk.Label(root, text="Введите сообщение:")
label_message.pack()

entry_message = tk.Entry(root, width=60)
entry_message.pack()

label_key = tk.Label(root, text="Введите ключ:")
label_key.pack()

entry_key = tk.Entry(root, width=40)
entry_key.pack()

label_key_length = tk.Label(root, text="Длина ключа для генерации:")
label_key_length.pack()

entry_key_length = tk.Entry(root, width=10)
entry_key_length.pack()

encrypt_button = tk.Button(root, text="Шифрование", command=encrypt_button_handler)
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Расшифровка", command=decrypt_button_handler)
decrypt_button.pack()

generate_key_button = tk.Button(root, text="Генерация ключа", command=generate_key_button_handler)
generate_key_button.pack()

hack_button = tk.Button(root, text="Взломать", command=hack_button_handler)
hack_button.pack()

result_label = tk.Label(root, text="Результат:")
result_label.pack()

root.mainloop()