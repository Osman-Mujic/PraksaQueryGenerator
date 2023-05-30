import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json

root = tk.Tk()
root.title("SQL Query generator")
root.geometry("490x600")
root.configure(bg='#202020')

menu_bar = tk.Menu(root)
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Info", command=lambda: messagebox.showinfo("Help", "In order to use the program you will "
                                                                                "need to write a sql query + add a {"
                                                                                "brojac} somewhere in the query, "
                                                                                "after you finish your query add "
                                                                                "digits that you want your query to "
                                                                                "go from and to or do it in a custom "
                                                                                "order if you wish that ( you can "
                                                                                "only do one of the two ways not "
                                                                                "both).\n\nAfter that click the view "
                                                                                "button and your query should be "
                                                                                "generated, if you wish to reuse it "
                                                                                "you can save it using the save "
                                                                                "button and giving it a name (DO NOT "
                                                                                "NAME MULTIPLE TEMPLATES WITH THE "
                                                                                "SAME NAME).\n\nAfter that you will "
                                                                                "have some more options to rename a "
                                                                                "saved template or to delete it. To "
                                                                                "use the saved templates it is best "
                                                                                "to click on a selected template and "
                                                                                "then use the keyboard to navigate to "
                                                                                "your desired template because the "
                                                                                "mouse does not interact the best "
                                                                                "with a listbox."))

menu_bar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menu_bar)

query_label = tk.Label(root, text="Query")
query_label.configure(font=('Arial', 12), fg='#f0f0f0', bg='#202020')
query_label.place(x=220, y=20)

query_textbox = tk.Text(root, height=8, width=50)
query_textbox.configure(font=('Arial', 12), fg='#f0f0f0', bg='#404040')
query_textbox.place(x=20, y=50)

od_label = tk.Label(root, text="From:")
od_label.configure(font=('Arial', 12), fg='#f0f0f0', bg='#202020')
od_label.place(x=130, y=220)

od_textbox = tk.Entry(root)
od_textbox.configure(font=('Arial', 12), fg='#f0f0f0', bg='#404040', width=5)
od_textbox.place(x=180, y=220)

do_label = tk.Label(root, text="To:")
do_label.configure(font=('Arial', 12), fg='#f0f0f0', bg='#202020')
do_label.place(x=240, y=220)

do_textbox = tk.Entry(root)
do_textbox.configure(font=('Arial', 12), fg='#f0f0f0', bg='#404040', width=5)
do_textbox.place(x=275, y=220)

custom_label = tk.Label(root, text="Custom order")
custom_label.configure(font=('Arial', 12), fg='#f0f0f0', bg='#202020')
custom_label.place(x=190, y=255)

custom_textbox = tk.Entry(root)
custom_textbox.configure(font=('Arial', 12), fg='#f0f0f0', bg='#404040', width=50)
custom_textbox.place(x=20, y=280)

list_label = tk.Label(root, text="Choose a template")
list_label.configure(font=('Arial', 12), fg='#f0f0f0', bg='#202020')
list_label.place(x=180, y=310)

name_listbox = tk.Listbox(root)
name_listbox.configure(bg='#404040', fg='#f0f0f0', font=('Arial', 12))
name_listbox.place(x=20, y=340, width=455, height=200)


def get_query_text():
    return query_textbox.get("1.0", "end-1c")


def load_templates():
    try:
        with open('templates.json', 'r') as file:
            templates = [json.loads(line.strip()) for line in file if line.strip()]
        return templates
    except FileNotFoundError:
        return []


templates = load_templates()

for template in templates:
    name_listbox.insert(tk.END, template['name'])


def save():
    query = get_query_text()
    od = od_textbox.get()
    do = do_textbox.get()
    custom_order = custom_textbox.get()

    if "{brojac}" in query:
        if (od and do) or custom_order:
            template = {
                'name': '',
                'query': query,
                'od': od,
                'do': do,
                'custom_order': custom_order
            }

            template_name = tk.simpledialog.askstring("Template Name", "Enter a name for the template:")
            if template_name:
                template['name'] = template_name

                with open('templates.json', 'a') as file:
                    file.write(json.dumps(template) + '\n')

                name_listbox.insert(tk.END, template_name)
            else:
                messagebox.showerror("Error", "Template name cannot be empty.")
        else:
            messagebox.showerror("Error", "Please provide either 'From' and 'To' values or a 'Custom order' value.")
    else:
        messagebox.showerror("Error", "Query must contain {brojac}")



def select_template(event):
    selected_template = name_listbox.get(tk.ACTIVE)

    with open('templates.json', 'r') as file:
        templates = [json.loads(line) for line in file]

    selected_template_data = next((template for template in templates if template['name'] == selected_template), None)

    if selected_template_data:
        query_textbox.delete("1.0", tk.END)
        query_textbox.insert("1.0", selected_template_data['query'])

        od_textbox.delete(0, tk.END)
        od_textbox.insert(tk.END, str(selected_template_data['od']))

        do_textbox.delete(0, tk.END)
        do_textbox.insert(tk.END, str(selected_template_data['do']))

        custom_textbox.delete(0, tk.END)
        custom_textbox.insert(tk.END, selected_template_data.get('custom_order', ''))



name_listbox.bind("<<ListboxSelect>>", select_template)


def preview():
    query = get_query_text()
    od = od_textbox.get()
    do = do_textbox.get()
    custom_order = custom_textbox.get()

    if od and do and not custom_order:
        if "{brojac}" in query:
            generated_queries = []
            for i in range(int(od), int(do) + 1):
                generated_query = query.replace("{brojac}", str(i))
                generated_queries.append(generated_query)

            preview_window = tk.Toplevel(root)
            preview_window.state("zoomed")
            preview_window.title("Preview Queries")
            preview_window.geometry("550x500")
            preview_window.configure(bg='#202020')

            preview_textbox = tk.Text(preview_window, height=240, width=200)
            preview_textbox.pack(pady=20)

            for query in generated_queries:
                preview_textbox.insert(tk.END, query + "\n")
        else:
            messagebox.showerror("Error", "Query must contain {brojac}")
    elif custom_order and not od and not do:
        if "{brojac}" in query:
            custom_order_list = custom_order.split(',')
            generated_queries = []
            for item in custom_order_list:
                generated_query = query.replace("{brojac}", item.strip())
                generated_queries.append(generated_query)

            preview_window = tk.Toplevel(root)
            preview_window.state("zoomed")
            preview_window.title("Preview Queries")
            preview_window.geometry("550x500")
            preview_window.configure(bg='#202020')

            preview_textbox = tk.Text(preview_window, height=240, width=200)
            preview_textbox.pack(pady=20)

            for query in generated_queries:
                preview_textbox.insert(tk.END, query + "\n")
        else:
            messagebox.showerror("Error", "Query must contain {brojac}")
    else:
        messagebox.showerror("Error", "Please provide either 'From' and 'To' values or a 'Custom order' value.")


def delete():
    selected_query = name_listbox.get(tk.ACTIVE)
    if selected_query:
        confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete this query?")
        if confirm:
            name_listbox.delete(tk.ACTIVE)

            with open('templates.json', 'r') as file:
                templates = [json.loads(line) for line in file]

            templates = [template for template in templates if template['name'] != selected_query]

            with open('templates.json', 'w') as file:
                for template in templates:
                    file.write(json.dumps(template) + '\n')


def rename_template():
    selected_template = name_listbox.get(tk.ACTIVE)
    if selected_template:
        new_name = simpledialog.askstring("Rename Template", "Enter a new name for the template:")
        if new_name:
            with open('templates.json', 'r') as file:
                templates = [json.loads(line) for line in file]

            template = next((t for t in templates if t['name'] == selected_template), None)

            if template:
                template['name'] = new_name

                with open('templates.json', 'w') as file:
                    for t in templates:
                        file.write(json.dumps(t) + '\n')

                name_listbox.delete(tk.ACTIVE)
                name_listbox.insert(tk.END, new_name)
            else:
                messagebox.showerror("Error", "Selected template not found.")
        else:
            messagebox.showerror("Error", "New name cannot be empty.")


button_save = tk.Button(root, text="Save", command=save)
button_save.configure(bg='#008a00', cursor='hand2', fg='#f0f0f0', font=('Arial', 12, 'bold'))
button_save.place(x=20, y=550)

button_preview = tk.Button(root, text="View", command=preview)
button_preview.configure(bg='blue', cursor='hand2', fg='#f0f0f0', font=('Arial', 12, 'bold'))
button_preview.place(x=100, y=550)

button_delete = tk.Button(root, text="Delete", command=delete)
button_delete.configure(bg='#a60000', cursor='hand2', fg='#f0f0f0', font=('Arial', 12, 'bold'))
button_delete.place(x=300, y=550)

button_rename = tk.Button(root, text="Rename", command=rename_template)
button_rename.configure(bg='purple', cursor='hand2', fg='#f0f0f0', font=('Arial', 12, 'bold'))
button_rename.place(x=400, y=550)

root.mainloop()
