import graphviz
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
import os
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace') if hasattr(sys.stdout, 'reconfigure') else None

# --- Graphviz PATH (gerekirse duzenle) ---
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

counter = [0]

def add_nodes(dot, tree, parent_id=None):
    if isinstance(tree, dict):
        for key, value in tree.items():
            node_id = f"node_{counter[0]}"
            counter[0] += 1

            if isinstance(value, str):
                # key dugumu (non-terminal)
                dot.node(node_id, label=key, shape="ellipse",
                         style="filled", fillcolor="#D6EAF8", color="#2980B9",
                         fontname="Sans Bold", fontsize="13")
                if parent_id:
                    dot.edge(parent_id, node_id)

                # terminal yaprak dugumu
                leaf_id = f"node_{counter[0]}"
                counter[0] += 1
                dot.node(leaf_id, label=value, shape="box",
                         style="filled,rounded", fillcolor="#2980B9", color="#1A5276",
                         fontcolor="white", fontname="Sans Bold", fontsize="12")
                dot.edge(node_id, leaf_id)

            else:
                dot.node(node_id, label=key, shape="ellipse",
                         style="filled", fillcolor="#D5F5E3", color="#27AE60",
                         fontname="Sans Bold", fontsize="13")
                if parent_id:
                    dot.edge(parent_id, node_id)
                add_nodes(dot, value, parent_id=node_id)


def json_to_image(tree_json, title="Parse Tree"):
    """JSON'dan graphviz PNG olusturur, PIL Image olarak doner (dosyaya yazmadan)."""
    counter[0] = 0

    dot = graphviz.Digraph(
        comment=title,
        graph_attr={
            "rankdir": "TB",
            "splines": "ortho",
            "nodesep": "0.5",
            "ranksep": "0.6",
            "bgcolor": "white",
            "fontname": "Sans",
            "label": title,
            "labelloc": "t",
            "fontsize": "15",
        },
        edge_attr={"color": "#555555", "arrowsize": "0.7"}
    )

    add_nodes(dot, tree_json)

    # PNG'yi bellege render et (dosyaya yazmadan)
    png_bytes = dot.pipe(format="png")
    image = Image.open(io.BytesIO(png_bytes))
    return image

def show_trees(trees: list[dict]):

    root = tk.Tk()
    root.title("Parse Tree Viewer")
    root.geometry("900x650")
    root.configure(bg="#1e1e2e")

    header = tk.Label(root, text="Parse Tree Viewer",
                      bg="#1e1e2e", fg="#cdd6f4",
                      font=("Segoe UI", 16, "bold"), pady=10)
    header.pack()

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TNotebook", background="#1e1e2e", borderwidth=0)
    style.configure("TNotebook.Tab", background="#313244", foreground="#cdd6f4",
                    font=("Segoe UI", 11), padding=[12, 6])
    style.map("TNotebook.Tab",
              background=[("selected", "#89b4fa")],
              foreground=[("selected", "#1e1e2e")])

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    for item in trees:
        title = item.get("title", "Tree")
        tree_json = item["json"]

        frame = tk.Frame(notebook, bg="#1e1e2e")
        notebook.add(frame, text=title)

        loading = tk.Label(frame, text="Render ediliyor...",
                           bg="#1e1e2e", fg="#a6adc8", font=("Segoe UI", 12))
        loading.pack(expand=True)
        root.update()

        img = json_to_image(tree_json, title=title)
        loading.destroy()

        canvas_frame = tk.Frame(frame, bg="#1e1e2e")
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
        h_scroll = tk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
        v_scroll = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)

        canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)

        h_scroll.pack(side="bottom", fill="x")
        v_scroll.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        photo = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.configure(scrollregion=(0, 0, img.width, img.height))
        canvas.image = photo  

        def on_mousewheel(event, c=canvas):
            c.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<MouseWheel>", on_mousewheel)

    root.mainloop()