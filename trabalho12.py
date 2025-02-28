import tkinter as tk
from tkinter import messagebox
import json
import os


def carregar_tarefas():
    """Carrega as tarefas do arquivo JSON"""
    try:
        if not os.path.exists("tasks.json"):
            raise FileNotFoundError("Arquivo de tarefas não encontrado. Criando um novo arquivo.")
        with open("tasks.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        if isinstance(e, FileNotFoundError):
            # Criar um arquivo vazio se não existir
            with open("tasks.json", "w") as file:
                json.dump([], file, indent=4)
        messagebox.showerror("Erro ao carregar tarefas", f"Erro ao carregar as tarefas: {str(e)}")
        return []


def salvar_tarefas(tarefas):
    """Salva as tarefas no arquivo JSON"""
    try:
        with open("tasks.json", "w") as file:
            json.dump(tarefas, file, indent=4)
    except IOError as e:
        messagebox.showerror("Erro ao salvar tarefas", f"Erro ao salvar as tarefas: {str(e)}")


def adicionar_tarefa(titulo, status):
    """Adiciona uma nova tarefa"""
    tarefas = carregar_tarefas()
    tarefas.append({"titulo": titulo, "status": status})
    salvar_tarefas(tarefas)


def atualizar_status(index, status):
    """Atualiza o status de uma tarefa"""
    tarefas = carregar_tarefas()
    try:
        tarefas[index]["status"] = status
        salvar_tarefas(tarefas)
    except IndexError:
        messagebox.showerror("Erro ao atualizar", "Índice de tarefa inválido.")


def excluir_tarefa(index):
    """Exclui uma tarefa"""
    tarefas = carregar_tarefas()
    try:
        del tarefas[index]
        salvar_tarefas(tarefas)
    except IndexError:
        messagebox.showerror("Erro ao excluir", "Índice de tarefa inválido.")


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas")
        self.root.geometry("500x400")

        self.lista_tarefas = tk.Listbox(self.root, height=10, width=50)
        self.lista_tarefas.pack(pady=20)

        self.carregar_lista_tarefas()

        self.titulo_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pendente")

        self.frame_form = tk.Frame(self.root)
        self.frame_form.pack(pady=10)

        tk.Label(self.frame_form, text="Título:").grid(row=0, column=0, padx=5)
        self.entry_titulo = tk.Entry(self.frame_form, textvariable=self.titulo_var, width=30)
        self.entry_titulo.grid(row=0, column=1)

        tk.Label(self.frame_form, text="Status:").grid(row=1, column=0, padx=5)
        self.combobox_status = tk.OptionMenu(self.frame_form, self.status_var, "Pendente", "Em Progresso", "Concluída")
        self.combobox_status.grid(row=1, column=1)

        self.botao_adicionar = tk.Button(self.root, text="Adicionar Tarefa", command=self.adicionar_tarefa)
        self.botao_adicionar.pack(pady=5)

        self.botao_atualizar = tk.Button(self.root, text="Atualizar Status", command=self.atualizar_status)
        self.botao_atualizar.pack(pady=5)

        self.botao_excluir = tk.Button(self.root, text="Excluir Tarefa", command=self.excluir_tarefa)
        self.botao_excluir.pack(pady=5)

    def carregar_lista_tarefas(self):
        """Carrega as tarefas na Listbox"""
        tarefas = carregar_tarefas()
        self.lista_tarefas.delete(0, tk.END)
        for tarefa in tarefas:
            self.lista_tarefas.insert(tk.END, f"{tarefa['titulo']} - {tarefa['status']}")

    def adicionar_tarefa(self):
        """Adiciona uma tarefa a partir dos campos de entrada"""
        titulo = self.titulo_var.get()
        status = self.status_var.get()
        if not titulo:
            messagebox.showerror("Erro", "O título não pode estar vazio.")
            return
        try:
            adicionar_tarefa(titulo, status)
            self.carregar_lista_tarefas()
            self.titulo_var.set("")  
        except Exception as e:
            messagebox.showerror("Erro ao adicionar tarefa", f"Ocorreu um erro: {str(e)}")

    def atualizar_status(self):
        """Atualiza o status da tarefa selecionada"""
        try:
            index = self.lista_tarefas.curselection()[0]
            novo_status = self.status_var.get()
            atualizar_status(index, novo_status)
            self.carregar_lista_tarefas()
        except IndexError:
            messagebox.showerror("Erro", "Selecione uma tarefa para atualizar.")
        except Exception as e:
            messagebox.showerror("Erro ao atualizar", f"Ocorreu um erro: {str(e)}")

    def excluir_tarefa(self):
        """Exclui a tarefa selecionada"""
        try:
            index = self.lista_tarefas.curselection()[0]
            excluir_tarefa(index)
            self.carregar_lista_tarefas()
        except IndexError:
            messagebox.showerror("Erro", "Selecione uma tarefa para excluir.")
        except Exception as e:
            messagebox.showerror("Erro ao excluir", f"Ocorreu um erro: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
